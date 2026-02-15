#Importaciones
from fastapi import FastAPI, status, HTTPException
import asyncio 
from typing import Optional 

#Instacia 
app = FastAPI(
    title='Mi primer API',
     description='Alexis Hernandez',
     version='1.0.0'
     )
#TB ficticia 
usuarios=[
    {"id":1,"nombre":"Juan Carlos","edad":23},
    {"id":2,"nombre":"America","edad":20},
    {"id":3,"nombre":"Sofi","edad":19},
]

#Endpoinst
@app.get("/", tags=['Inicio'])
async def bienvenida():
    return {"mensaje": "¡Bienvenido de mi API!"}

@app.get("/HolaMundo", tags=['Bienvenida Asincrona'])
async def hola():
    await asyncio.sleep(4) #Simulacion de una peticion
    return{
        "mensaje": "¡Hola mundo FastAPI!",
        "estatus": "200"
    }

@app.get("/v1/parametroOb/{id}", tags=['Parametro Obligatorio'])
async def consultaUno(id:int):
    return {"Se encontro usuario": id}

@app.get("/v1/parametroOp/", tags=['Parametro opcional'])
async def consultaTodos(id: Optional[int]= None):
    if id is not None:
        for usuario in usuarios:
            if usuario["id"]== id: 
                return{"mensaje":"usuario encontrado", "usuario": usuario}
        return{"mensaje":"usuario no encontrado", "usuario": id}
    else:
        return{"mensaje":"No se proporciono id"}


@app.get("/v1/usuarios/", tags=['CRUD HTTP'])
async def leer_usuarios():
    return{
        "status":"200",
        "total": len(usuarios), 
        "usuarios":usuarios
    }


@app.post("/v1/usuarios/", tags=['CRUD HTTP'],status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuario:dict):
    for usr in usuarios:
        if usr["id"] == usuario.get("id"):
            raise HTTPException(
                status_code=400,
                detail="El id ya existe"
            )
    usuarios.append(usuario)
    return{
        "mensaje":"Usuario Agregado",
        "Usuario":usuario
    }

@app.put("/v1/usuarios/", tags=['CRUD HTTP'])
async def actualizar_usuario(usuario: dict):
    found = False
    for index, usr in enumerate(usuarios):
        if usr["id"] == usuario.get("id"):
            usuarios[index] = usuario  
            found = True
            return {
                "mensaje": "Usuario Actualizado Correctamente",
                "usuario": usuario
            }
    if not found:
        raise HTTPException(
            status_code=404,
            detail="El usuario con ese ID no existe"
        )

# --- Endpoint para ELIMINAR ---
@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'])
async def eliminar_usuario(id: int):
    # Buscamos el usuario por su ID
    for index, usr in enumerate(usuarios):
        if usr["id"] == id:
            usuarios.pop(index) # Lo sacamos de la lista
            return {
                "mensaje": "Usuario Eliminado Correctamente",
                "id_eliminado": id
            }
    
    # Si no lo encontramos
    raise HTTPException(
        status_code=404,
        detail="El usuario no existe, no se puede eliminar"
    )
