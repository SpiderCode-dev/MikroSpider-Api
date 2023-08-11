from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from pydantic import BaseModel, Field

class UserModel(Base):
    __tablename__ = "users"
    id: Column(Integer, primary_key=True, increment=True)
    role: Column(Integer)
    user: Column(String)
    password: Column(String)
    created_at: Column(DateTime)
    token: Column(String)
    token_expires: Column(DateTime)

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