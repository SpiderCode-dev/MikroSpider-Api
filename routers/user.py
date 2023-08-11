from fastapi import APIRouter
from fastapi import HTTPException
from models.user import User, Credentials
from fastapi.responses import HTMLResponse, JSONResponse
from config.jwt_manager import create_token

user = APIRouter()


@user.get("/", tags=['home'])
def massege():
    return HTMLResponse('<h1>Hello World!</h1>')


@user.post("/login", tags=['auth'])
def login(user: Credentials):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
  

@user.post("/upservice", tags=['auth'], response_model=User, status_code=200, dependencies=[Depends(JWTBearer())])
def upservice(user: Credentials):
    