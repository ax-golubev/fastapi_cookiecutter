import logging

from fastapi import APIRouter

from repositories import user_create, user_delete, user_get_by_id, user_update
from schemas import UserCreate, UserInDB, UserUpdate

router = APIRouter()

logger = logging.getLogger(__name__)


@router.get("/user/{user_id}", response_model=UserInDB)
async def get_user(
    user_id: int,
):
    """Получение пользователя по id."""
    return await user_get_by_id(user_id=user_id)


@router.post("/user/", response_model=UserInDB)
async def create_user(user_data: UserCreate):
    """Создание пользователя."""
    return await user_create(**user_data.dict())


@router.put("/user/{user_id}", response_model=UserInDB)
async def update_user(user_id: int, user_data: UserUpdate):
    """Обновление пользователя."""
    return await user_update(user_id, **user_data.dict())


@router.delete("/user/{user_id}")
async def delete_user(user_id: int):
    """Удаление пользователя."""
    await user_delete(user_id)
    return {}
