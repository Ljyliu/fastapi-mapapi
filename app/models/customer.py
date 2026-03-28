from app.db.session import Base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, UniqueConstraint

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String(20), nullable=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    geocode_status = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    remark = Column(Text, nullable=True, default="")


    __table_args__ = (
        UniqueConstraint("user_id","name",name = "unique_user_customer_name"),
    )
