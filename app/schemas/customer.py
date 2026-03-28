from pydantic import BaseModel, Field
from typing import Optional

class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str] = None
    address: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geocode_status: Optional[str] = None
    remark: Optional[str] = ""

    model_config = { "from_attributes": True }


class CreateCustomer(BaseModel):
    name: str
    phone: Optional[str] = Field(None,max_length=20)
    address: str
    remark: Optional[str] = ""