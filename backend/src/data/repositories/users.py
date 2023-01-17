import uuid

from sqlalchemy import exc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, noload
from src.domain.entites import Bot, Dialog, User
from src.domain.exceptions import UserNotFoundException
from src.domain.use_cases.interfaces import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, user: User) -> None:
        self.session.add(user)

    async def get_user(self, user_id: uuid.UUID) -> User:
        query = (
            select(User)
            .options(
                joinedload(User.dialog).options(
                    noload(Dialog._messages), joinedload(Dialog.bot), joinedload(Dialog.user)
                )
            )
            .where(User.id == user_id)
        )
        try:
            return (await self.session.execute(query)).unique().scalar_one()
        except exc.NoResultFound:
            raise UserNotFoundException()

    async def get_bot(self) -> Bot:
        try:
            return (
                (await self.session.execute(select(Bot).where(Bot.id == Bot.BOT_ID)))
                .unique()
                .scalar_one()
            )
        except exc.NoResultFound:
            return await self._create_bot()

    async def _create_bot(self) -> Bot:
        bot = Bot()
        self.session.add(bot)
        return bot
