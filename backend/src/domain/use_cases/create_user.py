from src.domain.entites import User
from src.domain.interfaces import AbstractUnitOfWork
from src.domain.use_cases.interfaces import ICreateUser


class CreateUser(ICreateUser):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, username: str) -> User:
        async with self.uow:
            user = User(username)
            bot = await self.uow.users.get_bot()
            await user.create_dialog(bot)
            await self.uow.users.add(user)
            await self.uow.commit()
            return user
