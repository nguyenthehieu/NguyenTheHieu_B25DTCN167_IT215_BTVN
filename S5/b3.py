from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"}
]

courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2}
]

registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1}
]

class Registration(BaseModel):
    student_id: int
    course_id: int

@app.post("/registrations", status_code=201)
def create_registration(registration: Registration):
    student_found = False
    for student in students:
        if student["id"] == registration.student_id:
            student_found = True
            break

    if not student_found:
        return {
            "detail": "Student not found"
        }

    course_found = None
    for course in courses:
        if course["id"] == registration.course_id:
            course_found = course
            break

    if course_found is None:
        return {
            "detail": "Course not found"
        }

    for reg in registrations:
        if (reg["student_id"] == registration.student_id and
                reg["course_id"] == registration.course_id):
            return {
                "detail": "Student already registered this course"
            }

    count = 0
    for reg in registrations:
        if reg["course_id"] == registration.course_id:
            count += 1

    if count >= course_found["capacity"]:
        return {
            "detail": "Course is full"
        }

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id
    }

    registrations.append(new_registration)

    return {
        "message": "Registration created successfully",
        "data": new_registration
    }