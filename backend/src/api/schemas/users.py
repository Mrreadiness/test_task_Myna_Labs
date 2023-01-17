import datetime
import uuid

from pydantic import BaseModel


class UserInSchema(BaseModel):
    username: str


class UserOutSchema(BaseModel):
    id: uuid.UUID
    username: str

    class Config:
        orm_mode = True


class SendMessageInSchema(BaseModel):
    user_id: uuid.UUID
    message: str


class MessageOutSchema(BaseModel):
    id: uuid.UUID
    value: str
    created: datetime.datetime

    class Config:
        orm_mode = True
