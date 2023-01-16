from dependency_injector import containers, providers
from dependency_injector.containers import DeclarativeContainer
from src.config import Settings

app_config = Settings()


class Container(DeclarativeContainer):
    config = providers.Configuration(pydantic_settings=[app_config])
    wiring_config = containers.WiringConfiguration(packages=["src.api.routers"])


container = Container()
