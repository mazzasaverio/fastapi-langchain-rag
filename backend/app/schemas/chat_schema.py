from pydantic import BaseModel


class ChatBody(BaseModel):
    message: str
