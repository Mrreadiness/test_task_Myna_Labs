from dependency_injector import containers, providers
from dependency_injector.containers import DeclarativeContainer
from src.config import Settings
from src.data.uow import UnitOfWork
from src.domain.use_cases.create_user import CreateUser
from src.domain.use_cases.send_message import SendMessage

app_config = Settings()


class Container(DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[app_config])
    wiring_config = containers.WiringConfiguration(packages=["src.api.routers"])

    uow: UnitOfWork = providers.Factory(UnitOfWork, dsn=config.database.dsn)
    create_user: CreateUser = providers.Factory(CreateUser, uow=uow)
    send_message: SendMessage = providers.Factory(SendMessage, uow=uow)


container = Container()
