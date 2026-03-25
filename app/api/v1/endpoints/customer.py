from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.utils import get_current_user
from app.schemas.user import UserResponse
from app.db.session import get_async_db
from app.services.customer_service import get_customer_service
from app.schemas.customer import CustomerResponse
from app.schemas.api_response import ApiResponse


router = APIRouter()

# 获得客户信息
@router.get("/index", response_model=ApiResponse[list[CustomerResponse]])
async def index(current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customers = await get_customer_service(user_id=current_user.id,db=db)
    return ApiResponse(
        code = 200,
        data = customers,
        msg = "操作成功"
    )
    



