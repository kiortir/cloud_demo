from typing import Literal
from enum import StrEnum

from pydantic import SecretStr, computed_field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class RuntimeType(StrEnum):
    DEV = "dev"
    PRODUCTION = "prod"
    MIGRATION = "migration"


class RuntimeConfig(BaseSettings):
    runtime: RuntimeType = RuntimeType.DEV


RUNTIME_CONFIG = RuntimeConfig()


def get_env_file():
    if RUNTIME_CONFIG.runtime == RuntimeType.DEV:
        return "../.db.env"

class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=get_env_file(), env_prefix="db_")

    host: str = "postgres"
    port: int = 5432
    username: str
    password: SecretStr
    db: str

    driver: str = "postgresql+asyncpg"

    @computed_field
    @property
    def dsn(self) -> str:
        host = self.host
        port = self.port
        username = self.username
        password = self.password
        db = self.db
        driver = self.driver
        return f"{driver}://{username}:{password.get_secret_value()}@{host}:{port}/{db}"
