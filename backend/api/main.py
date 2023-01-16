from fastapi import FastAPI

from backend.container import container


def create_app() -> FastAPI:
    application = FastAPI(
        title=container.config.app.name(),
        root_path=container.config.app.root_path(),
        debug=container.config.app.debug(),
    )
    application.container = container
    return application


app = create_app()
