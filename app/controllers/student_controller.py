from typing import Optional
from sqlalchemy.orm import Session
from app import schemas
from app.services.student_service import StudentService
from app.utils.response import ok


class StudentController:
    def __init__(self, db: Session):
        self.service = StudentService(db)

    def create_student(self, payload: schemas.StudentCreate):
        student = self.service.create_student(payload)
        return ok(201, schemas.StudentOut.model_validate(student), "Student created successfully")

    def list_students(self, skip: int, limit: int, search: Optional[str]):
        students = self.service.list_students(skip, limit, search)
        data = [schemas.StudentOut.model_validate(s) for s in students]
        return ok(200, data, "Students fetched successfully")

    def get_student(self, student_id: int):
        student = self.service.get_student(student_id)
        return ok(200, schemas.StudentOut.model_validate(student), "Student fetched successfully")

    def update_student(self, student_id: int, payload: schemas.StudentUpdate):
        student = self.service.update_student(student_id, payload)
        return ok(200, schemas.StudentOut.model_validate(student), "Student updated successfully")

    def delete_student(self, student_id: int):
        self.service.delete_student(student_id)
        return ok(200, None, "Student deleted successfully")