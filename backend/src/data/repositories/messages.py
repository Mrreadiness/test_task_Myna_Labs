import uuid

from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from src.data import message_table
from src.domain.entites import Message
from src.domain.types import Pagination
from src.domain.use_cases.interfaces import IMessagesRepository


class MessagesRepository(IMessagesRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_dialog_id(self, dialog_id: uuid.UUID, pagination: Pagination) -> list[Message]:
        query = (
            select(Message)
            .options(joinedload(Message.user))
            .select_from(message_table)
            .where(message_table.c.dialog_id == dialog_id)
            .order_by(desc(message_table.c.created))
            .limit(pagination.limit)
            .offset(pagination.offset)
        )
        return (await self.session.execute(query)).unique().scalars().all()
