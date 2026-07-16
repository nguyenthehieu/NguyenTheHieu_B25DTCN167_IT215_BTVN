from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship(
        "Department",
        back_populates="students"
    )

    enrollments = relationship(
        "Enrollment",
        back_populates="student"
    )