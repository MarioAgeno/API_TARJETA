from pydantic import BaseModel, Field
from typing import Optional 

class Productos(BaseModel):
    id: Optional[int] = None
    nombre: str = Field(default="Producto Nuevo", min_length=5, max_length=20)
    precio: float = Field(default=0, ge=0, le=1000)
    stock: int = Field(default=0, gt=0)


    