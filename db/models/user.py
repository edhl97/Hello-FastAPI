from pydantic import BaseModel, Field 

class User(BaseModel):
    id: str | None = Field(default = None) # This means it is optional because the ID is unknwon. Instead, it is assigned by MongoDB. For MongoDB is "str" format, not "int"
    username: str
    email: str