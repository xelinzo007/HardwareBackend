from pydantic import BaseModel

class CategoryCreate(BaseModel):
    category_code: str
    category_name: str

class CategoryOut(CategoryCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
