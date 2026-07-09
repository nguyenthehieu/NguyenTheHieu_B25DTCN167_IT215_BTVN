from sqlalchemy import Column, Integer, String
from database import Base

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100))
    email = Column(String(100))