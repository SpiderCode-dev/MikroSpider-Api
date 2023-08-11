import os
# Crea el motor de base de datos de sqlite
from sqlalchemy import create_engine
# Crear una sesión para enlazar la base de datos
from sqlalchemy.orm.session import sessionmaker
# Permite manejar los modelos de datos
from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "../database.sqlite"
base_dir = os.path.dirname(os.path.realpath(__file__))

database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"
engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=engine)

Base = declarative_base()