from fastapi import APIRouter, HTTPException, status
from models.archivos import *
from conexion_db import Conexion
from typing import List 

router = APIRouter()

# -- Grabar Compras
def grabar_compra(compra: Compras):
    try:
        conexion = Conexion.get_connection()
        cursor = conexion.cursor()
        cursor.execute("exec grabarCompra ?, ?, ?, ?, ?, ?, ?, ?", 
                       [compra.idcomercio, compra.idtarjeta, compra.importe, compra.idplan, compra.cupon, compra.carga, compra.fecha, compra.autorizacion])
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
