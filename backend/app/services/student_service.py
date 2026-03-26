from sqlalchemy.orm import Session
from app.models.student import Student
from typing import List, Optional


class StudentService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_students(self, skip: int = 0, limit: int = 100) -> List[Student]:
        return self.db.query(Student).offset(skip).limit(limit).all()

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def get_student_by_student_id(self, student_id: str) -> Optional[Student]:
        return self.db.query(Student).filter(Student.student_id == student_id).first()

    def create_student(self, **kwargs) -> Student:
        student = Student(**kwargs)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update_student(self, student_id: int, **kwargs) -> Optional[Student]:
        student = self.get_student_by_id(student_id)
        if not student:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(student, key, value)
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete_student(self, student_id: int) -> bool:
        student = self.get_student_by_id(student_id)
        if not student:
            return False
        self.db.delete(student)
        self.db.commit()
        return True