from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    role: Mapped[int]= mapped_column(Integer)
    user: Mapped[str]= mapped_column(String)
    password: Mapped[str]= mapped_column(String)
    created_at: Mapped[str]= mapped_column(DateTime)
    token: Mapped[str]= mapped_column(String)
    token_expires: Mapped[str]= mapped_column(DateTime)

class User(BaseModel):
    id: int
    role: int
    user: str
    password: str
    created_at: str
    token: str
    token_expires: str

class Credentials(BaseModel):
    user: str
    password: str