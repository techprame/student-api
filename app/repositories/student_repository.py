from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas


class StudentRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, student_id: int) -> Optional[models.Student]:
        return self.db.query(models.Student).filter(models.Student.id == student_id).first()

    def get_by_email(self, email: str) -> Optional[models.Student]:
        return self.db.query(models.Student).filter(models.Student.email == email).first()

    def get_all(self, skip: int, limit: int) -> List[models.Student]:
        return (
            self.db.query(models.Student)
            .order_by(models.Student.id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create(self, payload: schemas.StudentCreate) -> models.Student:
        student = models.Student(**payload.model_dump())
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update(self, student: models.Student, payload: schemas.StudentUpdate) -> models.Student:
        for field, value in payload.model_dump().items():
            setattr(student, field, value)
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(self, student: models.Student) -> None:
        self.db.delete(student)
        self.db.commit()