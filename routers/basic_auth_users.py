
# "Depends" manages if authentication is valid or not and what can the authenticated user do (permissions)

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

#OAuth2 is the authentication protocol to use (backend authentication standard)

# Las dos clases que importo: La primera para gestionar la autenticación y la segunda gestiona la forma en la que se va a enviar al backend (por el API) el usuario y contraseña
# Two classes imported: First one to manage the authentication and the second one manages the way user and password are going to be sent to the backend
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
router = APIRouter(prefix="/basicauth", 
                   tags=["basicauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"Not found"}})
# tokenUrl is the URL that manages authentication 
oauth2 = OAuth2PasswordBearer(tokenUrl="login")
# Start the server: uvicorn basic_auth_users:app --reload

# Separate object user that does not return the password, for safety
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

# Database user that has the password
class UserDB(User):
    password: str

# Users that would be theoretically in the database
users_db = {
    "eduhurtado":{
        "username":"eduhurtado",
        "full_name":"Eduardo Hurtado",
        "email":"ehurtado@gmail.com",
        "disabled":False,
        "password": "123456" # Passwords are normally encrypted for safety. See JWT file
    },

     "eduhl":{
        "username":"eduhl",
        "full_name":"Edu Hurtado",
        "email":"eduhl@hotmail.com",
        "disabled":True,
        "password": "654321" # Passwords are normally encrypted for safety. See JWT file
    }
}
# Search user operation
def search_user_db(username:str):
    if username in users_db:
        # ** means that different parameters can go here
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        # ** means that different parameters can go here
        return User(**users_db[username])

# Dependency criteria (to obtain the token)
async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    if user.disabled: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return user

# Authentication operation (POST)
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not correct")
    
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not correct")
    return{"access_token": user.username, "token_type":"bearer"} 

@router.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user
