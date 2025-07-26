from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.models.product import Product
from app.schemas.product import ProductCreate, ProductOut
from app.db.database import get_db  # or wherever get_db is defined

router = APIRouter()

@router.post("/", response_model=ProductOut, status_code=201)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    # Check if product_code already exists
    # existing = db.query(Product).filter(Product.product_code == product_data.product_code).first()
    # if existing:
    #     raise HTTPException(status_code=400, detail="Product with this code already exists.")

    db_product = Product(**product_data.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

# ✅ DELETE endpoint
@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return