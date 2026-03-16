from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import DATABASE_URL

# 创建数据库连接引擎
engine = create_engine(DATABASE_URL)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 创建数据库会话的依赖项 后面services里用Depends(get_db)调用 来操作数据库
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()