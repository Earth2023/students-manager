from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.record import StudentRecord
from app.models.student import Student
from app.models.teacher import Teacher
from app.schemas.record import RECORD_TYPES, RecordCreate, RecordInfo, RecordUpdate

router = APIRouter(prefix="/api/students/{student_id}/records", tags=["档案记录"])
global_router = APIRouter(prefix="/api/records", tags=["档案记录"])


@router.get("", response_model=list[RecordInfo])
def list_records(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not db.query(Student).filter(Student.id == student_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    records = (
        db.query(StudentRecord)
        .filter(StudentRecord.student_id == student_id)
        .order_by(StudentRecord.created_at.desc())
        .all()
    )
    result = []
    for r in records:
        t = r.teacher
        result.append(
            RecordInfo(
                id=r.id,
                student_id=r.student_id,
                teacher_id=r.teacher_id,
                teacher_name=t.name if t else "",
                title=r.title,
                content=r.content,
                record_type=r.record_type,
                created_at=r.created_at,
            )
        )
    return result


@router.post("", response_model=RecordInfo, status_code=status.HTTP_201_CREATED)
def create_record(
    student_id: int,
    req: RecordCreate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not db.query(Student).filter(Student.id == student_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    if req.record_type not in RECORD_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"无效的记录类型，可选: {RECORD_TYPES}")
    record = StudentRecord(
        student_id=student_id,
        teacher_id=teacher.id,
        title=req.title,
        content=req.content,
        record_type=req.record_type,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return RecordInfo(
        id=record.id,
        student_id=record.student_id,
        teacher_id=record.teacher_id,
        teacher_name=teacher.name,
        title=record.title,
        content=record.content,
        record_type=record.record_type,
        created_at=record.created_at,
    )


@router.put("/{record_id}", response_model=RecordInfo)
def update_record(
    student_id: int,
    record_id: int,
    req: RecordUpdate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(StudentRecord)
        .filter(StudentRecord.id == record_id, StudentRecord.student_id == student_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    update_data = {k: v for k, v in req.model_dump().items() if v is not None}
    if "record_type" in update_data and update_data["record_type"] not in RECORD_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"无效的记录类型，可选: {RECORD_TYPES}")
    for key, value in update_data.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    teacher = record.teacher
    return RecordInfo(
        id=record.id,
        student_id=record.student_id,
        teacher_id=record.teacher_id,
        teacher_name=teacher.name if teacher else "",
        title=record.title,
        content=record.content,
        record_type=record.record_type,
        created_at=record.created_at,
    )


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    student_id: int,
    record_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = (
        db.query(StudentRecord)
        .filter(StudentRecord.id == record_id, StudentRecord.student_id == student_id)
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    db.delete(record)
    db.commit()


@global_router.put("/{record_id}", response_model=RecordInfo)
def update_record_global(
    record_id: int,
    req: RecordUpdate,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.query(StudentRecord).filter(StudentRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    update_data = {k: v for k, v in req.model_dump().items() if v is not None}
    if "record_type" in update_data and update_data["record_type"] not in RECORD_TYPES:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"无效的记录类型，可选: {RECORD_TYPES}")
    for key, value in update_data.items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    t = record.teacher
    return RecordInfo(
        id=record.id,
        student_id=record.student_id,
        teacher_id=record.teacher_id,
        teacher_name=t.name if t else "",
        title=record.title,
        content=record.content,
        record_type=record.record_type,
        created_at=record.created_at,
    )


@global_router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record_global(
    record_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = db.query(StudentRecord).filter(StudentRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="记录不存在")
    db.delete(record)
    db.commit()
