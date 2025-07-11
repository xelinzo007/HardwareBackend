from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.models.category import Category
from app.schemas.category import CategoryCreate, CategoryOut

router = APIRouter()

@router.post("/", response_model=CategoryOut)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing = db.query(Category).filter(
        (Category.category_code == category.category_code) |
        (Category.category_name == category.category_name)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Category code or name already exists")

    new_category = Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryOut])
def list_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()
