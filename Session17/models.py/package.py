from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class PackageModel(Base):
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True)
    package_code = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    weight = Column(Integer, nullable=False)
    warehouse_id = Column(Integer, ForeignKey('warehouses.id'), nullable=False)

    warehouse = relationship(
        'WarehouseModel', 
        back_populates='packages'
        )
    
    waybills = relationship(
        'WaybillModel',
        back_populates='package'
    )

    trucks = relationship(
        'TruckModel',
        secondary='package_truck',
        back_populates='packages'
    )