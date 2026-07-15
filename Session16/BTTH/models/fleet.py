from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class FleetModel(Base):
    __tablename__ = 'fleets'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    drivers = relationship(
        'DriverModel', 
        back_populates = 'fleet'
    )