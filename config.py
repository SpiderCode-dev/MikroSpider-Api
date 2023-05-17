from fastapi import FastAPI
import databases
import sqlalchemy


''' FastAPI CONFIGURATION '''
app = FastAPI()


''' DATABASE CONNECTION '''

# OJO: TENER CUIDADO CON ESTA INFORMACION
DATABASE_URL = "postgresql://spider:y46zp12x05s10m2ueui2@134.209.73.129:5432/mikro"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(
    DATABASE_URL
)


''' APP EVENT SETTING'''
@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()