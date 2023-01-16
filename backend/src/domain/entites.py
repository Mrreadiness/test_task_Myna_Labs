from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

from src.domain.exceptions import DialogAlreadyExistException


class UserType(Enum):
    user = "user"
    bot = "bot"


@dataclass
class User:
    username: str
    type: UserType = UserType.user
    dialog: Dialog | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)

    async def create_dialog(self) -> None:
        if self.dialog is not None:
            raise DialogAlreadyExistException()
        self.dialog = Dialog()

    async def send_message(self, message: str) -> None:
        ...


class Bot(User):
    type = UserType.bot

    async def reply_to_message(self, message: Message) -> None:
        ...


@dataclass
class Dialog:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    messages: list[Message] = field(default_factory=list)
    users: list[User] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Message:
    value: str
    user: User
    dialog: Dialog
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
