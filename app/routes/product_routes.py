from typing import Optional
from fastapi import APIRouter, Depends, Path, Query
from sqlalchemy.orm import Session
from app import schemas
from app.database import get_db
from app.controllers.product_controller import ProductController

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=schemas.APIResponse[schemas.ProductOut], status_code=201)
def create_product(payload: schemas.ProductCreate, db: Session = Depends(get_db)):
    return ProductController(db).create_product(payload)


@router.get("", response_model=schemas.APIResponse[list[schemas.ProductOut]])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    search: Optional[str] = Query(None, min_length=1, max_length=50),
    db: Session = Depends(get_db),
):
    return ProductController(db).list_products(skip, limit, search)


@router.get("/{product_id}", response_model=schemas.APIResponse[schemas.ProductOut])
def get_product(product_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return ProductController(db).get_product(product_id)


@router.put("/{product_id}", response_model=schemas.APIResponse[schemas.ProductOut])
def update_product(
    payload: schemas.ProductUpdate,
    product_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
):
    return ProductController(db).update_product(product_id, payload)


@router.delete("/{product_id}", response_model=schemas.APIResponse[None])
def delete_product(product_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return ProductController(db).delete_product(product_id)