from fastapi import FastAPI
from routers.productos import router as productos_router

app = FastAPI()


@app.get('/')
def mensage():
    return 'Prueba de FASTApi !!'


app.include_router(productos_router)