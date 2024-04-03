from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from routers.consultas import router as consultas_router
from routers.calculos import router as calcular_cuotas
from routers.grabaciones import router as grabaciones
from routers.usuario import router as usuario_router
import os

#-- Cargar las variables de entorno.
load_dotenv()

# Obtener el token de las variables de entorno
token_lectura = os.getenv("TOKEN")

app = FastAPI()
security = HTTPBearer()
app.title = "Tarjetas de Compras WebService. MAASoft !!!"

## Middleware para validar el token en rutas protegidas
async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials:
        if credentials.scheme == "Bearer":
            token = credentials.credentials
            # Aquí puedes realizar cualquier validación adicional del token si es necesario
            if token != token_lectura:
                raise HTTPException(status_code=403, detail="Token de acceso no válido.")
    else:
        # Si no se proporciona un encabezado de autorización, permitir el acceso
        return

# Ruta personalizada para la documentación
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentación")

# Ruta personalizada para la especificación OpenAPI
@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return JSONResponse(get_openapi(title="API Documentation", version="1.0.0", routes=app.routes))


@app.get('/', tags=['Inicio'])
async def mensage():
    return 'http://www.maasoft.com.ar'
app.include_router(consultas_router, dependencies=[Depends(validate_token)])
app.include_router(calcular_cuotas, dependencies=[Depends(validate_token)])
app.include_router(grabaciones, dependencies=[Depends(validate_token)])
app.include_router(usuario_router, dependencies=[Depends(validate_token)])
