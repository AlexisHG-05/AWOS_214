from fastapi import FastAPI
import asyncio
from typing import Optional

# Instancia del servidor
app = FastAPI(title="Mi primer API", 
              description="Esta es mi primera API con FastAPI",
              version="1.0.0")

# BD ficticia
usuarios = [
    {"id": 1, "nombre": "Juan", "Edad": 21},
    {"id": 2, "nombre": "Israel", "Edad": 21},
    {"id": 3, "nombre": "Sofi", "Edad": 21},
]

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API con FastAPI!"}

@app.get("/HolaMundo", tags=["Bienvenida Asincrona"])
async def hola():
    await asyncio.sleep(3)
    return {"mensaje": "Hola mundo FastAPI",
            "estatus" : "200"
            }

@app.get("/v1/usuario/{id}", tags=["Parametro obligatorio"])
async def consultauno(id: int):
    return {"Se encontro usuario": id}


@app.get("/v1/usuarios/", tags=["Parametro opcional"])
async def consultaTodos(id: Optional[int] = None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"] == id:
                return usuario


        return {"Mensaje": "usuario no encontrado", "usuario": id}
    else:
        return {"Mensaje": "¡No se proporciono id", "usuarios": usuarios}


 