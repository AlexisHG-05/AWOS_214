from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
import secrets

app = FastAPI(title="Control del GYM ", version="1.0.0")

security = HTTPBasic()

def verificar_acceso(credenciales: HTTPBasicCredentials = Depends(security)):
    user_ok = secrets.compare_digest(credenciales.username, "AlexisHG")
    pass_ok = secrets.compare_digest(credenciales.password, "123456")
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    return credenciales.username

class Miembro(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=3, max_length=50)
    edad: int = Field(..., ge=15, le=90)
    estado: str = Field(default="activo")

db_gym = [{"id": 1, 
         "nombre": "Alexis Hernandez",
         "edad": 20, 
         "estado": "activo"}]

@app.get("/v1/miembros/", tags=["Lectura"])
async def listar():
    return {"total": len(db_gym), "socios": db_gym}

@app.post("/v1/miembros/", status_code=status.HTTP_201_CREATED, tags=["Escritura"])
async def registrar(socio: Miembro, admin: str = Depends(verificar_acceso)):
    for s in db_gym:
        if s["id"] == socio.id:
            raise HTTPException(status_code=400, detail="El ID de socio ya existe")
    db_gym.append(socio.dict())
    return {"mensaje": f"Socio registrado por {admin}", "data": socio}

@app.put("/v1/miembros/{id}/baja", tags=["Logica"])
async def dar_baja(id: int, admin: str = Depends(verificar_acceso)):
    for s in db_gym:
        if s["id"] == id:
            if s["estado"] == "activo":
                s["estado"] = "inactivo"
                return {"mensaje": "Estatus actualizado a inactivo", "autorizado_por": admin}
            else:
                raise HTTPException(status_code=409, detail="El socio ya se encuentra inactivo")
    raise HTTPException(status_code=404, detail="Socio no encontrado")

@app.delete("/v1/miembros/{id}", tags=["Seguridad"])
async def eliminar(id: int, admin: str = Depends(verificar_acceso)):
    for s in db_gym:
        if s["id"] == id:
            db_gym.remove(s)
            return {"mensaje": f"Registro eliminado por admin: {admin}"}
    raise HTTPException(status_code=404, detail="No existe el registro")