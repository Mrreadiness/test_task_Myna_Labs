import uuid

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Query
from pydantic import parse_obj_as
from src.api.schemas.users import MessageOutSchema, SendMessageInSchema, UserInSchema, UserOutSchema
from src.domain.types import Pagination
from src.domain.use_cases.interfaces import ICreateUser, IGetMessages, ISendMessage

router = APIRouter()


@router.post("/")
@inject
async def create_user(
    in_schema: UserInSchema,
    use_case: ICreateUser = Depends(Provide["create_user"]),
) -> UserOutSchema:
    return UserOutSchema.from_orm(await use_case(in_schema.username))


@router.post("/send_message")
@inject
async def send_message(
    in_schema: SendMessageInSchema,
    use_case: ISendMessage = Depends(Provide["send_message"]),
) -> None:
    await use_case(in_schema.user_id, in_schema.message)


@router.get("/{user_id}/messages")
@inject
async def get_messages(
    user_id: uuid.UUID,
    limit: int = Query(10, le=100),
    offset: int = Query(0),
    use_case: IGetMessages = Depends(Provide["get_messages"]),
) -> list[MessageOutSchema]:
    results = await use_case(user_id, Pagination(limit=limit, offset=offset))
    return parse_obj_as(list[MessageOutSchema], results)
