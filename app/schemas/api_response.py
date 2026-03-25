from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: str = 200
    message: str = "操作成功"
    data: Optional[T] = None