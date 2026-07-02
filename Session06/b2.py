from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()
students = [
    {"id": 1, "code": "SV001", "name": "Nguyen Van A", "email": "a@gmail.com", "age": 20},
    {"id": 2, "code": "SV002", "name": "Tran Thi B", "email": "b@gmail.com", "age": 22},
    {"id": 3, "code": "SV003", "name": "Le Van C", "email": "c@gmail.com", "age": 18}
]

class Student(BaseModel):
    code: str
    name: str
    email: str
    age: int

@app.get("/students")
def get_students(
    keyword: str = None,
    min_age: int = Field(default=18),
    max_age: int = Field(default=22)
):
    result = students
    if keyword:
        result = []
        for student in students:
            if keyword.lower() in student["name"].lower() or keyword.lower() in student["code"].lower() or keyword.lower() in student["email"].lower():
                result.append(student)

    if min_age is not None:
        temp = []
        for student in result:
            if student["age"] >= min_age:
                temp.append(student)
        result = temp

    if max_age is not None:
        temp = []
        for student in result:
            if student["age"] <= max_age:
                temp.append(student)
        result = temp

    return result

@app.get("/students/{student_id}")
def get_student(student_id: int):
    for student in students:
        if student["id"] == student_id:
            return student

    raise HTTPException(
        status_code=404,
        detail="không tìm thấy sinh viên"
    )

@app.post("/students")
def create_student(student: Student):
    if student.name == "":
        raise HTTPException(
            status_code=400,
            detail="tên khồn được rỗng"
        )

    if student.email == "":
        raise HTTPException(
            status_code=400,
            detail="email k được rỗng"
        )

    if student.age <= 0:
        raise HTTPException(
            status_code=400,
            detail="tuổi phải lớn hơn 0"
        )

    for s in students:
        if s["code"] == student.code:
            raise HTTPException(
                status_code=400,
                detail="Ccode đã tồn tại"
            )

    new_student = {
        "id": len(students) + 1,
        "code": student.code,
        "name": student.name,
        "email": student.email,
        "age": student.age
    }
    students.append(new_student)
    return new_student

@app.put("/students/{student_id}")
def update_student(student_id: int, new_student: Student):
    if new_student.name == "":
        raise HTTPException(
            status_code=400,
            detail="tên kkhong được rỗng"
        )

    if new_student.email == "":
        raise HTTPException(
            status_code=400,
            detail="email không được roongx"
        )

    if new_student.age <= 0:
        raise HTTPException(
            status_code=400,
            detail="tuổi phải loén hơn 0"
        )

    for s in students:
        if s["code"] == new_student.code and s["id"] != student_id:
            raise HTTPException(
                status_code=400,
                detail="code đã tồn tại"
            )

    for i in range(len(students)):
        if students[i]["id"] == student_id:
            students[i] = {
                "id": student_id,
                "code": new_student.code,
                "name": new_student.name,
                "email": new_student.email,
                "age": new_student.age
            }
            return students[i]
        
    raise HTTPException(
        status_code=404,
        detail="không tìm thấy sinh viên"
    )

@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    for i in range(len(students)):
        if students[i]["id"] == student_id:
            return students.pop(i)

    raise HTTPException(
        status_code=404,
        detail="không tìm thấy sinh viên"
    )