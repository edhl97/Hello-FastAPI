from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(jwt_auth_users.router)
app.include_router(basic_auth_users.router)
app.include_router(users_db.router)


# Static resources
app.mount("/static", StaticFiles(directory="static"), name="static")

# Start the server: uvicorn main:app --reload
# Stop the server: CTRL+C
# Local URL: http://127.0.0.1:8000

@app.get("/")
async def root():
    return {"Hello world"}