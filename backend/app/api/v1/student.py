from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.database import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse, StudentListResponse

router = APIRouter(prefix="/students", tags=["学生管理"])


@router.get("/", response_model=StudentListResponse)
def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    college: Optional[str] = None,
    major: Optional[str] = None,
    province: Optional[str] = None,
    employment_status: Optional[str] = None,
    grade: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Student)

    # 筛选条件
    if college:
        query = query.filter(Student.college == college)
    if major:
        query = query.filter(Student.major == major)
    if province:
        query = query.filter(Student.province == province)
    if employment_status:
        query = query.filter(Student.employment_status == employment_status)
    if grade:
        query = query.filter(Student.grade == grade)

    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return StudentListResponse(total=total, page=page, page_size=page_size, items=items)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="学生不存在")
    return student


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    # 检查学号唯一性
    existing = db.query(Student).filter(Student.student_id == student.student_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="学号已存在")

    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, student: StudentUpdate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="学生不存在")

    for key, value in student.model_dump(exclude_unset=True).items():
        setattr(db_student, key, value)

    db.commit()
    db.refresh(db_student)
    return db_student


@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="学生不存在")

    db.delete(db_student)
    db.commit()
    return None