from fastapi import FastAPI
from src.api.routers import users
from src.container import container
from src.domain.exceptions import BaseDomainException
from starlette.requests import Request
from starlette.responses import JSONResponse


def create_app() -> FastAPI:
    application = FastAPI(
        title=container.config.app.name(),
        root_path=container.config.app.root_path(),
        debug=container.config.app.debug(),
    )
    application.include_router(users.router, tags=["User"])
    return application


app = create_app()


@app.exception_handler(BaseDomainException)
async def unicorn_exception_handler(request: Request, exc: BaseDomainException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.message},
    )
