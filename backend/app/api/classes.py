from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.class_group import ClassGroup, TeacherClass
from app.models.student import StudentClass
from app.models.teacher import Teacher
from app.schemas.class_group import ClassCreate, ClassInfo

router = APIRouter(prefix="/api/classes", tags=["班级"])


@router.get("", response_model=list[ClassInfo])
def list_classes(teacher: Teacher = Depends(get_current_user), db: Session = Depends(get_db)):
    links = (
        db.query(TeacherClass)
        .filter(TeacherClass.teacher_id == teacher.id)
        .all()
    )
    results = []
    for link in links:
        cls = link.class_group
        count = db.query(StudentClass).filter(StudentClass.class_id == cls.id).count()
        results.append(ClassInfo(id=cls.id, name=cls.name, grade=cls.grade, student_count=count))
    return results


@router.post("", response_model=ClassInfo, status_code=status.HTTP_201_CREATED)
def create_class(
    req: ClassCreate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cls = ClassGroup(name=req.name, grade=req.grade)
    db.add(cls)
    db.flush()
    db.add(TeacherClass(teacher_id=teacher.id, class_id=cls.id))
    db.commit()
    db.refresh(cls)
    return ClassInfo(id=cls.id, name=cls.name, grade=cls.grade)


@router.get("/{class_id}/students", response_model=list[int])
def get_class_student_ids(
    class_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    link = (
        db.query(TeacherClass)
        .filter(TeacherClass.teacher_id == teacher.id, TeacherClass.class_id == class_id)
        .first()
    )
    if not link:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="班级不存在或无权访问")
    rows = db.query(StudentClass).filter(StudentClass.class_id == class_id).all()
    return [r.student_id for r in rows]
