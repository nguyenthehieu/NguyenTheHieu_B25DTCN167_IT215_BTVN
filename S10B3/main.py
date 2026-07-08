from database import Base, engine, get_db
from fastapi import Depends, FastAPI, HTTPException, status
from schemas import ShipmentResponse
from sqlalchemy.orm import Session
from UserService import get_shipment as get_shipment_service

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get(
    "/shipments/{shipment_id}",
    response_model=ShipmentResponse,
    status_code=status.HTTP_200_OK,
)
def get_shipment(shipment_id: int, db: Session = Depends(get_db)):
    shipment = get_shipment_service(shipment_id, db)

    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Khong tim thay ma van don",
        )

    return shipment
