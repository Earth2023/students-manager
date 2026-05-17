from datetime import datetime, timezone, timedelta

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


def beijing_now() -> datetime:
    """返回带 UTC+8 时区的当前时间"""
    return datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=8)


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
        DateTime, default=beijing_now, comment="创建时间 (UTC+8)"
    )

    student = relationship("Student", back_populates="records")
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True, onupdate=beijing_now, comment="最后更新时间 (UTC+8)"
    )

    teacher = relationship("Teacher")
