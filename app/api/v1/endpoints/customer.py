from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.utils import get_current_user
from app.schemas.user import UserResponse
from app.db.session import get_async_db
from app.services.customer_service import get_customer_service, create_customer_service, get_one_customer_service, update_customer_service, delete_customer_service
from app.schemas.customer import CustomerResponse, CreateCustomer
from app.schemas.api_response import ApiResponse


router = APIRouter()

# 获得客户列表
@router.get("/customers", response_model=ApiResponse[list[CustomerResponse]])
async def list_customers(current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customers = await get_customer_service(user_id=current_user.id, db=db)
    return ApiResponse(
        code = 0,
        data = customers,
        msg = "操作成功"
    )

# 创建客户
@router.post("/customers",response_model=ApiResponse[CustomerResponse],status_code=status.HTTP_201_CREATED)
async def create_customer(customer_create: CreateCustomer,
                current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customer = await create_customer_service(customer_name=customer_create.name,
                                             customer_phone=customer_create.phone,
                                             customer_address=customer_create.address,
                                             customer_remark=customer_create.remark,
                                             db=db,
                                             user_id=current_user.id)
    return ApiResponse(
        code = 0,
        data = customer,
        msg = "操作成功"
    )

# 获得单个客户信息
@router.get("/customers/{customer_id}", response_model=ApiResponse[CustomerResponse])
async def get_customer(customer_id: int,
                current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customer = await get_one_customer_service(id=customer_id, user_id = current_user.id, db=db)
    return ApiResponse(
        code = 0,
        data = customer,
        msg = "操作成功"
    )
    
# 更新客户信息
@router.put("/customers/{customer_id}", response_model=ApiResponse[CustomerResponse])
async def update_customer(customer_id: int,
                customer_update: CreateCustomer,
                current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customer = await update_customer_service(customer_id=customer_id,
                                             update_name=customer_update.name,
                                             update_phone=customer_update.phone,
                                             update_address=customer_update.address,
                                             update_remark=customer_update.remark,
                                             db=db,
                                             user_id=current_user.id)
    return ApiResponse(
        code = 0,
        data = customer,
        msg = "操作成功"
    )


@router.delete("/customers/{customer_id}", response_model=ApiResponse[CustomerResponse])
async def delete_customer(customer_id: int,
                current_user: UserResponse = Depends(get_current_user),
                db: AsyncSession = Depends(get_async_db)):
    customer = await delete_customer_service(customer_id=customer_id,
                                             db=db,
                                             user_id=current_user.id)
    return ApiResponse(
        code = 0,
        data = customer,
        msg = "操作成功"
    )

    


