from fastapi import APIRouter
from app.api.v1.endpoints import test_pgsql
from app.api.v1.endpoints import user

api_v1 = APIRouter(prefix="/users")
api_v1.include_router(test_pgsql.router, tags=["测试pgsql连接"])
api_v1.include_router(user.router, tags=["用户接口"])