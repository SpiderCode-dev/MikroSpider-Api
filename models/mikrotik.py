from config.database import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from typing import Optional, List

# class MikrotikModel(Base):
#     __tablename__ = "mikrotik"
#     ip: Column(String, primary_key=True)
#     user: Column(String)
#     password: Column(String)
#     port: Column(Integer)
#     license_id: Column(Integer)

class Mikrotik(BaseModel):
    ip: str
    user: str
    password: str
    port: int
    license_id: Optional[int] = None