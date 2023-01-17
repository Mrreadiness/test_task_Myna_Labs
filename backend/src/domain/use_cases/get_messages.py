import uuid

from src.domain.entites import Message
from src.domain.interfaces import AbstractUnitOfWork
from src.domain.types import Pagination
from src.domain.use_cases.interfaces import IGetMessages


class GetMessages(IGetMessages):
    def __init__(self, uow: AbstractUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, user_id: uuid.UUID, pagination: Pagination) -> list[Message]:
        async with self.uow:
            user = await self.uow.users.get_user(user_id)
            return await self.uow.messages.get_by_dialog_id(user.dialog.id, pagination)
