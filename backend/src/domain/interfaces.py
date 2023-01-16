import abc
from types import TracebackType
from typing import Type


class AbstractUnitOfWork(abc.ABC):
    @abc.abstractmethod
    async def commit(self) -> None:
        ...

    @abc.abstractmethod
    async def rollback(self) -> None:
        ...

    async def __aenter__(self) -> None:
        pass

    async def __aexit__(
        self,
        exc_t: Type[BaseException] | None,
        exc_v: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.rollback()
