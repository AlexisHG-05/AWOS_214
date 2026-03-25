from fastapi import FastAPI
from App.routers import usuarios, varios
from App.data import usuario
from App.data.db import engine

usuario.Base.metadata.create_all(bind=engine) 

#instancia del servidor 
app = FastAPI(
    title="Mi primer API",
    description="Alexis Hernandez",
    version="1.0.0"
    )

app.include_router (usuarios.router)
app.include_router(varios.router)




