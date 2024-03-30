from fastapi import FastAPI
from dotenv import load_dotenv
from routers.consultas import router as consultas_router
from routers.calculos import router as calcular_cuotas
from routers.grabaciones import router as grabaciones
from routers.usuario import router as usuario_router
from fastapi.responses import RedirectResponse

#-- Cargar las variables de entorno.
load_dotenv()

app = FastAPI()
app.title = "Tarjetas de Compras WebService. MAASoft !!!"

@app.get('/', tags=['Inicio'])
def mensage():
    return RedirectResponse(url="/docs")

app.include_router(consultas_router)
app.include_router(calcular_cuotas)
app.include_router(grabaciones)
app.include_router(usuario_router)
