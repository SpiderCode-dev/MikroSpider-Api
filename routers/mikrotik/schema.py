from datetime import datetime
from pydantic import BaseModel


''' Model Schema Using Pydantic '''
class Mikrotik(BaseModel):
    ip: str
    user: str
    password: str
    port: int