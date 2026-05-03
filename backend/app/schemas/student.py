from datetime import date

from pydantic import BaseModel, Field


class StudentCreate(BaseModel):
    student_no: str = Field(..., min_length=1, max_length=30)
    name: str = Field(..., min_length=1, max_length=50)
    gender: str = Field(default="", max_length=10)
    birth_date: date | None = None
    phone: str = Field(default="", max_length=20)
    address: str = Field(default="", max_length=255)
    parent_name: str = Field(default="", max_length=50)
    parent_phone: str = Field(default="", max_length=20)
    notes: str = Field(default="", max_length=500)


class StudentUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=50)
    gender: str | None = Field(default=None, max_length=10)
    birth_date: date | None = None
    phone: str | None = Field(default=None, max_length=20)
    address: str | None = Field(default=None, max_length=255)
    parent_name: str | None = Field(default=None, max_length=50)
    parent_phone: str | None = Field(default=None, max_length=20)
    notes: str | None = Field(default=None, max_length=500)


class StudentInfo(BaseModel):
    id: int
    student_no: str
    name: str
    gender: str
    birth_date: date | None = None
    phone: str
    address: str
    parent_name: str
    parent_phone: str
    notes: str

    model_config = {"from_attributes": True}
