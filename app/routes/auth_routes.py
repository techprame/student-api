from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, models
from app.database import get_db
from app.controllers.auth_controller import AuthController
from app.utils.security import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=schemas.APIResponse[schemas.UserOut], status_code=201)
def register(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    return AuthController(db).register(payload)


@router.post("/login", response_model=schemas.APIResponse[schemas.Token])
def login(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    return AuthController(db).login(payload)


@router.get("/me", response_model=schemas.APIResponse[schemas.UserOut])
def read_me(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return AuthController(db).me(current_user)