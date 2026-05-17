import csv
import io
import os
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.database import get_db
from app.models.student import Student, StudentClass
from app.models.record import StudentRecord
from app.models.teacher import Teacher
from app.schemas.student import StudentClassInfo, StudentCreate, StudentInfo, StudentUpdate, StudentSearchResult, ImportResult

router = APIRouter(prefix="/api/students", tags=["学生"])

UPLOAD_DIR = Path(__file__).resolve().parent.parent.parent / "uploads" / "avatars"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _attach_classes(student, db):
    rows = (
        db.query(StudentClass)
        .filter(StudentClass.student_id == student.id)
        .all()
    )
    return [
        StudentClassInfo(id=r.class_group.id, name=r.class_group.name, grade=r.class_group.grade)
        for r in rows
    ]


def _student_to_info(student, db):
    info = StudentInfo.model_validate(student)
    info.classes = _attach_classes(student, db)
    return info


@router.get("/search", response_model=StudentSearchResult)
def search_students(
    q: str = Query("", min_length=0),
    class_id: int | None = None,
    gender: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
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
    if gender:
        query = query.filter(Student.gender == gender)

    total = query.count()
    students = query.order_by(Student.student_no).offset((page - 1) * page_size).limit(page_size).all()
    items = [_student_to_info(s, db) for s in students]
    return StudentSearchResult(items=items, total=total, page=page, page_size=page_size)


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
    return _student_to_info(student, db)


@router.get("/{student_id}", response_model=StudentInfo)
def get_student(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    return _student_to_info(student, db)


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
    return _student_to_info(student, db)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    # 清理头像文件
    if student.avatar:
        avatar_path = UPLOAD_DIR / student.avatar
        if avatar_path.exists():
            os.remove(avatar_path)
    db.delete(student)
    db.commit()


@router.post("/{student_id}/avatar", response_model=StudentInfo)
async def upload_avatar(
    student_id: int,
    file: UploadFile = File(...),
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")

    # 验证文件类型
    allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持 JPG/PNG/GIF/WebP 格式")

    # 删除旧头像
    if student.avatar:
        old_path = UPLOAD_DIR / student.avatar
        if old_path.exists():
            os.remove(old_path)

    # 保存新头像
    ext = file.filename.rsplit(".", 1)[-1] if "." in file.filename else "jpg"
    filename = f"avatar_{student_id}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = UPLOAD_DIR / filename
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="图片大小不能超过 5MB")
    with open(filepath, "wb") as f:
        f.write(content)

    student.avatar = filename
    db.commit()
    db.refresh(student)
    return _student_to_info(student, db)


@router.get("")
def list_all_students(
    class_id: int | None = Query(None),
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    if class_id is not None:
        sub = db.query(StudentClass.student_id).filter(StudentClass.class_id == class_id)
        query = query.filter(Student.id.in_(sub))
    students = query.order_by(Student.student_no).all()
    return [_student_to_info(s, db) for s in students]


@router.get("/export/csv")
def export_students_csv(
    class_id: int | None = Query(None),
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(Student)
    if class_id is not None:
        sub = db.query(StudentClass.student_id).filter(StudentClass.class_id == class_id)
        query = query.filter(Student.id.in_(sub))
    students = query.order_by(Student.student_no).all()

    output = io.StringIO()
    output.write("\ufeff")  # BOM for Excel
    writer = csv.writer(output)
    writer.writerow(["学号", "姓名", "性别", "出生日期", "联系电话", "家庭住址", "家长姓名", "家长电话", "备注", "档案记录数"])

    beijing_epoch = datetime(2026, 1, 1, tzinfo=timezone(timedelta(hours=8)))

    for s in students:
        record_count = db.query(StudentRecord).filter(StudentRecord.student_id == s.id).count()
        writer.writerow([
            s.student_no, s.name, s.gender, s.birth_date or "",
            s.phone, s.address, s.parent_name, s.parent_phone, s.notes, record_count
        ])

    content = output.getvalue()
    return Response(
        content=content.encode("utf-8-sig"),
        media_type="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=students.csv"},
    )


@router.post("/import", response_model=ImportResult)
async def import_students_csv(
    file: UploadFile = File(...),
    class_id: int = Query(...),
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="仅支持 CSV 文件")

    content = await file.read()
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = content.decode("gbk")

    reader = csv.DictReader(io.StringIO(text))
    success = 0
    failed = 0
    errors = []

    for row_num, row in enumerate(reader, start=2):
        student_no = row.get("学号", "").strip()
        name = row.get("姓名", "").strip()
        if not student_no or not name:
            failed += 1
            errors.append(f"第{row_num}行：学号或姓名为空")
            continue
        if db.query(Student).filter(Student.student_no == student_no).first():
            failed += 1
            errors.append(f"第{row_num}行：学号 '{student_no}' 已存在")
            continue

        try:
            birth_date = row.get("出生日期", "").strip() or None
            student = Student(
                student_no=student_no,
                name=name,
                gender=row.get("性别", "").strip(),
                birth_date=birth_date,
                phone=row.get("联系电话", "").strip(),
                address=row.get("家庭住址", "").strip(),
                parent_name=row.get("家长姓名", "").strip(),
                parent_phone=row.get("家长电话", "").strip(),
                notes=row.get("备注", "").strip(),
            )
            db.add(student)
            db.flush()
            db.add(StudentClass(student_id=student.id, class_id=class_id))
            success += 1
        except Exception as e:
            db.rollback()
            failed += 1
            errors.append(f"第{row_num}行：{str(e)}")

    db.commit()
    return ImportResult(success=success, failed=failed, errors=errors)


@router.get("/{student_id}/stats")
def get_student_stats(
    student_id: int,
    teacher: Teacher = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="学生不存在")
    records = db.query(StudentRecord).filter(StudentRecord.student_id == student_id).all()
    by_type = {}
    for r in records:
        by_type[r.record_type] = by_type.get(r.record_type, 0) + 1
    return {"total": len(records), "by_type": by_type}
