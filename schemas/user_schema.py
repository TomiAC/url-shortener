from pydantic import BaseModel, EmailStr

# Esquema para crear un usuario (entrada)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

# Esquema para devolver un usuario (salida)
class UserResponse(UserCreate):
    id: int

class UserLogin(BaseModel):
    email: str
    password: str