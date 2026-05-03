from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)
    name: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(default="", max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TeacherInfo(BaseModel):
    id: int
    username: str
    name: str
    phone: str

    model_config = {"from_attributes": True}
