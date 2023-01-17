from fastapi import FastAPI
from src.api.routers import users
from src.container import container


def create_app() -> FastAPI:
    application = FastAPI(
        title=container.config.app.name(),
        root_path=container.config.app.root_path(),
        debug=container.config.app.debug(),
    )
    application.include_router(users.router, tags=["User"])
    return application


app = create_app()
