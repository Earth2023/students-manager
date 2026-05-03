from pydantic import BaseModel, Field


class ClassCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    grade: str = Field(default="", max_length=20)


class ClassInfo(BaseModel):
    id: int
    name: str
    grade: str
    student_count: int = 0

    model_config = {"from_attributes": True}
