from pydantic import BaseModel
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