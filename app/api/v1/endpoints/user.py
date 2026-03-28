from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.schemas.user import UserResponse, UserCreate, UserLogin, LoginResponse
from app.services.user_service import register_user_service, login_user_service
from app.core.utils import create_access_token, get_current_user
from app.schemas.api_response import ApiResponse


router = APIRouter()

# 用户注册
@router.post("/users", response_model=ApiResponse[UserResponse],status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, 
                        db: AsyncSession = Depends(get_async_db)):
    result = await register_user_service(create_username=user_create.username,
                                         create_email=user_create.email,
                                         create_password=user_create.password,
                                         db=db)
    
    return ApiResponse(
        code = 0,
        data = result,
        msg = "操作成功"
    )
    

# 用户登录
@router.post("/auth/login", response_model=ApiResponse[LoginResponse])
async def login_user(user_login: UserLogin, 
                     db: AsyncSession = Depends(get_async_db)):
    
    result = await login_user_service(login_username=user_login.username,
                                      login_password=user_login.password,
                                      db=db)
    access_token = create_access_token(result.id)
    
    return ApiResponse(
            code = 0,
            data = LoginResponse( 
                access_token = access_token,
                token_type = "bearer",
                user = result),
            msg = "操作成功"
        )
                    

# 获取当前用户信息
@router.get("/users/me", response_model=ApiResponse[UserResponse])
async def get_me(user: UserResponse = Depends(get_current_user)):
    return ApiResponse(
        code = 0,
        data = user,
        msg = "操作成功"
    )