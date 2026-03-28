from pydantic import BaseModel
from typing import Optional, TypeVar, Generic

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    code: int = 0
    msg: str = "操作成功"
    data: Optional[T] = None