from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_async_db
from app.schemas.user import UserResponse, UserCreate
from app.services.user_service import register_user_service
from app.core.exceptions import UserAlreadyExists, EmailAlreadyExists


router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_create: UserCreate, 
                        db: AsyncSession = Depends(get_async_db)):
    
    try:
        return await register_user_service(user_create, db)
    
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))
    
    except EmailAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=str(e))