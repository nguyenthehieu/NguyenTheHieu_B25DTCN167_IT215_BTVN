from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
products_db = [
    {"id": 101, "name": "Bàn phím cơ", "stock": 5, "price": 1200000.0},
    {"id": 102, "name": "Chuột Gaming", "stock": 2,"price": 600000.0}
]

orders_db = []

class Order(BaseModel):
    product_id: int
    quantity: int

@app.post("/orders", status_code=status.HTTP_201_CREATED)
def create_order(order: Order):
    product = None
    for p in products_db:
        if p["id"] == order.product_id:
            product = p
            break

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sản phẩm"
        )

    if order.quantity <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Số lượng mua phải lớn hơn 0"
        )

    if order.quantity > product["stock"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sản phẩm không đủ số lượng trong kho"
        )

    product["stock"] = product["stock"] - order.quantity
    new_order = {
        "id": len(orders_db) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "total_price": product["price"] * order.quantity
    }

    orders_db.append(new_order)
    return {
        "message": "Tạo đơn hàng thành công",
        "data": new_order
    }

@app.get("/products")
def get_products():
    return {
        "message": "Danh sách sản phẩm",
        "data": products_db
    }

@app.get("/orders")
def get_orders():
    return {
        "message": "Danh sách đơn hàng",
        "data": orders_db
    }