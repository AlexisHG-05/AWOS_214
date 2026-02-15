#Importamos la imagen base
FROM python:3.12-slim

#Crear carpeta del contenedor 
WORKDIR /app

#Copiar requerimientos del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#Copiar el proyecto
COPY ./App ./app
#Exponemos el puerto
EXPOSE 5000

#Comandos 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5000"]