from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
import models
import UserService
import schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def response(statusCode, message, error, data, path):
    return {
        "statusCode": statusCode,
        "message": message,
        "error": error,
        "data": data,
        "path": path,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/parking-slots")
def create_parking_slot(parking: schemas.ParkingSlotCreate, request: Request, db: Session = Depends(get_db)):
    if parking.zone_name.strip() == "":
        return response(
            400,
            "Zone name is required",
            "Bad Request",
            None,
            str(request.url.path)
        )

    if parking.max_weight <= 0:
        return response(
            400,
            "Max weight must be greater than 0",
            "Bad Request",
            None,
            str(request.url.path)
        )

    check = UserService.get_slot_by_code(db, parking.slot_code)
    if check:
        return response(
            400,
            "Slot code already exists",
            "Bad Request",
            None,
            str(request.url.path)
        )

    new_slot = models.ParkingSlot(
        slot_code=parking.slot_code,
        zone_name=parking.zone_name,
        max_weight=parking.max_weight,
        is_available=parking.is_available
    )

    try:
        UserService.create_slot(db, new_slot)
        return response(
            201,
            "Thêm vị trí đỗ xe thành công",
            None,
            {
                "id": new_slot.id,
                "slot_code": new_slot.slot_code,
                "zone_name": new_slot.zone_name,
                "max_weight": new_slot.max_weight,
                "is_available": new_slot.is_available
            },
            str(request.url.path)
        )

    except Exception:
        db.rollback()
        return response(
            500,
            "Database Error",
            "Internal Server Error",
            None,
            str(request.url.path)
        )

@app.get("/parking-slots")
def get_all(request: Request,db: Session = Depends(get_db)):
    slots = UserService.get_all_slots(db)
    data = []
    for slot in slots:
        data.append({
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        })

    return response(
        200,
        "Lấy danh sách thành công",
        None,
        data,
        str(request.url.path)
    )

@app.get("/parking-slots/{slot_id}")
def get_one(slot_id: int, request: Request, db: Session = Depends(get_db)):
    slot = UserService.get_slot_by_id(db, slot_id)
    if slot is None:
        return response(
            404,
            "Parking slot not found",
            "Not Found",
            None,
            str(request.url.path)
        )

    return response(
        200,
        "Lấy chi tiết thành công",
        None,
        {
            "id": slot.id,
            "slot_code": slot.slot_code,
            "zone_name": slot.zone_name,
            "max_weight": slot.max_weight,
            "is_available": slot.is_available
        },
        str(request.url.path)
    )