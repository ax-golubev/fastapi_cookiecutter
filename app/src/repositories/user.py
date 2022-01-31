from sqlalchemy import delete, insert, select, update

import schemas
from database import db
from models.user import User
from repositories.exceptions import EntityDoesNotExist
from schemas import UserInDB

__all__ = ["user_get_by_id", "user_create", "user_update", "user_delete"]


async def user_get_by_id(user_id: int) -> schemas.UserInDB:
    statement = select(User).where(User.id == user_id)
    result = await db.session.execute(statement)
    try:
        user_row = result.first()[0]
        return UserInDB.from_orm(user_row)
    except TypeError:
        pass

    raise EntityDoesNotExist(
        "Пользователь с идентификатором {0} не найден.".format(user_id)
    )


async def user_create(
    first_name: str, last_name: str, email: str, is_superuser: bool = False
) -> schemas.UserInDB:
    statement = (
        insert(User)
        .values(
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_superuser=is_superuser,
        )
        .returning(User)
    )
    user_row = await db.session.execute(statement)
    await db.session.commit()
    return UserInDB.from_orm(user_row.first())


async def user_update(user_id: int, **kwargs) -> schemas.UserInDB:
    statement = update(User).where(User.id == user_id).values(**kwargs).returning(User)
    user_row = await db.session.execute(statement)
    await db.session.commit()
    return UserInDB.from_orm(user_row.first())


async def user_delete(user_id: int) -> None:
    statement = delete(User).where(User.id == user_id).returning(User.id)
    await db.session.execute(statement)
    await db.session.commit()
    return None
