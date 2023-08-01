from fastapi import FastAPI
from config.database import engine


''' FastAPI CONFIGURATION '''
app = FastAPI()


''' APP EVENT SETTING'''
@app.on_event("startup")
async def startup():
    await engine.connect()


@app.on_event("shutdown")
async def shutdown():
    await engine.disconnect()