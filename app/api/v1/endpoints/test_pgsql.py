from fastapi import Depends, APIRouter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db

router = APIRouter()

@router.get("/test_pgsql")
async def test_pgsql(db: AsyncSession = Depends(get_async_db)):
    """测试pgsql连接"""
    try:
        await db.execute(text("select 1"))
        return {"message": "连接成功", "code": 200}
    except Exception as e:
        return {"message": "连接失败", "code": 500, "error": str(e)}
