from fastapi import APIRouter
from app.api.v1.endpoints import test_pgsql

api_v1 = APIRouter()
api_v1.include_router(test_pgsql.router, tags=["测试pgsql连接"])