from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    role: Mapped[int]= mapped_column(Integer)
    token: Mapped[str]= mapped_column(String)
    email: Mapped[str]= mapped_column(String)
    password: Mapped[str]= mapped_column(String)
    created_at: Mapped[str]= mapped_column(String)
    token_expires: Mapped[str]= mapped_column(String)

class User(BaseModel):
    id: Optional[int] = None
    role: int
    email: str
    password: str
    created_at: Optional[str] = None
    token: Optional[str] = None
    token_expires: Optional[str] = None

class Credentials(BaseModel):
    email: str
    password: str