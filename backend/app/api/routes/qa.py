import os
import yaml

from app.core.config import logger, settings


from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import get_buffer_string
from langchain_core.prompts import format_document

from langchain_community.vectorstores.pgvector import PGVector
from langchain.memory import ConversationBufferMemory

from langchain.prompts.prompt import PromptTemplate
from app.schemas.chat_schema import ChatBody
from fastapi import APIRouter, Depends
from app.api.deps import CurrentUser, get_current_user
from app.models.user_model import User

from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config/chat.yml")
with open(config_path, "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)

chat_config = config.get("CHAT_CONFIG", None)

logger.info(f"Chat config: {chat_config}")


@router.post("/chat")
async def chat_action(
    request: ChatBody,
    current_user: User = Depends(get_current_user),
    # request: ChatBody,
):

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
    logger.info(f"CONDENSE_QUESTION_PROMPT: {CONDENSE_QUESTION_PROMPT}")
    logger.info(f"ANSWER_PROMPT: {ANSWER_PROMPT}")
    logger.info(f"DEFAULT_DOCUMENT_PROMPT: {DEFAULT_DOCUMENT_PROMPT}")

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

    test = final_inputs["context"]

    logger.info(f"Final inputs: {test}")
    # And finally, we do the part that returns the answers
    answer = {
        "answer": final_inputs | ANSWER_PROMPT | ChatOpenAI(),
        "docs": itemgetter("docs"),
    }

    final_chain = loaded_memory | standalone_question | retrieved_documents | answer

    inputs = {"question": request.message}
    logger.info(f"Inputs: {inputs}")
    result = final_chain.invoke(inputs)

    test2 = result["answer"]

    logger.info(f"Result: {test2}")

    test3 = result["answer"].content

    logger.info(f"Result: {test3}")

    return {"data": result["answer"].content}
