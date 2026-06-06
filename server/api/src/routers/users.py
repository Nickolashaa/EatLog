from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from ..di.users import get_user_service
from ..schemas.users import UserInput, UserRegister, UserResponse
from ..services.exceptions import ObjectNotFound
from ..services.users.service import UserService

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}")
async def get_user(
    id: UUID, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get(id)
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/by-telegram/{telegram_id}")
async def get_user_by_telegram_id(
    telegram_id: int, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.get_by_telegram_id(telegram_id)
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
    input: UserInput, service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await service.create(
        telegram_id=input.telegram_id,
        gender=input.gender,
        weight=input.weight,
        height=input.height,
        age=input.age,
        goal=input.goal,
    )


@router.post("/register")
async def register_user(
    input: UserRegister, service: UserService = Depends(get_user_service)
) -> UserResponse:
    try:
        return await service.update(id=input.id, telegram_id=input.telegram_id)
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{id}")
async def update_user(
    id: UUID,
    input: UserInput,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        return await service.update(
            id=id,
            telegram_id=input.telegram_id,
            gender=input.gender,
            weight=input.weight,
            height=input.height,
            age=input.age,
            goal=input.goal,
        )
    except ObjectNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    id: UUID, service: UserService = Depends(get_user_service)
) -> None:
    await service.delete(id)
