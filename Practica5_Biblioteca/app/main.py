from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import List, Literal
from datetime import datetime

app = FastAPI(
    title="API Biblioteca Digital",
    description="Alexis Hernandez - Repaso General",
    version="1.0.0"
)

#  Modelos de Validación Pydantic
class Libro(BaseModel):
    id: int
    titulo: str = Field(..., min_length=2, max_length=100)
    autor: str
    anio: int = Field(..., gt=1450, le=datetime.now().year)
    paginas: int = Field(..., gt=1)
    # Estado restringido a disponible o prestado 
    estado: Literal["disponible", "prestado"] = "disponible" 

class Usuario(BaseModel):
    nombre: str = Field(..., min_length=1) 
    correo: EmailStr 

class Prestamo(BaseModel):
    libro_id: int
    usuario: Usuario
#Base de Datos Ficticia 
biblioteca = []
prestamos = []

#Endpoints 

#  Registrar un libro
@app.post("/libros/", status_code=status.HTTP_201_CREATED)
def registrar_libro(libro: Libro):
    for l in biblioteca:
        if l.id == libro.id:
            # 400 si el ID ya existe o datos inválidos 
            raise HTTPException(status_code=400, detail="El ID del libro ya existe")
    biblioteca.append(libro)
    return {"mensaje": "Libro registrado exitosamente", "libro": libro}

# Listar todos los libros 
@app.get("/libros/", response_model=List[Libro])
def listar_libros():
    return biblioteca

#  Buscar un libro por su nombre
@app.get("/libros/{nombre}")
def buscar_libro(nombre: str):
    resultados = [l for l in biblioteca if nombre.lower() in l.titulo.lower()]
    if not resultados:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return resultados

#  Registrar el préstamo de un libro 
@app.post("/prestamos/", status_code=status.HTTP_201_CREATED)
def registrar_prestamo(prestamo: Prestamo):
    for libro in biblioteca:
        if libro.id == prestamo.libro_id:
            if libro.estado == "prestado":
                # 409 si el libro ya está prestado 
                raise HTTPException(status_code=409, detail="El libro ya está prestado")
            
            libro.estado = "prestado"
            prestamos.append(prestamo)
            return {"mensaje": "Préstamo registrado"}
    
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Marcar un libro como devuelto 
@app.put("/libros/devolver/{libro_id}", status_code=status.HTTP_200_OK)
def devolver_libro(libro_id: int):
    for libro in biblioteca:
        if libro.id == libro_id:
            libro.estado = "disponible"
            global prestamos
            prestamos = [p for p in prestamos if p.libro_id != libro_id]
            return {"mensaje": "Libro devuelto exitosamente"}
    
    raise HTTPException(status_code=404, detail="Libro no encontrado")

# Eliminar el registro de un préstamo 
@app.delete("/prestamos/{libro_id}")
def eliminar_prestamo(libro_id: int):
    global prestamos  
    inicial = len(prestamos)
    prestamos = [p for p in prestamos if p.libro_id != libro_id]
    
    if len(prestamos) == inicial:
        # 409 si el registro de préstamo ya no exist
        raise HTTPException(status_code=409, detail="El registro de préstamo ya no existe")
    
    return {"mensaje": "Registro de préstamo eliminado"}