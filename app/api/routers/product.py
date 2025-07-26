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

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_data: ProductCreate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # # Optional: Check if product_code is being changed to one that already exists
    # if product.product_code != product_data.product_code:
    #     code_exists = db.query(Product).filter(Product.product_code == product_data.product_code).first()
    #     if code_exists:
    #         raise HTTPException(status_code=400, detail="Product code already exists.")

    for key, value in product_data.dict().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product