from fastapi import APIRouter, Path

from models.productos import Productos

router = APIRouter()

productos = [
    {
        "id": 1,
        "nombre": "papas",
        "precio": 123,
        "stock": 4
    },
    {
        "id": 2,
        "nombre": "zanahorias",
        "precio": 250,
        "stock": 8
    },
    {
        "id": 3,
        "nombre": "tomates",
        "precio": 350,
        "stock": 12
    }
]

@router.get('/productos')
def leer_productos():
    return productos

# parametros de ruta
@router.get('/productos')
def leer_productos():
    return productos

# parametros de ruta con filtro
@router.get('/productos/{id}')
def leer_producto(id: int = Path(gt=0)):
    return list(filter(lambda item: item['id'] == id, productos))

# parametros Query 
@router.get('/productos/')
def leer_productos_by_stock(stock: int):
    return list(filter(lambda item: item['stock'] == stock, productos))

# Agregar productos metodo post
@router.post('/productos')
def crear_productos(producto: Productos):
    productos.append(producto)
    return productos

# Modificar productos metodo put
@router.put('/productos/{id}')
def modifico_producto(id: int, producto: Productos):
    for index, item in enumerate(productos):
        if item['id'] == id:
            productos[index]['nombre'] = producto.nombre            
            productos[index]['stock'] = producto.stock
            productos[index]['precio'] = producto.precio
    return productos

# Eliminar Productos metodo delete
@router.delete('/productos/{id')
def borrar_producto(id: int):
    for item in productos:
        if item['id'] == id:
            productos.remove(item)
    return productos

