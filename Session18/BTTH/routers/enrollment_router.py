from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models import Student, Course, Enrollment
from schemas import EnrollmentCreate

router = APIRouter()

@router.post("/enrollments", status_code=status.HTTP_201_CREATED)
def create_enrollment(data: EnrollmentCreate, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400,
            detail="Student is not ACTIVE"
        )

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if course is None:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if course.status != "OPEN":
        raise HTTPException(
            status_code=400,
            detail="Course is CLOSED"
        )

    enrollment = db.query(Enrollment).filter( Enrollment.student_id == data.student_id, Enrollment.course_id == data.course_id).first()
    if enrollment:
        raise HTTPException(
            status_code=400,
            detail="Student already enrolled"
        )

    new_enrollment = Enrollment(
        student_id=data.student_id,
        course_id=data.course_id
    )

    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)

    return {
        "message": "Enroll successfully",
        "id": new_enrollment.id,
        "student_id": new_enrollment.student_id,
        "course_id": new_enrollment.course_id
    }