from fastapi import APIRouter
from app.api.v1.endpoints import test_pgsql
from app.api.v1.endpoints import user
from app.api.v1.endpoints import customer

api_v1 = APIRouter()
api_v1.include_router(test_pgsql.router, tags=["测试pgsql连接"])
api_v1.include_router(user.router, tags=["用户认证接口"])
api_v1.include_router(customer.router, tags=["客户管理接口"])