# HTTPException is to import error codes
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# BaseModel allows us to manage users

router = APIRouter()

# Start the server: uvicorn users:app --reload
# User entity
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

# Theoretical users of the database
users_list = [User(id=1, name="Edu", surname="Hurtado", url="https://hurtado.edu", age=27),
         User(id=2, name="Juan", surname="Lopez", url="https://juanlopez.com", age=35),
         User(id=3, name="Ramon", surname="Dahlberg", url="https://ramdahlberg.com", age=33)]

@router.get("/users")
async def users():
    return users_list

# This function can be anywhere
def search_user(id:int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error":"No se ha encontrado el usuario"}
#Path
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

# Query
@router.get("/userquery/")
async def user(id: int):
    return search_user(id)

# Adding users, with if/else type check that the user does not already exist. status_code next to the path, allows me to change 200 OK that would return by default
# Añadir usuarios, con comprobación tipo if/else de que el usuario no exista. El status_code al lado del path, me permite cambiar el 200 OK que saldría por defecto
# response_model is to see in the documentation that if this goes right an user type object is returned

@router.post("/user/", response_model=User, status_code=201)
async def user(user:User):
    if type(search_user(user.id)) ==User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    else: 
        users_list.append(user)
        return user

# Complete user update, to update only a part of it we would use patch. 
@router.put("/user/")
async def user(user:User):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
                users_list[index] = user
                found =True
    if not found:
        return {"error":"No se ha actualizado el usuario"}
    else:
        return user

# Delete user. With id is enough. Since the id is mandatory, it is passed in the path
@router.delete("/user/{id}")
async def user(id:int):
    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
                del users_list[index]
                found =True
    if not found:
        return {"error":"No se ha aliminado el usuario"}
                
   