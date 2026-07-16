from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100))
    status = Column(String(20))

    enrollments = relationship(
        "Enrollment", 
        back_populates="student"
    )