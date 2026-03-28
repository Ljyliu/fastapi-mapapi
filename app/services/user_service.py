from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.utils import get_password_hash, verify_password
from app.core.exceptions import UserAlreadyExists, EmailAlreadyExists, AuthenticationError


async def register_user_service(create_username: str,
                                create_email: str,
                                create_password: str, 
                                db: AsyncSession) -> User:
    
    # 用户名校验
    result = await db.execute(select(User).where(User.username == create_username))
    user = result.scalar_one_or_none()
    if user:
        raise UserAlreadyExists()

    # 邮箱校验
    result = await db.execute(select(User).where(User.email == create_email))
    user = result.scalar_one_or_none()
    if user:
        raise EmailAlreadyExists()


    # 创建用户
    hash_pwd = get_password_hash(create_password)
    new_user = User(
        username = create_username,
        email = create_email,
        password_hash = hash_pwd
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user) # 刷新获取新增id等自动生成的字段
    return new_user

# 用户登录
async def login_user_service(login_username: str,
                             login_password: str, 
                             db: AsyncSession) -> User:
    
    # 获取用户
    result = await db.execute(select(User).where(User.username == login_username))
    user = result.scalar_one_or_none()
    if not user:
        raise AuthenticationError()

    # 验证密码
    if not verify_password(login_password, user.password_hash):
        raise AuthenticationError()
    
    return user
