import abc
import uuid

from src.domain.entites import Bot, Message, User
from src.domain.types import Pagination


class IUserRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, user: User) -> None:
        ...

    @abc.abstractmethod
    async def get_user(self, user_id: uuid.UUID) -> User:
        ...

    @abc.abstractmethod
    async def get_bot(self) -> Bot:
        ...


class IMessagesRepository(abc.ABC):
    @abc.abstractmethod
    async def get_by_dialog_id(self, dialog_id: uuid.UUID, pagination: Pagination) -> User:
        ...


class ICreateUser(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, username: str) -> User:
        ...


class ISendMessage(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, user_id: uuid.UUID, message: str) -> None:
        ...


class IGetMessages(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, user_id: uuid.UUID, pagination: Pagination) -> list[Message]:
        ...
