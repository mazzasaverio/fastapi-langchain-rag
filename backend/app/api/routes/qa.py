from app.core.db import SessionLocal
import os
import yaml
from fastapi import APIRouter


from app.core.config import logger


from operator import itemgetter

from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel
from langchain_community.vectorstores.pgvector import PGVector
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from langchain.prompts.prompt import PromptTemplate
from pydantic import BaseModel

router = APIRouter()

config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.yml")
with open(config_path, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

chat_config = config.get("CHAT_CONFIG", None)


class ChatRequest(BaseModel):
    message: str


@router.post("/chat")
async def chat_action(request: ChatRequest):

    embeddings = OpenAIEmbeddings()

    store = PGVector(
        collection_name="docs",
        connection_string=settings.SYNC_DATABASE_URI,
        embedding_function=embeddings,
    )

    retriever = store.as_retriever()

    # Load prompts from configuration
    _template_condense = chat_config["PROMPTS"]["CONDENSE_QUESTION"]
    _template_answer = chat_config["PROMPTS"]["ANSWER_QUESTION"]
    _template_default_document = chat_config["PROMPTS"]["DEFAULT_DOCUMENT"]

    # Your existing logic here, replace hardcoded prompt templates with loaded ones
    # Example of using loaded prompts:
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template_condense)
    ANSWER_PROMPT = ChatPromptTemplate.from_template(_template_answer)
    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(_template_default_document)

    def _combine_documents(
        docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
    ):
        doc_strings = [format_document(doc, document_prompt) for doc in docs]

        return document_separator.join(doc_strings)

    memory = ConversationBufferMemory(
        return_messages=True, output_key="answer", input_key="question"
    )

    # First we add a step to load memory
    # This adds a "memory" key to the input object
    loaded_memory = RunnablePassthrough.assign(
        chat_history=RunnableLambda(memory.load_memory_variables)
        | itemgetter("history"),
    )
    # Now we calculate the standalone question
    standalone_question = {
        "standalone_question": {
            "question": lambda x: x["question"],
            "chat_history": lambda x: get_buffer_string(x["chat_history"]),
        }
        | CONDENSE_QUESTION_PROMPT
        | ChatOpenAI(temperature=0)
        | StrOutputParser(),
    }
    # Now we retrieve the documents
    retrieved_documents = {
        "docs": itemgetter("standalone_question") | retriever,
        "question": lambda x: x["standalone_question"],
    }
    # Now we construct the inputs for the final prompt
    final_inputs = {
        "context": lambda x: _combine_documents(x["docs"]),
        "question": itemgetter("question"),
    }

    logger.info(f"Final inputs: {final_inputs}")
    # And finally, we do the part that returns the answers
    answer = {
        "answer": final_inputs | ANSWER_PROMPT | ChatOpenAI(),
        "docs": itemgetter("docs"),
    }

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    inputs = {"question": request.message}
    result = final_chain.invoke(inputs)

    return result["answer"].content
