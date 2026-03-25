from fastapi import status, HTTPException, Depends, APIRouter
from App.data.database import usuarios
from App.data.database import usuarios
from App.security.auth import verificar_Peticion
from App.models.usuario import usuario_create

from sqlalchemy.orm import Session
from App.data.db import get_db
from App.data.usuario import Usuario as usuarioDB 


router = APIRouter(
    prefix="/v1/usuarios", tags=["CRUD HTTP"]
)

#Endpoins de usuarios, para el CRUD completo
@router.get("/")
async def leer_usuarios(db:Session= Depends(get_db)):

    queryUsers= db.query(usuarioDB). all()
    
    return{
        "status":"200",
        "total": len(queryUsers),
        "usuarios":queryUsers
    }

@router.post("/",status_code=status.HTTP_201_CREATED)
async def crear_usuario(usuarioP:usuario_create, db:Session= Depends(get_db)):

    nuevoUsuario = usuarioDB(
        id=usuarioP.id,
        nombre=usuarioP.nombre,
        edad=usuarioP.edad
    )
    db.add(nuevoUsuario)
    db.commit()
    db.refresh(nuevoUsuario)

    return{
        "mensaje":"Usuario agregado",
        "Usuario":usuarioP
    }

@router.put("/{id_buscado}",status_code=status.HTTP_200_OK, tags=["CRUD HTTP"])
async def actualizar_usuario(id_buscado: int, datos_nuevos: dict):
    for usr in usuarios:
        if usr["id"] == id_buscado:
            usr.update(datos_nuevos)
            return {
                "mensaje": "Usuario actualizado",
                "usuario": usr
            }
        
    raise HTTPException(
        status_code=404,
        detail="Usuario no encontrado"
    )  

@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def eliminar_usuario(id:int, userAuth:str= Depends(verificar_Peticion)):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return{
                "mensaje": f"Usuario eliminado por :{userAuth}" 
            }
    raise HTTPException(
        status_code=400, 
        detail="Usuario no encontrado"
    )