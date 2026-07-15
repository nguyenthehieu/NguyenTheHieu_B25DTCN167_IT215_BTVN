from database import Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class DriverModel(Base):
    __tablename__ = 'drivers'

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), default='Active', nullable=False)
    fleet_id = Column(Integer, ForeignKey('fleets.id'), nullable=False)

    fleet = relationship(
        'FleetModel', 
        back_populates ='drivers', 
        secondary='booking'
    )
    cars = relationship(
        'CarModel', 
        back_populates ='drivers', 
        secondary='booking'
    )