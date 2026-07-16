from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    status = Column(String(20))

    enrollments = relationship(
        "Enrollment", 
        back_populates="course"
    )