from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

#-- Modelos ---------------
class AspNetUsers(BaseModel):
    Id: str
    Email: Optional[str]
    EmailConfirmed: bool
    PasswordHash: str
    SecurityStamp: str
    PhoneNumber: Optional[str]
    PhoneNumberConfirmed: bool
    TwoFactorEnabled: bool
    LockoutEndDateUtc: Optional[datetime]
    LockoutEnabled: bool
    AccessFailedCount: int
    UserName: str

# -- Planes de Finaciacion
class Planes(BaseModel):
	id: int
	nombre: str
	cuotas: int
	interes: float
	costofin: float
	vencimento: datetime
	activo: bool

#-- Modelo de Vistas con ultinas 5 compras de una tarjeta
class Ultimas_Compras(BaseModel):
	fecha: datetime
	cupon: int = Field("Nro. cupon")
	idcomercio: int = Field("ID Comercion")
	comercio: str = Field("Nombre del Comercio")
	importe: float = Field("Importe")
	idplan: int = Field("ID PLan")
	id: int = Field("ID Compra")

#-- Vista con Detalle de Cuotas de la compra 
class Detalle_Cuotas(BaseModel):
	cuota: int
	vencimento: datetime
	importe: float
	liquidacion: int
