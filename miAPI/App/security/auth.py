from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
from fasapi import Depends, HTTPSException, status

#Seguridad HTTP basic
security= HTTPBasic()

def verificar_Peticion(credenciales:HTTPBasicCredentials=Depends(security)):
    userAuth = secrets.compare_digest(credenciales.username, "AlexisHG")
    passAuth = secrets.compare_digest(credenciales.password, "123456")
    if not (userAuth and passAuth):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    return credenciales.username 
