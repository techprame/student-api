from typing import Optional
from sqlalchemy.orm import Session
from app import schemas
from app.services.product_service import ProductService


def ok(status_code: int, data, message: str) -> dict:
    return {"status_code": status_code, "data": data, "message": message}


class ProductController:
    def __init__(self, db: Session):
        self.service = ProductService(db)

    def create_product(self, payload: schemas.ProductCreate):
        product = self.service.create_product(payload)
        return ok(201, schemas.ProductOut.model_validate(product), "Product created successfully")

    def list_products(self, skip: int, limit: int, search: Optional[str]):
        products = self.service.list_products(skip, limit, search)
        data = [schemas.ProductOut.model_validate(p) for p in products]
        return ok(200, data, "Products fetched successfully")

    def get_product(self, product_id: int):
        product = self.service.get_product(product_id)
        return ok(200, schemas.ProductOut.model_validate(product), "Product fetched successfully")

    def update_product(self, product_id: int, payload: schemas.ProductUpdate):
        product = self.service.update_product(product_id, payload)
        return ok(200, schemas.ProductOut.model_validate(product), "Product updated successfully")

    def delete_product(self, product_id: int):
        self.service.delete_product(product_id)
        return ok(200, None, "Product deleted successfully")