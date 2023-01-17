import uuid

from src.domain.interfaces import AbstractUnitOfWork
from src.domain.use_cases.interfaces import ISendMessage


class SendMessage(ISendMessage):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user_id: uuid.UUID, message: str) -> None:
        async with self.uow:
            user = await self.uow.users.get_user(user_id)
            await user.send_message(message)
            await self.uow.commit()
