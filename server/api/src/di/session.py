from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from ..database.connection import session_maker


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
