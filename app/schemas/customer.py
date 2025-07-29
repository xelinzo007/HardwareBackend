from pydantic import BaseModel

class CustomerIn(BaseModel):
    customer_name: str
    phone: str
    address: str

    model_config = {
        "from_attributes": True
    }

class CustomerOut(CustomerIn):
    id: int

    model_config = {
        "from_attributes": True
    }


    
