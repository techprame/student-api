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
    """Request body for POST /students."""


class StudentUpdate(StudentBase):
    """Request body for PUT /students/{id} (replaces the whole record)."""


class StudentOut(StudentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: ProductName
    price: float = Field(..., gt=0, le=10_000_000)
    stock: int = Field(..., ge=0, le=1_000_000)


class ProductCreate(ProductBase):
    """Request body for POST /products."""


class ProductUpdate(ProductBase):
    """Request body for PUT /products/{id} (replaces the whole record)."""


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
    """Standard wrapper used by every response."""

    status_code: int
    data: Optional[T] = None
    message: str