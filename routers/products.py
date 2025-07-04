from fastapi import APIRouter

# Prefix is used to short the path in the operations of the file, so all of them should be /products... 
# Tag is to allow documentation to group the operations of this file 
# Responses is for errors
router = APIRouter(prefix="/products", 
                   tags=["products"],
                   responses={404: {"message":"Not found"}})

products_list= ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]

@router.get("/")
async def products():
    return products_list

@router.get("/{id}")
async def products(id:int):
    return products_list[id]
