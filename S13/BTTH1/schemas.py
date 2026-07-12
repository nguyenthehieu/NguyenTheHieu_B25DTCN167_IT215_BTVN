from pydantic import BaseModel, Field, ConfigDict

class MenuItemCreate(BaseModel):
    dish_code: str
    dish_name: str
    calorie_count: int = Field(gt=0)
    price: float = Field(gt=0)
    status: str = "AVAILABLE"

class MenuItemUpdate(BaseModel):
    dish_code: str | None = None
    dish_name: str | None = None
    calorie_count: int | None = Field(default=None, gt=0)
    price: float | None = Field(default=None, gt=0)
    status: str | None = None

class MenuItemResponse(BaseModel):
    id: int
    dish_code: str
    dish_name: str
    calorie_count: int
    price: float
    status: str
    model_config = ConfigDict(from_attributes=True)