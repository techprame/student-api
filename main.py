from fastapi import FastAPI
from pydantic import BaseModel

from database import Base, engine
import models
from database import SessionLocal

app = FastAPI(title="Student Management API")

# Database tables create karna
Base.metadata.create_all(bind=engine)


class StudentSchema(BaseModel):
    name: str
    email: str
    age: int
    course: str


@app.get("/")
def home():
    return {
        "message": "Student Management API is running"
    }


@app.post("/students")
@app.get("/students")
@app.get("/students/{student_id}")
@app.put("/students/{student_id}")
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if student:
        db.delete(student)
        db.commit()
        db.close()

        return {
            "message": "Student deleted successfully"
        }

    db.close()

    return {
        "message": "Student not found"
    }
def update_student(student_id: int, student: StudentSchema):
    db = SessionLocal()

    existing_student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    if existing_student:
        existing_student.name = student.name
        existing_student.email = student.email
        existing_student.age = student.age
        existing_student.course = student.course

        db.commit()
        db.refresh(existing_student)
        db.close()

        return {
            "message": "Student updated successfully",
            "student": existing_student
        }

    db.close()

    return {
        "message": "Student not found"
    }
def get_student(student_id: int):
    db = SessionLocal()

    student = db.query(models.Student).filter(
        models.Student.id == student_id
    ).first()

    db.close()

    return student
def get_students():
    db = SessionLocal()

    students = db.query(models.Student).all()

    db.close()

    return students
def create_student(student: StudentSchema):
    db = SessionLocal()

    new_student = models.Student(
        name=student.name,
        email=student.email,
        age=student.age,
        course=student.course
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    db.close()

    return {
        "message": "Student created successfully",
        "student": new_student
    }
    



