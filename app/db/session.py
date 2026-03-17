from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

engine = create_async_engine(settings.database_url, echo=settings.ECHO_SQL)

# 创建基类
Base = declarative_base()

# 创建异步会话
AsyncSessionLocal = async_sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
    bind=engine
)
async def get_async_db() -> AsyncSession:
    """依赖函数"""
    async with AsyncSessionLocal() as db:
        yield db