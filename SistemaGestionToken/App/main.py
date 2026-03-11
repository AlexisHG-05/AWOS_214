from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import JWTError, jwt
import secrets

# Configuración JWT (Práctica de Seguridad Avanzada)
SECRET_KEY = "mi_llave_secreta_para_el_examen"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Examen - Seguridad JWT Total", version="2.0.0")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- LÓGICA DE TOKENS ---
def crear_token(data: dict):
    copia_data = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    copia_data.update({"exp": expira})
    return jwt.encode(copia_data, SECRET_KEY, algorithm=ALGORITHM)

async def validar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="No se pudo validar el token")

# --- MODELOS ---
class Usuario(BaseModel):
    id: int
    username: str
    rol: str

db_usuarios = [{"id": 1, "username": "AlexisHG", "rol": "Admin"}]

# --- ENDPOINTS ---

# 1. Ruta para obtener el Token (LOGIN)
@app.post("/token", tags=["Seguridad"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Validación simple de tus prácticas
    if form_data.username == "AlexisHG" and form_data.password == "123456":
        token = crear_token(data={"sub": form_data.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=400, detail="Usuario o contraseña incorrectos")

# 2. GET: Protegido (Solo si tienes el Token)
@app.get("/v1/usuarios/", tags=["CRUD Protegido"])
async def listar(user: str = Depends(validar_token)):
    return {"ejecutado_por": user, "lista": db_usuarios}

# 3. POST: Protegido
@app.post("/v1/usuarios/", tags=["CRUD Protegido"])
async def crear(nuevo: Usuario, user: str = Depends(validar_token)):
    db_usuarios.append(nuevo.dict())
    return {"mensaje": "Usuario creado", "admin": user}

# 4. DELETE: Protegido
@app.delete("/v1/usuarios/{id}", tags=["CRUD Protegido"])
async def borrar(id: int, user: str = Depends(validar_token)):
    for u in db_usuarios:
        if u["id"] == id:
            db_usuarios.remove(u)
            return {"mensaje": f"Borrado por {user}"}
    raise HTTPException(status_code=404, detail="No encontrado")