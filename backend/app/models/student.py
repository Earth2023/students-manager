from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_no: Mapped[str] = mapped_column(String(30), unique=True, index=True, comment="学号")
    name: Mapped[str] = mapped_column(String(50), comment="姓名")
    gender: Mapped[str] = mapped_column(String(10), default="", comment="性别")
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True, comment="出生日期")
    phone: Mapped[str] = mapped_column(String(20), default="", comment="联系电话")
    address: Mapped[str] = mapped_column(String(255), default="", comment="家庭住址")
    parent_name: Mapped[str] = mapped_column(String(50), default="", comment="家长姓名")
    parent_phone: Mapped[str] = mapped_column(String(20), default="", comment="家长电话")
    notes: Mapped[str] = mapped_column(Text, default="", comment="备注")
    avatar: Mapped[str] = mapped_column(String(255), default="", comment="头像文件名")

    class_links = relationship("StudentClass", back_populates="student", cascade="all, delete-orphan")
    records = relationship("StudentRecord", back_populates="student", cascade="all, delete-orphan")


class StudentClass(Base):
    __tablename__ = "student_classes"
    __table_args__ = (UniqueConstraint("student_id", "class_id"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey("students.id"))
    class_id: Mapped[int] = mapped_column(Integer, ForeignKey("class_groups.id"))

    student = relationship("Student", back_populates="class_links")
    class_group = relationship("ClassGroup", back_populates="student_links")
