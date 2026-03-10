from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
import secrets

# Instancia del servidor
app = FastAPI(title="Inventario Hardware", version="1.0.0")

# Seguridad HTTP Basic
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

# Modelo de Pydantic
class Hardware(BaseModel):
    id: int = Field(..., gt=0)
    nombre: str = Field(..., min_length=2, max_length=100)
    precio: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)

inventario = [{"id": 1, "nombre": "Monitor Gamer", "precio": 4200.0, "stock": 5}]

# --- ENDPOINTS ---

@app.get("/v1/productos/", tags=["Lectura"])
async def listar_productos():
    return {"productos": inventario}

@app.post("/v1/productos/", status_code=status.HTTP_201_CREATED, tags=["Escritura"])
async def registrar_producto(item: Hardware, admin: str = Depends(verificar_acceso)):
    for p in inventario:
        if p["id"] == item.id:
            raise HTTPException(status_code=400, detail="El ID ya existe")
    inventario.append(item.dict())
    return {"mensaje": f"Registrado por {admin}", "data": item}

@app.put("/v1/productos/{id}/venta", tags=["Lógica"])
async def realizar_venta(id: int, admin: str = Depends(verificar_acceso)):
    for p in inventario:
        if p["id"] == id:
            if p["stock"] > 0:
                p["stock"] -= 1
                return {"mensaje": f"Venta exitosa por {admin}", "stock": p["stock"]}
            else:
                raise HTTPException(status_code=409, detail="Producto agotado")
    raise HTTPException(status_code=404, detail="Producto no encontrado")

@app.delete("/v1/productos/{id}", tags=["Seguridad"])
async def eliminar_producto(id: int, admin: str = Depends(verificar_acceso)):
    for p in inventario:
        if p["id"] == id:
            inventario.remove(p)
            return {"mensaje": f"Eliminado por {admin}"}
    raise HTTPException(status_code=404, detail="No existe")