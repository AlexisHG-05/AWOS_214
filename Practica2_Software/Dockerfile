# Importamos la Imagen base (Práctica 3)
FROM python:3.12-slim

# Crear carpeta del contenedor
WORKDIR /app

# Copiar requerimientos e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el proyecto
COPY ./App /app/app

# Exponemos el puerto definido en tus prácticas
EXPOSE 5000

# Comando para iniciar el servidor con reload activo
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1000", "--reload"]