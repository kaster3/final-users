from pathlib import Path
from typing import Literal

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_PATH = Path(__file__).parent.parent.parent

class ApiV1Prefix(BaseModel):
    endpoint: str = "/endpoint"
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/user"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path[1:]

class AccessToken(BaseModel):
    lifetime_seconds: int
    reset_password_token_secret: str
    verification_token_secret: str


class JWTToken(BaseModel):
    lifetime_seconds: int
    algorithm: str = "RS256"
    private_key: Path = BASE_PATH / "certs" / "jwt-private.pem"
    public_key: Path = BASE_PATH / "certs" / "jwt-public.pem"


class LoggingConfig(BaseModel):
    log_level: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str


class DataBase(BaseModel):
    url: PostgresDsn
    echo: bool
    echo_pool: bool
    pool_size: int
    max_overflow: int

class Redis(BaseModel):
    url: str
    ttl: int


class GunicornConfig(BaseModel):
    host: str
    port: int
    workers: int
    timeout: int


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_PATH / ".template.env",
            BASE_PATH / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI__",
    )
    gunicorn: GunicornConfig
    db: DataBase
    logging: LoggingConfig
    access_token: AccessToken
    jwt_token: JWTToken
    redis: Redis
    api: ApiPrefix = ApiPrefix()


settings = Settings()
