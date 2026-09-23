from sqlalchemy.orm import Session
from app import schemas, models
from app.services.auth_service import AuthService


def ok(status_code: int, data, message: str) -> dict:
    return {"status_code": status_code, "data": data, "message": message}


class AuthController:
    def __init__(self, db: Session):
        self.service = AuthService(db)

    def register(self, payload: schemas.UserCreate):
        user = self.service.register(payload)
        return ok(201, schemas.UserOut.model_validate(user), "User registered successfully")

    def login(self, payload: schemas.UserLogin):
        token = self.service.login(payload)
        return ok(200, schemas.Token(access_token=token), "Login successful")

    def me(self, current_user: models.User):
        return ok(200, schemas.UserOut.model_validate(current_user), "Current user fetched")