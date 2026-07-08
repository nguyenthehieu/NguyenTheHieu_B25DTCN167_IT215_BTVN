from pydantic import BaseModel

class ParkingSlotCreate(BaseModel):
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool = True

class ParkingSlotResponse(BaseModel):
    id: int
    slot_code: str
    zone_name: str
    max_weight: int
    is_available: bool

    class Config:
        from_attributes = True