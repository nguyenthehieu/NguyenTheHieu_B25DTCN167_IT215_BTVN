from database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class CarModel(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(50), nullable=False)
    status = Column(String(20), default='Available', nullable=False)

    drivers = relationship(
        'DriverModel', 
        secondary = 'booking', 
        back_populates = ''
    )