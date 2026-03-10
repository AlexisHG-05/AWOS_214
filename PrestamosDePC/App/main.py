from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
import secrets

app = FastAPI(title="Prestamo Equipos", version="1.0.0")

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

class Equipo(BaseModel):
    id: int = Field(..., gt=0)
    marca: str = Field(..., min_length=2, max_length=50)
    modelo: str = Field(..., min_length=2)
    estado: str = Field(default="disponible") # disponible o prestado

# BD Ficticia inicial
db_equipos = [{"id": 1, "marca": "Dell", "modelo": "Latitude", "estado": "disponible"}]

# --- ENDPOINTS ---

@app.get("/v1/equipos/", tags=["Lectura"])
async def listar():
    return {"total": len(db_equipos), "equipos": db_equipos}

@app.post("/v1/equipos/", status_code=status.HTTP_201_CREATED, tags=["Escritura"])
async def registrar(item: Equipo, admin: str = Depends(verificar_acceso)):
    for e in db_equipos:
        if e["id"] == item.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    db_equipos.append(item.dict())
    return {"mensaje": "Equipo registrado", "autorizado_por": admin}

@app.put("/v1/equipos/{id}/prestar", tags=["Lógica"])
async def realizar_prestamo(id: int, admin: str = Depends(verificar_acceso)):
    for e in db_equipos:
        if e["id"] == id:
            if e["estado"] == "disponible":
                e["estado"] = "prestado"
                return {"mensaje": "Prestamo exitoso", "responsable": admin}
            else:
                # Error de conflicto si ya está ocupada
                raise HTTPException(status_code=409, detail="El equipo ya se encuentra prestado")
    raise HTTPException(status_code=404, detail="Equipo no encontrado")

@app.delete("/v1/equipos/{id}", tags=["Seguridad"])
async def eliminar(id: int, admin: str = Depends(verificar_acceso)):
    for e in db_equipos:
        if e["id"] == id:
            db_equipos.remove(e)
            return {"mensaje": f"Equipo {id} eliminado por {admin}"}
    raise HTTPException(status_code=404, detail="ID no encontrado")