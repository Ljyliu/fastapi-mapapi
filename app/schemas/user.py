from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    username: str = Field(..., min_length=5, max_length=20,examples=["testuser", "john_doe" ])
    password: str = Field(..., min_length=8, max_length=128, examples=["P@ssw0rd!", "my_password" ])
    email: EmailStr


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    model_config = { "from_attributes": True }