from database import Base
from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship

class BookingModel(Base):
    __tablename__ = 'booking'

    id = Column(Integer, primary_key=True)
    driver_id = Column(Integer, ForeignKey('drivers.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('cars.id'), nullable=False)