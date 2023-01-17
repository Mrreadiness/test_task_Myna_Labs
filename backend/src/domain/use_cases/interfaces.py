import abc
import uuid

from src.domain.entites import Bot, User


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


class ICreateUser(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, username: str) -> User:
        ...


class ISendMessage(abc.ABC):
    @abc.abstractmethod
    async def __call__(self, user_id: uuid.UUID, message: str) -> None:
        ...
