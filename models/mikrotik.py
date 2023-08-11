from config.database import Base
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column

class MikrotikModel(Base):
    __tablename__ = "mikrotik"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    ip: Mapped[str] = mapped_column(String, nullable=False)
    user: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    port: Mapped[int] = mapped_column(Integer)
    license_id: Mapped[int] = mapped_column(Integer)

class Mikrotik(BaseModel):
    ip: str
    user: str
    password: str
    port: int
    license_id: Optional[int] = None