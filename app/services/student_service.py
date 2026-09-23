from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.repositories.student_repository import StudentRepository


class StudentService:
    def __init__(self, db: Session):
        self.repo = StudentRepository(db)

    def create_student(self, payload: schemas.StudentCreate):
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.create(payload)

    def list_students(self, skip: int, limit: int):
        return self.repo.get_all(skip, limit)

    def get_student(self, student_id: int):
        student = self.repo.get_by_id(student_id)
        if student is None:
            raise HTTPException(status_code=404, detail="Student not found")
        return student

    def update_student(self, student_id: int, payload: schemas.StudentUpdate):
        student = self.get_student(student_id)
        duplicate = self.repo.get_by_email(payload.email)
        if duplicate and duplicate.id != student_id:
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.update(student, payload)

    def delete_student(self, student_id: int):
        student = self.get_student(student_id)
        self.repo.delete(student)