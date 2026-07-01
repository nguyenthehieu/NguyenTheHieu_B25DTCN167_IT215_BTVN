from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

students = [
    {
        "full_name": "Student Demo",
        "email": "existing@gmail.com",
        "age": 21,
        "course": "python",
        "phone": "0123456789"
    }
]

class Student(BaseModel):
    full_name: str
    email: str
    age: int
    course: str
    phone: str

@app.post("/students")
def create_student(student: Student):
    if len(student.full_name.strip()) < 3:
        return {
            "detail": "Họ tên phải có ít nhất 3 ký tự"
        }

    if "@" not in student.email:
        return {
            "detail": "Email không đúng định dạng"
        }

    for s in students:
        if s["email"] == student.email:
            return {
                "detail": "Email đã tồn tại trong hệ thống"
            }

    students.append(student.model_dump())

    return {
        "message": "Thêm học viên thành công",
        "student": student
    }