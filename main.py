from fastapi import FastAPI
from dotenv import load_dotenv
from routers.consultas import router as consultas_router
from routers.usuario import router as usuario_router

#-- Cargar las variables de entorno.
load_dotenv()

app = FastAPI()

@app.get('/')
def mensage():
    return 'API de consultas de compras con Tarjetas. MAASoft !!!'

app.include_router(consultas_router)
app.include_router(usuario_router)
