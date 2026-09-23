from typing import Annotated, Generic, Optional, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
)

Name = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=50)]
Course = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=100)]
ProductName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=100)]


class StudentBase(BaseModel):
    name: Name
    email: EmailStr
    age: int = Field(..., ge=5, le=100)
    course: Course


class StudentCreate(StudentBase):
    """POST /students ka body."""


class StudentUpdate(StudentBase):
    """PUT /students/{id} ka body (poora record replace hota hai)."""


class StudentOut(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: ProductName
    price: float = Field(..., gt=0, le=10_000_000)
    stock: int = Field(..., ge=0, le=1_000_000)


class ProductCreate(ProductBase):
    """POST /products ka body."""


class ProductUpdate(ProductBase):
    """PUT /products/{id} ka body (poora record replace hota hai)."""


class ProductOut(ProductBase):
    id: int

    model_config = ConfigDict(from_attributes=True)



class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=64)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=64)


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Har response ka standard format."""

    status_code: int
    data: Optional[T] = None
    message: str