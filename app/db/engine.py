"""
Async engine for SqlAlchemy
"""
from typing import AsyncGenerator

from sqlalchemy.engine.url import URL
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine as _create_async_engine
)


def create_async_engine(url: URL | str) -> AsyncEngine:
    """
    Create async engine with constant params
    :param url:
    :return:
    """
    return _create_async_engine(url=url, echo=True, pool_pre_ping=True)


async def get_session_maker(engine: AsyncEngine) -> async_sessionmaker:
    """
    return async session maker
    :param engine:
    :return:
    """
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_sessionmaker() as session:
        yield session
