from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.utils import get_password_hash, verify_password
from app.core.exceptions import UserAlreadyExists, EmailAlreadyExists, AuthenticationError


async def register_user_service(user_create: UserCreate, 
                                db: AsyncSession):
    
    # 用户名校验
    result = await db.execute(select(User).where(User.username == user_create.username))
    user = result.scalar_one_or_none()
    if user:
        raise UserAlreadyExists("用户名已被注册")

    # 邮箱校验
    result = await db.execute(select(User).where(User.email == user_create.email))
    user = result.scalar_one_or_none()
    if user:
        raise EmailAlreadyExists("邮箱已被注册")


    # 创建用户
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

# 用户登录
async def login_user_service(user_login: UserLogin, 
                             db: AsyncSession):
    
    # 获取用户
    result = await db.execute(select(User).where(User.username == user_login.username))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthenticationError("用户名或密码错误")

    # 验证密码
    if not verify_password(user_login.password, user.password_hash):
        raise AuthenticationError("用户名或密码错误")
    
    return user
