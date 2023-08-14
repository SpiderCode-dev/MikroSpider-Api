from fastapi import FastAPI, Depends
from routers.mikrotik import mikrotik
from config.database import Base, Session, engine
from routers.user import user_router
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.include_router(mikrotik, prefix="/mikrotik", tags=["mikrotik"], dependencies=[Depends(JWTBearer())])
app.include_router(user_router, prefix="/user", tags=["user"])

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
