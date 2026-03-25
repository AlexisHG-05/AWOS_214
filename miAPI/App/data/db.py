from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL=os.getenv(
    "DATABASE_URL",
    "postgresql://admin:123456@postgres:5432/DB_miapi"
    )

#2. Creamos el motor de la conecion a la base de datos, y la sesión local para manejar las transacciones
engine = create_engine(DATABASE_URL)
#3. Creamos gestionador de sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
    )

#4:Base declarativa para modelos 
Base = declarative_base()

#5.Funcion para la sesion de cada peticion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()