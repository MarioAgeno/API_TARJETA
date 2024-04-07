from fastapi import APIRouter, HTTPException, status
from models.archivos import *
from conexion_db import Conexion
from datetime import datetime
#from typing import List 

router = APIRouter()

# Función para generar el código de autorización
def generar_codigo_autorizacion():
    fecha_actual = datetime.now()
    dia_juliano = fecha_actual.strftime("%j")
    fecha_hora_actual = fecha_actual.strftime("%Y%m%d%H%M%S")
    codigo_autorizacion = dia_juliano + fecha_hora_actual[-6:]
    return codigo_autorizacion

# -- Grabar Compras
def grabar_compra(compra: Compras):
    try:
        codigo_autorizacion = generar_codigo_autorizacion()  # Generar código de autorización
        conexion = Conexion.get_connection()
        cursor = conexion.cursor()
        cursor.execute("exec grabarCompra ?, ?, ?, ?, ?, ?, ?, ?", 
                       [compra.idcomercio, compra.idtarjeta, compra.importe, compra.idplan, compra.cupon, 'A', compra.fecha, codigo_autorizacion])
        conexion.commit()
        return {"message": "Compra grabada exitosamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

@router.post("/grabar_compra/", tags=['Registros de Compras'])
async def grabar_compra_tarjeta(compra: Compras):
    return grabar_compra(compra)


# -- Actualizar el Saldo de la Tarjeta
def actualizar_saldo_tarjeta(saldos_tarjeta: Saldo_Tarjeta):
    try:
        # Establecer conexión a la base de datos
        conexion = Conexion.get_connection()
        cursor = conexion.cursor()

        # Ejecutar el procedimiento almacenado
        cursor.execute("exec grabarSaldoTarj ?, ?", [saldos_tarjeta.id, saldos_tarjeta.importe])
        conexion.commit()

        return {"message": "Saldo de la tarjeta actualizado correctamente"}
    except Exception as e:
        # Manejo de errores
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Cerrar el cursor y la conexión
        cursor.close()
        conexion.close()

@router.put("/actualizar_saldo_tarjeta/", tags=['Tarjetas Asociados'])
async def actualizar_saldo(saldos_tarjeta: Saldo_Tarjeta):
    return actualizar_saldo_tarjeta(saldos_tarjeta)


# Función para grabar la compra y actualizar el saldo de la tarjeta
def grabar_compra_y_actualizar_saldo(compra: Compras, saldos_tarjeta: Saldo_Tarjeta):
    try:
        codigo_autorizacion = generar_codigo_autorizacion()  # Generar código de autorización
        conexion = Conexion.get_connection()
        cursor = conexion.cursor()

        # Ejecutar el procedimiento almacenado para grabar la compra
        cursor.execute("exec grabarCompra ?, ?, ?, ?, ?, ?, ?, ?", 
                       [compra.idcomercio, compra.idtarjeta, compra.importe, compra.idplan, compra.cupon, 'A', compra.fecha, codigo_autorizacion])
        conexion.commit()

        # Ejecutar el procedimiento almacenado para actualizar el saldo de la tarjeta
        cursor.execute("exec grabarSaldoTarj ?, ?", [compra.idtarjeta, compra.importe])
        conexion.commit()

        return {"message": "Compra grabada y saldo de la tarjeta actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        conexion.close()

@router.post("/grabar_compra_y_actualizar_saldo/", tags=['Registros de Compras'])
async def grabar_compra_y_actualizar_saldo_endpoint(compra: Compras, saldos_tarjeta: Saldo_Tarjeta):
    return grabar_compra_y_actualizar_saldo(compra, saldos_tarjeta)