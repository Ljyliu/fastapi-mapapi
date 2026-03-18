from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.common.utils import get_password_hash


router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register_user(user_create: UserCreate, 
                        db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User)).where(User.username == user_create.username)
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户名已被注册")
    
    hash_pwd = get_password_hash(user_create.password)
    new_user = User(
        username = user_create.username,
        email = user_create.email,
        password_hash = hash_pwd
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) # 刷新获取新增id等自动生成的字段
    return new_user