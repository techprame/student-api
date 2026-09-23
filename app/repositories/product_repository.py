from typing import List, Optional
from sqlalchemy.orm import Session
from app import models, schemas


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, product_id: int) -> Optional[models.Product]:
        return self.db.query(models.Product).filter(models.Product.id == product_id).first()

    def get_all(self, skip: int, limit: int, search: Optional[str]) -> List[models.Product]:
        query = self.db.query(models.Product)
        if search:
            query = query.filter(models.Product.name.ilike(f"%{search}%"))
        return query.order_by(models.Product.id).offset(skip).limit(limit).all()

    def create(self, payload: schemas.ProductCreate) -> models.Product:
        product = models.Product(**payload.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(self, product: models.Product, payload: schemas.ProductUpdate) -> models.Product:
        for field, value in payload.model_dump().items():
            setattr(product, field, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: models.Product) -> None:
        self.db.delete(product)
        self.db.commit()