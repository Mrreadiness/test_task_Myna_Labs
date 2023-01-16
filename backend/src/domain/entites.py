from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class UserType(Enum):
    user = "user"
    bot = "bot"


@dataclass
class User:
    username: str
    type: UserType = field(default=UserType.user)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow())


@dataclass
class Dialog:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    messages: list[Message] = field(default_factory=list)
    users: list[User] = field(default_factory=list)
    created: datetime = field(default_factory=datetime.utcnow())


@dataclass
class Message:
    value: str
    user: User
    dialog: Dialog
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created: datetime = field(default_factory=datetime.utcnow())
