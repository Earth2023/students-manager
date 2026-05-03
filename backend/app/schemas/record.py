from datetime import datetime

from pydantic import BaseModel, Field

RECORD_TYPES = ["学业", "行为", "健康", "其他"]


class RecordCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    record_type: str = Field(default="其他")


class RecordUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=100)
    content: str | None = None
    record_type: str | None = None


class RecordInfo(BaseModel):
    id: int
    student_id: int
    teacher_id: int
    teacher_name: str = ""
    title: str
    content: str
    record_type: str
    created_at: datetime

    model_config = {"from_attributes": True}
