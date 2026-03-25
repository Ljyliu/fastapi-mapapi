from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.customer import Customer
from typing import List



# 获得归属用户的客户信息
async def get_customer_service(user_id: int, db: AsyncSession) -> List[Customer]:
    result = await db.execute(select(Customer).where(Customer.user_id == user_id))
    return result.scalars().all()