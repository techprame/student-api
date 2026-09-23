from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.controllers.student_controller import StudentController

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("", response_model=schemas.APIResponse[schemas.StudentOut], status_code=201)
def create_student(payload: schemas.StudentCreate, db: Session = Depends(get_db)):
    return StudentController(db).create_student(payload)


@router.get("", response_model=schemas.APIResponse[list[schemas.StudentOut]])
def list_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return StudentController(db).list_students(skip, limit)


@router.get("/{student_id}", response_model=schemas.APIResponse[schemas.StudentOut])
def get_student(student_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return StudentController(db).get_student(student_id)


@router.put("/{student_id}", response_model=schemas.APIResponse[schemas.StudentOut])
def update_student(
    payload: schemas.StudentUpdate,
    student_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    return StudentController(db).update_student(student_id, payload)


@router.delete("/{student_id}", response_model=schemas.APIResponse[None])
def delete_student(student_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return StudentController(db).delete_student(student_id)