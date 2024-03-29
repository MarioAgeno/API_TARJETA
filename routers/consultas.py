from fastapi import APIRouter, HTTPException, status
from models.archivos import *
from conexion_db import Conexion
from typing import List 

router = APIRouter()

# Leer todos los Estados 
@router.get('/estados', response_model=List[Estados], tags=['Estado de Tarjetas'])
def leer_estados():
	estados_db = []
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'SELECT id, nombre FROM tjEstados'
				cursor.execute(sentenciaSQL)
				tabla = cursor.fetchall()
				if tabla:
					for row in tabla:
						estado_list = Estados(
							id = row[0],
							nombre = row[1]
						)
						estados_db.append(estado_list)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return estados_db

# Buscar un Estados de Tarjeta segun su ID
@router.get('/estados/', tags=['Estado de Tarjetas'])
def buscar_estado(id_estado: int):
	estado_db = None
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = 'SELECT * FROM tjEstados WHERE id = ?'
				cursor.execute(sentenciaSQL, id_estado)
				registro = cursor.fetchone()
				if registro:
					estado_db = Estados(
						id = registro[0],
						nombre = registro[1]
					)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return estado_db


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

# Buscar los planes habilitados de un Comercio
@router.get('/planesComercios/', response_model=List[Planes_Comercios], tags=['Planes de pagos'])
def planes_comercios(id_comercio: int):
	planes_db	= []
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = '''
							select * from tjPlanes where tjPlanes.id in 
							(select idPlan from tjPlanComercio where idComercio=?) and tjPlanes.activo = 1 
							and tjPlanes.vencimiento >= getdate()
							'''
				cursor.execute(sentenciaSQL, id_comercio)
				registros = cursor.fetchall()
				if registros:
					for row in registros:
						ultimas_compras_list = Planes_Comercios(
							id = row[0],
							nombre = row[1],
							cuotas = row[2],
							interes = row[3],
							costofin = row[4]
						)
						planes_db.append(ultimas_compras_list)

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


# Buscar un Comercio segun su ID
@router.get('/comercios/', tags=['Registros de Compras'])
def buscar_comercio(id_comercio: int):
	comercio_db = None
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = '''
				SELECT id, pin, comercio, nombre, domicilio, localidad, provincia, mail, sucursal, socio, cuit
					FROM tjComercios WHERE id = ?
				'''
				cursor.execute(sentenciaSQL, id_comercio)
				registro = cursor.fetchone()
				if registro:
					comercio_db = Comercios(
						id = registro[0],
						pin = registro[1],
						comercio = registro[2],
						nombre = registro[3],
						domicilio = registro[4],
						localidad = registro[5],
						provincia = registro[6],
						mail = registro[7],
						sucursal = registro[8],
						socio = registro[9],
						cuit = registro[10]
					)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return comercio_db

# Buscar una Tarjeta segun su ID
@router.get('/tarjetas/', tags=['Tarjetas Asociados'])
def buscar_tarjeta(id_tarjeta: int = 'ID Tarjeta'):
	tarjeta_db = None
	try:
		with Conexion.get_connection() as conexion:
			with conexion.cursor() as cursor:
				sentenciaSQL = '''
				SELECT id, sucursal, socio, adicional, verificador, nombre, domicilio, localidad, provincia, mail, tope, saldo, estado, baja, vencimiento 
					from tjTarjetas WHERE id = ?
				'''
				cursor.execute(sentenciaSQL, id_tarjeta)
				registro = cursor.fetchone()
				if registro:
					tarjeta_db = Tarjetas(
						id = registro[0],
						sucursal = registro[1],
						socio = registro[2],
						adicional = registro[3],
						verificador = registro[4],
						nombre = registro[5],
						domicilio = registro[6],
						localidad = registro[7],
						provincia = registro[8],
						mail = registro[9],
						tope = registro[10],
						saldo = registro[11],
						estado = registro[12],
						baja = registro[13],
						vencimento = registro[14]
					)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail="No se pudo establecer la conexión con el servidor!"
		)
						
	return tarjeta_db

