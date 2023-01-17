import uuid

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.entites import Bot, User
from src.domain.exceptions import UserNotFoundException
from src.domain.use_cases.interfaces import IUserRepository


class UserRepository(IUserRepository):
    BOT_ID = uuid.UUID("00000000-0000-0000-0000-000000000000")

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        self.session.add(user)

    async def get_user(self, user_id: uuid.UUID) -> User:
        query = select(User).where(User.id == user_id)
        try:
            return (await self.session.execute(query)).scalar_one()
        except exc.NoResultFound:
            raise UserNotFoundException()

    async def get_bot(self) -> Bot:
        try:
            return (await self.session.execute(select(Bot))).scalar_one()
        except exc.NoResultFound:
            return await self._create_bot()

    async def _create_bot(self) -> Bot:
        bot = Bot(id=self.BOT_ID)
        self.session.add(bot)
        return bot
