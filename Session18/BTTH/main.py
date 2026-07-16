from fastapi import FastAPI
from database import Base, engine
from routers.student_router import router as student_router
from routers.enrollment_router import router as enrollment_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(student_router)
app.include_router(enrollment_router)