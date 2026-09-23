from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.repositories.user_repository import UserRepository
from app.utils.security import hash_password, verify_password, create_access_token


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, payload: schemas.UserCreate):
        if self.repo.get_by_email(payload.email):
            raise HTTPException(status_code=409, detail="Email already registered")
        return self.repo.create(payload.email, hash_password(payload.password))

    def login(self, payload: schemas.UserLogin) -> str:
        user = self.repo.get_by_email(payload.email)
        if user is None or not verify_password(payload.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        return create_access_token(user.email)
