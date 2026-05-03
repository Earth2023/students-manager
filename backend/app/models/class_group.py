from sqlalchemy import ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ClassGroup(Base):
    __tablename__ = "class_groups"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(50), comment="班级名称，如 三年级一班")
    grade: Mapped[str] = mapped_column(String(20), default="", comment="年级")

    teacher_links = relationship("TeacherClass", back_populates="class_group", cascade="all, delete-orphan")
    student_links = relationship("StudentClass", back_populates="class_group", cascade="all, delete-orphan")


class TeacherClass(Base):
    __tablename__ = "teacher_classes"
    __table_args__ = (UniqueConstraint("teacher_id", "class_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(Integer, ForeignKey("teachers.id"))
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("class_groups.id"))

    teacher = relationship("Teacher", back_populates="class_links")
    class_group = relationship("ClassGroup", back_populates="teacher_links")
