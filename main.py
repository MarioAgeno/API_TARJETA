from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
from dotenv import load_dotenv
from conexion_db_c import Conexion
from typing import List


#-- Cargar las variables de entorno.
load_dotenv()

app = FastAPI()

#-- Modelos ---------------
class AspNetUsers(BaseModel):
    Id: str
    Email: str
    EmailConfirmed: bool
    PasswordHash: str
    SecurityStamp: str
    PhoneNumber: str
    PhoneNumberConfirmed: bool
    TwoFactorEnabled: bool
    LockoutEndDateUtc: datetime
    LockoutEnabled: bool
    AccessFailedCount: int
    UserName: str

class Planes(BaseModel):
	id: int
	nombre: str
	cuotas: int
	interes: float
	costofin: float
	vencimento: datetime
	activo: bool

#-- MOdelo de Vistas
class Ultimas_Compras(BaseModel):
	fecha: datetime
	cupon: int
	idcomercio: int
	comercio: str
	importe: float
	idplan: int

class Detalle_Cuotas(BaseModel):
	cuota: int
	vencimento: datetime
	importe: float
	liquidacion: int


@app.get('/')
def mensage():
    return 'Prueba de FASTApi y MAASoft !!'

# Leer todos los planes de pagos
@app.get('/planes', response_model=List[Planes])
def leer_planes():
	planes_db = []
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'SELECT * FROM tjPlanes'
				cursor.execute(sentenciaSQL)
				plan = cursor.fetchall()
				if plan:
					for row in plan:
						plan_list = Planes(
							id = row[0],
							nombre = row[1],
							cuotas = row[2],
							interes = row[3],
							costofin = row[4],
							vencimento = row[5],
							activo = row[6]
						)
						planes_db.append(plan_list)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return planes_db

# Buscar un plan de pagos segun su ID
@app.get('/planes/')
def buscar_plan(id_plan: int):
	planes_db = None
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'SELECT * FROM tjPlanes WHERE id = ?'
				cursor.execute(sentenciaSQL, id_plan)
				plan = cursor.fetchone()
				if plan:
					planes_db = Planes(
						id = plan[0],
						nombre = plan[1],
						cuotas = plan[2],
						interes = plan[3],
						costofin = plan[4],
						vencimento = plan[5],
						activo = plan[6]
					)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return planes_db


# Leer ultimas 5 compras con una tarjeta
@app.get('/compras/', response_model=List[Ultimas_Compras])
def ultimas_compras(id_tarjeta: int):
	ultimas_compras_db = []
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'EXEC UltComprasSocios_App ?'
				cursor.execute(sentenciaSQL, id_tarjeta)
				compras = cursor.fetchall()
				if compras:
					for row in compras:
						ultimas_compras_list = Ultimas_Compras(
							fecha = row[0],
							cupon = row[1],
							idcomercio = row[2],
							comercio = row[3],
							importe = row[4],
							idplan = row[5]
						)
						ultimas_compras_db.append(ultimas_compras_list)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return ultimas_compras_db

# Obtener las cuotas de una compra segun ID de Compras
@app.get('/cuotas/', response_model=List[Detalle_Cuotas])
def detalle_cuotas(id_compra: int):
	detalle_cuotas_db = []
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'EXEC DetalleCuotas_App ?'
				cursor.execute(sentenciaSQL, id_compra)
				cuotas = cursor.fetchall()
				if cuotas:
					for row in cuotas:
						cuotas_list = Detalle_Cuotas(
							cuota = row[0],
							vencimento = row[1],
							importe = row[2],
							liquidacion = row[3]
						)
						detalle_cuotas_db.append(cuotas_list)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return detalle_cuotas_db


# buscar un usuario 
def search_user(username: str):
	user_db = None
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = """
					SELECT u.UserName, u.PhoneNumber, u.Email, u.PasswordHash, u.Id, u.SecurityStamp
						FROM AspNetUsers u
						WHERE UserName = ?
				"""
				cursor.execute(sentenciaSQL, username)
				user = cursor.fetchone()
				
				if user:
					user_db = AspNetUsers(
						UserName=user[0],
						PhoneNumber=user[1],
						Email=user[2],
						PasswordHash=user[3],
						Id=user[4],
						SecurityStamp=user[5]
					)
	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
					
	return user_db