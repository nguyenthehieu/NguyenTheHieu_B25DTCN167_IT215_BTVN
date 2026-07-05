from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel

app = FastAPI()
promo_codes_db = {
    "SUMMER25": {"code": "SUMMER25", "discount_rate": 0.15, "max_budget": 50000000, "is_active": True},
    "WELCOME50": {"code": "WELCOME50", "discount_rate": 0.50, "max_budget": 10000000, "is_active": False}
}

class PromoInternal(BaseModel):
    code: str
    discount_rate: float
    max_budget: int 
    is_active: bool

class PromoPublic(BaseModel):
    code: str
    discount_rate: float

@app.get("/promos/{code}", response_model=PromoPublic, status_code=status.HTTP_200_OK)
def get_promo(code: str):
    if code not in promo_codes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mã giảm giá không tồn tại"
        )

    promo = promo_codes_db[code]
    if promo["is_active"] == False:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mã giảm giá đã hết hạn sử dụng"
        )

    return promo