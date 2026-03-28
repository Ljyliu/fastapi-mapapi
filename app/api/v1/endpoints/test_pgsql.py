from fastapi import Depends, APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.schemas.api_response import ApiResponse

router = APIRouter()

@router.get("/test_pgsql")
async def test_pgsql(db: AsyncSession = Depends(get_async_db)):
    """测试pgsql连接"""
    try:
        await db.execute(text("select 1"))
        return ApiResponse(code=0, msg="连接成功", data=None)
    except Exception as e:
        return ApiResponse(code=500, msg=f"连接失败：{str(e)}", data=None)