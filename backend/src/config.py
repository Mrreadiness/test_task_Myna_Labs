from typing import Any

from pydantic import AnyUrl, BaseSettings, validator


class EnvBaseSettings(BaseSettings):
    class Config:
        env_file = ".env"


class AppSettings(EnvBaseSettings):
    name: str = "Test Task Myna Labs"
    root_path: str = ""
    debug: bool = False

    class Config:
        env_prefix = "app_"


class PostgresDsn(AnyUrl):
    allowed_schemes = {"postgres", "postgresql", "asyncpg", "postgresql+asyncpg"}
    user_required = True


class PostgresConfig(EnvBaseSettings):
    scheme: str = "postgresql+asyncpg"
    host: str = "localhost"
    port: str = "5432"
    user: str = "postgres"
    password: str = "postgres"
    db: str = "postgres"
    dsn: PostgresDsn | None = None

    @validator("dsn", pre=True)
    def assemble_db_connection(cls, v: str | None, values: dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme=values.get("scheme"),
            user=values.get("user"),
            password=values.get("password"),
            host=values.get("host"),
            port=values.get("port"),
            path=f"/{values.get('db')}",
        )

    class Config:
        env_prefix = "postgres_"


class Settings(EnvBaseSettings):
    app: AppSettings = AppSettings()
    database: PostgresConfig = PostgresConfig()
