from fastapi import APIRouter, HTTPException, status
from models.archivos import *
from conexion_db import Conexion
from typing import List 

router = APIRouter()

# Leer todos los planes de pagos
@router.get('/planes', response_model=List[Planes], tags=['Planes de pagos'])
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
@router.get('/planes/', tags=['Planes de pagos'])
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
@router.get('/compras/', response_model=List[Ultimas_Compras], tags=['Registros de Compras'])
def ultimas_compras(id_tarjeta: int = 'ID Tarjeta'):
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
							idplan = row[5],
							id = row[6]
						)
						ultimas_compras_db.append(ultimas_compras_list)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return ultimas_compras_db

# Obtener las cuotas de una compra segun ID de Compras
@router.get('/cuotas/', response_model=List[Detalle_Cuotas], tags=['Registros de Compras'])
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


