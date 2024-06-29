from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from settings import PostgresSettings


class Base(DeclarativeBase):
    pass


DB = PostgresSettings()  # type:ignore
engine = create_async_engine(DB.dsn, echo=True)


async def get_connection():
    global engine
    async with engine.connect() as con:
        yield con


__all__ = ("AsyncConnection", "get_connection", "Base")
