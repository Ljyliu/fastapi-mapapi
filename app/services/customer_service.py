from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.customer import Customer
from app.core.exceptions import CustomerAlreadyExists, PhoneNumberError, CustomerNotFound



# 获得归属用户的客户信息
async def get_customer_service(user_id: int, db: AsyncSession) -> List[Customer]:
    result = await db.execute(select(Customer).where(Customer.user_id == user_id))
    return result.scalars().all()



# 验证手机号码
def _validate_phone(phone: Optional[str]) -> None:
    if phone:
        if len(phone) > 20:
            raise PhoneNumberError(msg="手机号码长度不能超过20位")
        
        if len(phone) < 5:
            raise PhoneNumberError(msg="手机号码长度不能少于5位")
        
        if not phone.isdigit(): # 判断是否全为数字
            raise PhoneNumberError(msg="手机号码只能为数字")



# 验证客户姓名
async def _validate_customer_name(customer_name: str,
                                 current_user_id:int,
                                 db: AsyncSession,
                                 exists_id: Optional[int]) -> None:
    """
    验证客户姓名是否重复
    
    Args:
        name: 客户姓名
        user_id: 用户 ID
        db: 数据库会话
        exists_id: 排除的客户 ID（更新时用，避免和自己冲突）
    """
    result = await db.execute(select(Customer).where(
        Customer.name == customer_name,
        Customer.user_id == current_user_id
    ))
    customer = result.scalar_one_or_none()
    
    if customer:
        # 如果没有 exists_id，说明是创建操作，直接报错
        # 如果有 exists_id 但和查询到的 ID 不同，说明是有别的客户重名，也报错
        if exists_id is None or customer.id != exists_id:
            raise CustomerAlreadyExists()



# 创建客户
async def create_customer_service(customer_name: str,
                                  customer_address: str,
                                  db: AsyncSession,
                                  user_id: int,
                                  customer_phone: Optional[str] = None,
                                  customer_remark: Optional[str] = "",) -> Customer:
    # 客户姓名校验
    await _validate_customer_name(customer_name=customer_name,
                                 current_user_id=user_id,
                                 db=db,
                                 exists_id=None)
        
    # 客户电话校验
    _validate_phone(phone=customer_phone)

    # 创建客户
    new_customer = Customer(
        name = customer_name,
        phone = customer_phone,
        address = customer_address,
        remark = customer_remark,
        user_id = user_id
    )
    db.add(new_customer)
    await db.commit()
    await db.refresh(new_customer)
    return new_customer



# 获得单个客户信息
async def get_one_customer_service(id: int, user_id: int, db: AsyncSession) -> Customer:
    result = await db.execute(select(Customer).where(Customer.id == id, Customer.user_id == user_id))
    customer = result.scalar_one_or_none()
    if not customer:
        raise CustomerNotFound()
    return customer



# 更新客户信息
async def update_customer_service(customer_id: int,
                                  update_name: str,
                                  update_address: str,
                                  db: AsyncSession,
                                  user_id: int,
                                  update_phone: Optional[str] = None,
                                  update_remark: Optional[str] = "",) -> Customer:
    customer = await get_one_customer_service(customer_id, user_id, db)

    # 客户姓名校验
    await _validate_customer_name(customer_name=update_name,
                                 current_user_id=user_id,
                                 db=db,
                                 exists_id=customer_id)
    
    # 客户电话校验
    _validate_phone(phone=update_phone)

    customer.name = update_name
    customer.phone = update_phone
    customer.address = update_address
    customer.remark = update_remark

    await db.commit()
    await db.refresh(customer)
    return customer

    

# 删除客户
async def delete_customer_service(customer_id: int, user_id: int, db: AsyncSession) -> Customer:
    customer = await get_one_customer_service(customer_id, user_id, db)
    await db.delete(customer)
    await db.commit()
    return customer