from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from app.core.security import hash_password, verify_password
from app.core.deps import get_current_user
from app.database import get_db
from app.models.teacher import Teacher
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    TeacherInfo,
    ProfileUpdate,
    PasswordChange,
)
from app.core.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/register", response_model=TokenResponse)
def register(req: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(Teacher).filter(Teacher.username == req.username).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已存在")
    teacher = Teacher(
        username=req.username,
        hashed_password=hash_password(req.password),
        name=req.name,
        phone=req.phone,
    )
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    token = create_access_token({"sub": str(teacher.id)})
    return TokenResponse(access_token=token)


@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    teacher = db.query(Teacher).filter(Teacher.username == req.username).first()
    if not teacher or not verify_password(req.password, teacher.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = create_access_token({"sub": str(teacher.id)})
    return TokenResponse(access_token=token)


@router.get("/me", response_model=TeacherInfo)
def get_me(teacher: Teacher = Depends(get_current_user)):
    return teacher


@router.get("/profile", response_model=TeacherInfo)
def get_profile(teacher: Teacher = Depends(get_current_user)):
    return teacher


@router.put("/profile", response_model=TeacherInfo)
def update_profile(
    req: ProfileUpdate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if req.name is not None:
        teacher.name = req.name
    if req.phone is not None:
        teacher.phone = req.phone
    db.commit()
    db.refresh(teacher)
    return teacher


@router.put("/password")
def change_password(
    req: PasswordChange,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(req.old_password, teacher.hashed_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="原密码错误")
    teacher.hashed_password = hash_password(req.new_password)
    db.commit()
    return {"message": "密码修改成功"}
