from __future__ import annotations

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
class User:
    username: str
    type: UserType = UserType.user
    dialog: Dialog | None = None
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)

    async def create_dialog(self, bot: Bot) -> None:
        if self.dialog is not None:
            raise DialogAlreadyExistException()
        self.dialog = Dialog(user=self, bot=bot)

    async def send_message(self, message: str) -> None:
        if self.dialog is None:
            raise DialogNotFoundException()

        await self._send_message(message, dialog=self.dialog)

    async def _send_message(self, message: str, dialog: Dialog) -> None:
        await dialog.receive_message(Message(value=message, user=self, dialog=dialog))


@dataclass()
class Bot(User):
    username: str = field(default="Bot", init=False)
    type = UserType.bot

    async def reply_to_message(self, message: Message) -> None:
        # echo mode
        await self._send_message(message.value, dialog=message.dialog)


@dataclass
class Dialog:
    user: User
    bot: Bot
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    __messages: list[Message] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow)

    @property
    def messages(self) -> Sequence[Message]:
        return self.__messages

    async def receive_message(self, message: Message) -> None:
        self.__messages.append(message)
        if message.user == self.user:
            # todo: a better way will send the event to the events queue and not block the user
            #  by waiting for bot reply
            await self.bot.reply_to_message(message)


@dataclass
class Message:
    value: str
    user: User
    dialog: Dialog
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow)
