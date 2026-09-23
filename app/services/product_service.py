from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app import schemas
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, db: Session):
        self.repo = ProductRepository(db)

    def create_product(self, payload: schemas.ProductCreate):
        return self.repo.create(payload)

    def list_products(self, skip: int, limit: int, search: Optional[str]):
        return self.repo.get_all(skip, limit, search)

    def get_product(self, product_id: int):
        product = self.repo.get_by_id(product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    def update_product(self, product_id: int, payload: schemas.ProductUpdate):
        product = self.get_product(product_id)
        return self.repo.update(product, payload)

    def delete_product(self, product_id: int):
        product = self.get_product(product_id)
        self.repo.delete(product)