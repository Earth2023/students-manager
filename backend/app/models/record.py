from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class StudentRecord(Base):
    __tablename__ = "student_records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"))
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id"))
    title: Mapped[str] = mapped_column(String(100), comment="记录标题")
    content: Mapped[str] = mapped_column(Text, comment="记录内容")
    record_type: Mapped[str] = mapped_column(
        String(20), default="其他", comment="记录类型: 学业/行为/健康/其他"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc), comment="创建时间"
    )

    student = relationship("Student", back_populates="records")
    teacher = relationship("Teacher")
