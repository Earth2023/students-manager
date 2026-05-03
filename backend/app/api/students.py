from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.student import Student, StudentClass
from app.models.teacher import Teacher
from app.schemas.student import StudentCreate, StudentInfo, StudentUpdate

router = APIRouter(prefix="/api/students", tags=["学生"])


@router.get("/search", response_model=list[StudentInfo])
def search_students(
    q: str = Query("", min_length=1),
    class_id: int | None = None,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    if class_id is not None:
        sub = db.query(StudentClass.student_id).filter(StudentClass.class_id == class_id)
        query = query.filter(Student.id.in_(sub))
    if q:
        like = f"%{q}%"
        query = query.filter(
            Student.name.ilike(like) | Student.student_no.ilike(like)
        )
    return query.order_by(Student.student_no).limit(50).all()


@router.post("", response_model=StudentInfo, status_code=status.HTTP_201_CREATED)
def create_student(
    req: StudentCreate,
    class_id: int | None = Query(None),
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(Student).filter(Student.student_no == req.student_no).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="学号已存在")
    student = Student(**req.model_dump())
    db.add(student)
    db.flush()
    if class_id is not None:
        db.add(StudentClass(student_id=student.id, class_id=class_id))
    db.commit()
    db.refresh(student)
    return student


@router.get("/{student_id}", response_model=StudentInfo)
def get_student(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    return student


@router.put("/{student_id}", response_model=StudentInfo)
def update_student(
    student_id: int,
    req: StudentUpdate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    update_data = {k: v for k, v in req.model_dump().items() if v is not None}
    for key, value in update_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    db.delete(student)
    db.commit()
