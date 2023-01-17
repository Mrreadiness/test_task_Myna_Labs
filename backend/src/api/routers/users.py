from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from src.api.schemas.users import SendMessageInSchema, UserInSchema, UserOutSchema
from src.domain.use_cases.interfaces import ICreateUser, ISendMessage

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
