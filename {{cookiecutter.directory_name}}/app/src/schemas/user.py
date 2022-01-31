from pydantic import BaseModel

__all__ = ["UserCreate", "UserUpdate", "UserInDBBase", "UserInDB"]


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    is_superuser: bool

    class Config:
        orm_mode = True


# Properties to return to client
class UserInDB(UserInDBBase):
    pass
