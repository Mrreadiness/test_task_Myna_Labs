from src.domain.entites import User
from src.domain.interfaces import AbstractUnitOfWork
from src.domain.use_cases.interfaces import ICreateUser


class CreateUser(ICreateUser):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, username: str) -> User:
        async with self.uow:
            user = User(username)
            await self.uow.user.add(user)
            bot = await self.uow.user.get_bot()
            await user.create_dialog(bot)
            await self.uow.commit()
            return user
