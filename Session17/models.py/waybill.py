from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class WaybillModel(Base):
    __tablename__ = 'waybills'

    id = Column(Integer, primary_key=True)
    shipping_status = Column(String(50), nullable=False)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    tracking_number = Column(String(50), unique=True, nullable=False)

    package = relationship(
        'PackageModel', 
        back_populates='waybills'
        )