from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class Licence(Base):
    __tablename__ = "licencia"
    id: Column(Integer, primary_key=True, increment=True)
    user_id: Column(Integer)
    plan: Column(String)
    domain: Column(String)
    valid: Column(Boolean)
    created_at: Column(DateTime)
    end_at: Column(DateTime)