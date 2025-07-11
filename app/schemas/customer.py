from pydantic import BaseModel

class CustomerCreate(BaseModel):
    customer_name: str
    phone: str  # required
    address: str | None = None

class CustomerOut(CustomerCreate):
    id: int

    model_config = {
        "from_attributes": True
    }
