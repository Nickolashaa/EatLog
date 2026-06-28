from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..services.users.service import UserService
from .session import get_session


async def get_user_service(session: AsyncSession = Depends(get_session)) -> UserService:
    return UserService(session)
