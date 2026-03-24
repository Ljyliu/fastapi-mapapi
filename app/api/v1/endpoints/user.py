from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.schemas.user import UserResponse, UserCreate, UserLogin
from app.services.user_service import register_user_service, login_user_service
from app.core.utils import handle_exceptions, create_access_token, get_current_user


router = APIRouter()

# 用户注册
@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
@handle_exceptions
async def register_user(user_create: UserCreate, 
                        db: AsyncSession = Depends(get_async_db)):
    
    return await register_user_service(user_create, db)
    

# 用户登录
@router.post("/login", status_code=status.HTTP_200_OK)
@handle_exceptions
async def login_user(user_login: UserLogin, 
                     db: AsyncSession = Depends(get_async_db)):
    
    result = await login_user_service(user_login, db)
    access_token = create_access_token(result.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": result.id,
            "username": result.username,
            "email": result.email
        }
    }

# 获取当前用户信息
@router.get("/me", response_model=UserResponse)
async def get_me(user: UserResponse = Depends(get_current_user)):
    return user