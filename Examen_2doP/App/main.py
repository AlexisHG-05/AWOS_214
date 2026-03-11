from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel, Field
import secrets

app = FastAPI(title="Sistema de tickets de soporte técnico")
security = HTTPBasic()
def verificar_acceso(credenciales: HTTPBasicCredentials = Depends(security)):
    user_ok = secrets.compare_digest(credenciales.username, "soporte")
    pass_ok = secrets.compare_digest(credenciales.password, "4321")
    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    return credenciales.username
# Definición del modelo de datos para un ticket :nombre,descripcion,prioridad,estado
class Ticket(BaseModel):
    Nombre: str = Field(min_length=5)
    Descripcion: str = Field(...,min_length=20, max_length=200)
    Prioridad: str = Field(before="Alta", pattern="^(Alta|Media|Baja)$")
    Estado: str = Field(default="pendiente")
bdtickets = [
    Ticket(Nombre="Problema con la impresora", Descripcion="La impresora no responde al comando de impresión y muestra un mensaje de error.", Prioridad="Alta"),
    Ticket(Nombre="Error en el software de contabilidad", Descripcion="El software de contabilidad se cierra inesperadamente al intentar generar un informe financiero.", Prioridad="Media"),
    Ticket(Nombre="Falla en la conexión a Internet", Descripcion="La conexión a Internet es intermitente y se desconecta varias veces al día, afectando la productividad.", Prioridad="Baja")
]


#endpoint para crear un ticket
@app.post("/v1/tickets", status_code=status.HTTP_201_CREATED)
def crear_ticket(ticket: Ticket, username: str = Depends(verificar_acceso)):
    bdtickets.append(ticket)
    return ticket

# Enpoint para listar tickets
@app.get("/v1/tickets", tags=["Tickets"])
def listar_ticket(username: str = Depends(verificar_acceso)):
    return {"total": len(bdtickets), "tickets": bdtickets}

#Endpoint para consultar un ticket por su nombre
@app.get("/v1/tickets/{nombre}", tags=["Tickets"])
def consultar_ticket(nombre: str, username: str = Depends(verificar_acceso)):    
    for ticket in bdtickets:
        if ticket.Nombre == nombre:
            return ticket
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
#Endpoint para cambiar estado de un ticket
@app.put("/v1/tickets/{nombre}/estado", tags=["Tickets"])
def cambiar_estado_ticket(nombre: str, nuevo_estado: str = Field(..., pattern="^(pendiente|en proceso|resuelto)$"), username: str = Depends(verificar_acceso)):
    for ticket in bdtickets:
        if ticket.Nombre == nombre:
            ticket.Estado = nuevo_estado
            return ticket
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")

#endpoint para eliminar un ticket
@app.delete("/v1/tickets/{nombre}", status_code=status.HTTP_204_NO_CONTENT)    
def eliminar_ticket(nombre: str, username: str = Depends(verificar_acceso)):
    global bdtickets
    bdtickets = [ticket for ticket in bdtickets if ticket.Nombre != nombre]
    return {
        "detail": "Ticket eliminado"    
    }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ticket no encontrado")
        

