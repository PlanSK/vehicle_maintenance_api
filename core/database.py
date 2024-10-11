from asyncio import current_task
from typing import AsyncGenerator, AsyncIterator

from loguru import logger
from sqlalchemy.exc import DatabaseError, IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

from .config import settings


class DatabaseHandler:
    def __init__(self, url: str, echo: bool):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
        self.scoped_session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )

    async def get_db(self) -> AsyncIterator[AsyncSession]:
        session = self.scoped_session()
        if session is None:
            raise Exception("Database session manager is not initialized.")
        try:
            yield session
        except DatabaseError as e:
            await session.rollback()
            logger.error(f"Database error. Exception: {e}")
            raise
        except Exception as e:
            await session.rollback()
            logger.debug(f"General unhandled exception: {e}")
            raise
        finally:
            await session.close()


db_handler = DatabaseHandler(url=settings.db.url, echo=settings.db.echo)
