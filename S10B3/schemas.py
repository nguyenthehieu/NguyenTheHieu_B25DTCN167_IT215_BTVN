from pydantic import BaseModel

try:
    from pydantic import ConfigDict
except ImportError:
    ConfigDict = None

if ConfigDict is not None:
    class ShipmentResponse(BaseModel):
        id: int
        tracking_number: str
        status: str

        model_config = ConfigDict(from_attributes=True)
else:
    class ShipmentResponse(BaseModel):
        id: int
        tracking_number: str
        status: str

        class Config:
            orm_mode = True
