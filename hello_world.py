from fastapi import FastAPI

app = FastAPI()

# Start the server: uvicorn hello_world:app --reload
# hello_world is the file name, app is the instance and -- reload is to refresh the server continously in response to any change in the code
# Stop the server: CTRL+C

@app.get("/")
async def root():
    return {"Hello world"}

# Local Url: http://127.0.0.1:8000

@app.get("/message")
async def message():
    return {"message":"Hello world"}

# Local URL: http://127.0.0.1:8000/message

# Swagger documentation: http://127.0.0.1:8000/docs
# Redocly documentation: http://127.0.0.1:8000/redoc
