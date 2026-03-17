from db.session import Base
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=True, index=True)
    address = Column(String, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    geocode_status = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    remark = Column(Text, nullable=True, default="")
