# JWT (Json web token) is an encrypted authentication 

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Typical encrypt algorith
ALGORITHM = "HS256"
# Limit duration for token authentication (minutes)
ACCESS_TOKEN_DURATION = 1
# Random secret password that can be passed to jwt.encode 
# openssl rand -hex 32
SECRET = "5giwefr7234oit674931207fhh98fg32"

router = APIRouter(prefix="/jwtauth", 
                   tags=["jwtauth"],
                   responses={status.HTTP_404_NOT_FOUND: {"message":"Not found"}})
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Start local server: uvicorn jwt_auth_users:app --reload


crypt = CryptContext(schemes="bcrypt")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "eduhurtado":{
        "username":"eduhurtado",
        "full_name":"Eduardo Hurtado",
        "email":"ehurtado@gmail.com",
        "disabled":False,
        # Encrypt with an online bcrypt hash generator. Each time you encrypt is different
        "password": "$2a$12$9tDwhJYvEPl.gMWVHUHaS.2wf37nz2nTeE5Jok8dubMxCTo6osG5O" 
    },

     "eduhl":{
        "username":"eduhl",
        "full_name":"Edu Hurtado",
        "email":"eduhl@hotmail.com",
        "disabled":True,
        # Encrypt with an online bcrypt hash generator. Each time you encrypt is different
        "password": "$2a$12$nFs.38ST6i/k.KuOZF/L0uBJMPvCoiBXKMMXhzalrFHrqC/QZOxQG" 
    }
}

def search_user_db(username:str):
    if username in users_db:
        # ** means that different parameters can go here
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        # ** means that different parameters can go here
        return User(**users_db[username])

# Token validation process
async def auth_user(token: str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    try: 
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
        
    except JWTError:
        raise exception
    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not correct")
    
    user = search_user_db(form.username)

    # Comparison of login password (normal) and database password (encrypted) 
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not correct")
    
    # Secure authentication with a pre-defined duration limit
    # This access_token is un JSON because the method is JWT. Then I encrypt it. 
    access_token = {"sub":user.username, "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    return{"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type":"bearer"} 

@router.get("/users/me")
async def me(user: User= Depends(current_user)):
    return user
