from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Department, Course, Enrollment

router = APIRouter()

@router.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    department = db.query(Department).filter(Department.id == student.department_id).first()
    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student.id).all()

    course_list = []
    for enrollment in enrollments:
        course = db.query(Course).filter(Course.id == enrollment.course_id).first()

        if course:
            course_list.append(
                {
                    "id": course.id,
                    "name": course.name,
                    "status": course.status
                }
            )

    return {
        "id": student.id,
        "full_name": student.full_name,
        "status": student.status,
        "department": {
            "id": department.id,
            "name": department.name
        },
        "courses": course_list
    }