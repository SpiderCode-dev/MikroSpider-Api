from config.database import Base
from sqlalchemy import Column, Integer, String

class Mikrotik(Base):
    __tablename__ = "mikrotik"
    ip: Column(String, primary_key=True)
    user: Column(String)
    password: Column(String)
    port: Column(Integer)
    license_id: Column(Integer)