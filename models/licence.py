from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from pydantic import BaseModel, Field
from sqlalchemy.orm import Mapped, mapped_column

class LicenceModel(Base):
    __tablename__ = "licencia"
    id: Mapped[int]= mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int]= mapped_column(Integer)
    plan: Mapped[str]= mapped_column(String)
    domain: Mapped[str]= mapped_column(String)
    valid: Mapped[bool]= mapped_column(Boolean)
    created_at: Mapped[str]= mapped_column(DateTime)
    end_at: Mapped[str]= mapped_column(DateTime)

class Licence(BaseModel):
    id: int
    user_id: int
    plan: str
    domain: str
    valid: bool
    created_at: str
    end_at: str