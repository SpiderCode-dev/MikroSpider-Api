from fastapi import FastAPI
from config.database import engine
from routers.mikrotik import mikrotik


''' FastAPI CONFIGURATION '''
app = FastAPI()



app.include_router(mikrotik, prefix="/api/mikrotik", tags=["mikrotik"])

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
