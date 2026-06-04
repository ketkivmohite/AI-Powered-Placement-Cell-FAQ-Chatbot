from pydantic import BaseModel

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str

class ChatReq(BaseModel):
    message: str