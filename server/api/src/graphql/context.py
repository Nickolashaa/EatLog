from dataclasses import dataclass

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import BaseContext

from ..di.session import get_session
from ..di.users import get_user_service
from ..services.users import UserService


@dataclass(slots=True)
class Context(BaseContext):
    session: AsyncSession
    user_service: UserService


async def context_getter(
    session: AsyncSession = Depends(get_session),
    user_service: UserService = Depends(get_user_service),
) -> Context:
    return Context(
        session=session,
        user_service=user_service,
    )
