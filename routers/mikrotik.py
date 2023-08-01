from fastapi import APIRouter
from fastapi import HTTPException

from .model import Mikrotik
from scripts.conexion_api_mikrotik import *

mikrotik = APIRouter()


@mikrotik.post("/test", status_code=201)
async def test(router: Mikrotik):
  status = test_conexion(router.ip, router.user, router.password, router.port)

  if (status == True):
    return {"message": "La conexión via api se ha realizado exitosamente."}
  else:
    raise HTTPException(status_code=400, detail="No se ha logrado conectar vía API, revisar la información ingresada por favor.")
  