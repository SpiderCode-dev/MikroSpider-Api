from fastapi import APIRouter, Depends
from fastapi import HTTPException
from models.user import User, Credentials
from fastapi.responses import HTMLResponse, JSONResponse
from config.jwt_manager import create_token
from config.database import Session
from middlewares.jwt_bearer import JWTBearer
from services.user import UserService

user_router = APIRouter()

@user_router.post("/login")
def login(user: Credentials):
    db = Session()
    result = UserService(db).get_user(user.email)
    if (result is None):
        raise HTTPException(status_code=404, detail="El usuario no existe")
    
    if (result.password != user.password):
        raise HTTPException(status_code=403, detail="Credenciales son invalidas")
    
    token: str = create_token(user.dict())
    return JSONResponse(status_code=200, content=token)
  

@user_router.post("/register", response_model=User, status_code=200, dependencies=[Depends(JWTBearer())])
def register(user: Credentials):
    return JSONResponse(status_code=200, content='hello')