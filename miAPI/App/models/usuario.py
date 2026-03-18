#modelo de validacion pydantic
From pydantic import BaseModel, Field

class usuario_create(BaseModel):
    id: int = Field(...,gt=0, description="Identificador de usuario")
    nombre: str = Field(..., min_length=3, max=50, example="Alexis")
    edad: int = Field(..., ge=1, le=123, description="Edad valida entre 1 - 123")
