from __future__ import annotations

import abc
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Sequence

from src.domain.exceptions import DialogAlreadyExistException, DialogNotFoundException


class UserType(Enum):
    user = "user"
    bot = "bot"


@dataclass
class BaseUser(abc.ABC):
    type: UserType
    id: uuid.UUID = field(default_factory=uuid.uuid4, init=False)
    created: datetime = field(default_factory=datetime.utcnow, init=False)

    async def _send_message(self, message: str, dialog: Dialog) -> None:
        _message = Message(value=message, user=self, dialog=dialog)
        await dialog.receive_message(_message)


@dataclass
class User(BaseUser):
    username: str
    dialog: Dialog | None = None
    type: UserType = field(default=UserType.user, init=False)

    async def create_dialog(self, bot: Bot) -> None:
        if self.dialog is not None:
            raise DialogAlreadyExistException()
        self.dialog = Dialog(user=self, bot=bot)

    async def send_message(self, message: str) -> None:
        if self.dialog is None:
            raise DialogNotFoundException()

        await self._send_message(message, dialog=self.dialog)


@dataclass()
class Bot(BaseUser):
    BOT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")
    id: uuid.UUID = field(default=BOT_ID, init=True)
    dialogs: list[Dialog] = field(default_factory=list, init=False)
    type: UserType = field(default=UserType.bot, init=False)

    async def reply_to_message(self, message: Message) -> None:
        # echo mode
        await self._send_message(message.value, dialog=message.dialog)


@dataclass
class Dialog:
    user: User
    bot: Bot
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    _messages: list[Message] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)

    @property
    def messages(self) -> Sequence[Message]:
        return self._messages

    async def receive_message(self, message: Message) -> None:
        self._messages.append(message)
        if message.user == self.user:
            # todo: a better way will send the event to the events queue and not block the user
            #  by waiting for bot reply
            await self.bot.reply_to_message(message)


@dataclass
class Message:
    value: str
    user: BaseUser
    dialog: Dialog
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
