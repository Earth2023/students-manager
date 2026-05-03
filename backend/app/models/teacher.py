from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, comment="登录用户名")
    hashed_password: Mapped[str] = mapped_column(String(255), comment="密码哈希")
    name: Mapped[str] = mapped_column(String(50), comment="教师姓名")
    phone: Mapped[str] = mapped_column(String(20), default="", comment="联系电话")

    # 多对多：教师 ↔ 班级
    class_links = relationship("TeacherClass", back_populates="teacher", cascade="all, delete-orphan")
