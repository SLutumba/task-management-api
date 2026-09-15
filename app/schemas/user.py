from pydantic import BaseModel, EmailStr, Field

class RegisterUserRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)

class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)