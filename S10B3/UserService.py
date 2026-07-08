from models import ShipmentModel
from sqlalchemy.orm import Session

def get_shipment(shipment_id: int, db: Session):
    return db.query(ShipmentModel).filter(ShipmentModel.id == shipment_id).first()
