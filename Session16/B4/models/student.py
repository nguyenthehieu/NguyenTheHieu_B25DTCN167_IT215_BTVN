from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100))

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )

    courses = relationship(
        "Course",
        secondary="enrollments",
        back_populates="students"
    )