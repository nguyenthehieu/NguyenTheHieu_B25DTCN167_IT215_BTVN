from sqlalchemy.orm import Session
from models import ParkingSlot

def get_all_slots(db: Session):
    return db.query(ParkingSlot).all()

def get_slot_by_id(db: Session, slot_id: int):
    return db.query(ParkingSlot).filter(ParkingSlot.id == slot_id).first()

def get_slot_by_code(db: Session, code: str):
    return db.query(ParkingSlot).filter(ParkingSlot.slot_code == code).first()

def create_slot(db: Session, slot):
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot