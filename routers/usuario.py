from fastapi import APIRouter, HTTPException, status
from models.archivos import *
from conexion_db import Conexion

router = APIRouter()

# buscar un usuario 
@router.get('/usuario/', tags=['Usuarios'])
def buscar_usuario(user_name: str):
    user_db = None
    try:
        with Conexion.get_connection() as conexion:
            with conexion.cursor() as cursor:
                sentenciaSQL = """
                    SELECT u.Id, u.Email, u.EmailConfirmed, u.PasswordHash, 
                        u.SecurityStamp, u.PhoneNumber, u.PhoneNumberConfirmed, 
                        u.TwoFactorEnabled, u.LockoutEndDateUtc, u.LockoutEnabled, 
                        u.AccessFailedCount, u.UserName
                    FROM AspNetUsers u
                    WHERE UserName = ?
                """
                cursor.execute(sentenciaSQL, (user_name,))
                user = cursor.fetchone()
                if user:
                    user_db = AspNetUsers(
                        Id=user[0],
                        Email=user[1],
                        EmailConfirmed=user[2],
                        PasswordHash=user[3],
                        SecurityStamp=user[4],
                        PhoneNumber=user[5],
                        PhoneNumberConfirmed=user[6],
                        TwoFactorEnabled=user[7],
                        LockoutEndDateUtc=user[8],
                        LockoutEnabled=user[9],
                        AccessFailedCount=user[10],
                        UserName=user[11]
                    )
                else:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Usuario no encontrado"
                    )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se pudo establecer la conexión con el servidor!"
        )
    finally:
        cursor.close()
        conexion.close()	
    return user_db