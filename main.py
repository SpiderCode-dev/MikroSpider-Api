from fastapi import FastAPI
from routers.mikrotik import mikrotik
from config.database import Base, Session, engine
from models.user import UserModel
from models.mikrotik import MikrotikModel
from models.licence import LicenceModel

app = FastAPI()
app.include_router(mikrotik, prefix="/api/mikrotik", tags=["mikrotik"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Welcome to SpiderMikrotik API"}


# ''' APP EVENT SETTING'''
# @app.on_event("startup")
# async def startup():
#     await engine.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await engine.disconnect()
