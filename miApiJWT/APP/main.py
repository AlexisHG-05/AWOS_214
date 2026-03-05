from fastapi import FastAPI, status, HTTPException, Depends
import asyncio
from typing import Optional
from pydantic import BaseModel, Field
# Cambiamos HTTPBasic por las herramientas de OAuth2 y JWT
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
 # Configuracion de seguridad
SECRET_KEY = "Alexis_ Hernandez_Gutierrez_UPQ" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Límite máximo de 30 minutos

# Definimos el esquema donde se buscará el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# instancia del servidor 
app = FastAPI(

    title="Mi API con JWT",
    description="Alexis Hernandez - Práctica OAuth2 + JWT",
    version="2.0.0"
    
)

# BD ficticia
usuarios=[
    {"id": 1, "nombre":"Juan", "edad" :23 },
    {"id": 2, "nombre":"Diego", "edad" :23 },
    {"id": 3, "nombre":"Jose", "edad" :19 },
    {"id": 4, "nombre":"Jafet", "edad" :14 },
    {"id": 5, "nombre":"Alexis", "edad" :39 },
    {"id": 6, "nombre":"Juan p", "edad" :23 },
]

# modelo de validacion pydantic
class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max_length=50, example="Alexis")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")

# Funciones para manejo de JWT
#  Configuraciones y  Generación de Tokens
def crear_token_acceso(data: dict):
    datos_a_cifrar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos_a_cifrar.update({"exp": expiracion})
    return jwt.encode(datos_a_cifrar, SECRET_KEY, algorithm=ALGORITHM)

#  Implementar validación de tokens
async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    credenciales_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token o ha expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credenciales_exception
        return username
    except JWTError:
        raise credenciales_exception

# Endpoint para obtener el ticket de acceso (login)
@app.post("/token", tags=["Autenticación"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validación de credenciales manuales
    if form_data.username != "AlexisHG" or form_data.password != "123456":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos"
        )
    
    token = crear_token_acceso(data={"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


# ENDPOINTS

@app.get("/", tags=["Inicio"])
async def bienvenida():
    return {"mensaje" : "¡Bienvenido a mi API con JWT!"}

@app.get("/HolaMundo" ,tags=["Bienvenida Asincrona"])
async def hola():
    await asyncio.sleep(4)
    return {"mensaje" : "¡Hola mundo FastAPI! ", "estatus": "200"}

@app.get("/v1/usuarios/", tags=["CRUD HTTP"])
async def leer_usuarios():
    return {
        "status":"200",
        "total": len(usuarios),
        "usuarios":usuarios
    }

# Protección de endpoints PUT y DELETE

@app.put("/v1/usuarios/{id_buscado}", tags=["CRUD HTTP"])
async def actualizar_usuario(
    id_buscado: int, 
    datos_nuevos: dict, 
    user_auth: str = Depends(obtener_usuario_actual)
):
    for usr in usuarios:
        if usr["id"] == id_buscado:
            usr.update(datos_nuevos)
            return {
                "mensaje": f"Usuario actualizado por {user_auth}",
                "usuario": usr
            }
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")  

@app.delete("/v1/usuarios/{id}", tags=['CRUD HTTP'], status_code=status.HTTP_200_OK)
async def eliminar_usuario(
    id: int, 
    user_auth: str = Depends(obtener_usuario_actual) #
):
    for usuario in usuarios:
        if usuario["id"] == id:
            usuarios.remove(usuario)
            return {
                "mensaje": f"Usuario eliminado por: {user_auth}" 
            }
    raise HTTPException(status_code=400, detail="Usuario no encontrado")