from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from functools import wraps
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime,timedelta,timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.db.session import get_async_db
from app.models.user import User
from app.schemas.user import UserResponse

# 密码加密、验证
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# 创建token
def create_access_token(user_id:int):
    expire = datetime.now(timezone.utc) + timedelta(minutes = EXPIRE_MINUTES)

    to_encode = {"sub": str(user_id), "exp": expire}

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

# 获取当前登录用户（依赖）
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_async_db)):
    # 登录失效错误
    login_expired_exception = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED,
        detail= "登录失效，请重新登录",
        headers= {"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get('sub')
        if user_id is None:
            raise login_expired_exception
    except JWTError:
        raise login_expired_exception
    
    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise login_expired_exception
    return UserResponse.model_validate(user)
    



