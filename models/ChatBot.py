from sqlmodel import SQLModel
from typing import Any


class ChatBotResponse(SQLModel):
    status:str
    resposne:Any