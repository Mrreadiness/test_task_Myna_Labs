from types import TracebackType
from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.config import PostgresDsn
from src.data.repositories.users import UserRepository
from src.domain.interfaces import AbstractUnitOfWork


class UnitOfWork(AbstractUnitOfWork):
    def __init__(self, dsn: PostgresDsn):
        engine = create_async_engine(dsn)
        self.session_factory = sessionmaker(
            engine,
            autoflush=True,
            autocommit=False,
            expire_on_commit=False,
            class_=AsyncSession,
        )

    async def __aenter__(self) -> None:
        await super().__aenter__()
        self.session: AsyncSession = self.session_factory()
        self.users = UserRepository(self.session)

    async def __aexit__(
        self,
        exc_t: Type[BaseException] | None,
        exc_v: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.session.expunge_all()
        await super().__aexit__(exc_t, exc_v, exc_tb)
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
