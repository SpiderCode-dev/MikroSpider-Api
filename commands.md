Prepara el entorno virtual usando el modulo venv
python -m venv venv

Carga en la terminal el entorno virtual creado
source venv/bin/activate

Instalar los paquetes principales
pip install fastapi // Modulo de FastAPI
pip install uvicorn // Modulo para inicializar 
pip install pyjwt // Modulo de JSON Web Tokens
pip install sqlalchemy


Ejecutar el servidor de desarrollo
uvicorn main:app --reload --port 5000 --host 0.0.0.0
reload: sirve como hot reloading
port: usa el puerto para servir la aplicacion
host: 0.0.0.0 sera el puerto para usar en la red local