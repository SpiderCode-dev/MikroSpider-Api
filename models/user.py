from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class User(Base):
    __tablename__ = "users"
    id: Column(Integer, primary_key=True, increment=True)
    role: Column(Integer)
    user: Column(String)
    password: Column(String)
    created_at: Column(DateTime)
    token: Column(String)
    token_expires: Column(DateTime)