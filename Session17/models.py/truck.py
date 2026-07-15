from sqlalchemy import Column, ForeignKey, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class TruckModel(Base):
    __tablename__ = 'trucks'

    id = Column(Integer, primary_key=True)
    license_plate = Column(String(20), unique=True, nullable=False)

    packages = relationship(
        'PackageModel',
        secondary='package_truck',
        back_populates='trucks'
    )