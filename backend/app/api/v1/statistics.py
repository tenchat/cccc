from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.student import Student

router = APIRouter(prefix="/statistics", tags=["统计"])


@router.get("/summary")
def get_summary(db: Session = Depends(get_db)):
    total = db.query(func.count(Student.id)).scalar()
    employed = db.query(func.count(Student.id)).filter(Student.employment_status == 1).scalar()
    unemployed = db.query(func.count(Student.id)).filter(Student.employment_status == 0).scalar()
    further_study = db.query(func.count(Student.id)).filter(Student.employment_status == 2).scalar()
    abroad = db.query(func.count(Student.id)).filter(Student.employment_status == 3).scalar()

    return {
        "total": total,
        "employed": employed,
        "unemployed": unemployed,
        "further_study": further_study,
        "abroad": abroad,
        "employment_rate": round(employed / total * 100, 2) if total > 0 else 0
    }


@router.get("/by-college")
def get_by_college(db: Session = Depends(get_db)):
    results = db.query(
        Student.college,
        func.count(Student.id).label("total"),
        func.sum(Student.employment_status).label("employed")
    ).group_by(Student.college).all()

    return [{"college": r[0], "total": r[1], "employed": r[2] or 0} for r in results]


@router.get("/by-major")
def get_by_major(db: Session = Depends(get_db)):
    results = db.query(
        Student.major,
        Student.college,
        func.count(Student.id).label("total"),
        func.sum(Student.employment_status).label("employed")
    ).group_by(Student.major, Student.college).all()

    return [{
        "major": r[0],
        "college": r[1],
        "total": r[2],
        "employed": r[3] or 0
    } for r in results]


@router.get("/by-province")
def get_by_province(db: Session = Depends(get_db)):
    results = db.query(
        Student.province,
        func.count(Student.id).label("total")
    ).group_by(Student.province).all()

    return [{"province": r[0], "total": r[1]} for r in results]