from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db
from models import Base, ShipmentModel

app = FastAPI()

class ShipmentUpdate(BaseModel):
    receiver_name: str
    delivery_address: str

def update_shipment_service(db: Session, shipment_id: int, shipment_update: ShipmentUpdate):
    shipment = db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()

    if shipment is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy đơn giao hàng."
        )

    shipment.receiver_name = shipment_update.receiver_name
    shipment.delivery_address = shipment_update.delivery_address

    db.commit()
    db.refresh(shipment)
    return shipment

@app.put("/shipments/{shipment_id}")
def update_shipment(shipment_id: int, shipment_update: ShipmentUpdate, db: Session = Depends(get_db)):

    shipment = update_shipment_service(
        db,
        shipment_id,
        shipment_update
    )

    return {
        "message": "Cập nhật thành công",
        "data": {
            "id": shipment.id,
            "tracking_code": shipment.tracking_code,
            "receiver_name": shipment.receiver_name,
            "delivery_address": shipment.delivery_address
        }
    }