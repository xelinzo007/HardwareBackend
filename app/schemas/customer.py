from pydantic import BaseModel
from typing import Optional

class CustomerIn(BaseModel):
    customer_name: str
    phone: str
    address: Optional[str] = None

    model_config = {
        "from_attributes": True
    }

class CustomerOut(CustomerIn):
    id: int

    model_config = {
        "from_attributes": True
    }
