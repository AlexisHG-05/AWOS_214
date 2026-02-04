from fastapi import FastAPI
import asyncio


app = FastAPI()
@app.get("/")
async def bienvenida():
    return {"mensaje": "Bienvenido a mi API con FastAPI!"}

    @app.get("/Hola mundo")
    async def hola():
        await asycio.sleep(4)
        return {"mensaje": "Hola munedo FastAPI",
          "estatus" : "200"
          }