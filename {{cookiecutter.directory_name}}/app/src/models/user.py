from sqlalchemy import Boolean, Column, Integer, String

from models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(256), nullable=True)
    last_name = Column(String(256), nullable=True)
    email = Column(String, index=True, nullable=False)
    is_superuser = Column(Boolean, default=False)
