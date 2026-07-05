from fastapi import FastAPI, HTTPException, status

app = FastAPI()
orders_list = [
    {"id": 1, "code": "SP001", "payment_status": "PAID", "method": "BANK_TRANSFER"},
    {"id": 2, "code": "SP002", "payment_status": "UNPAID", "method": "NONE"}
]

@app.get("/orders/{order_id}/payment")
def get_payment(order_id: int):
    try:
        if order_id not in orders_list:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Không tìm thấy đơn hàng"
            )

        order = orders_list[order_id]
        return {
            "message": "Lấy lịch sử thanh toán thành công",
            "payment_status": order["payment_status"],
            "method": order["method"]
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Đã xảy ra lỗi hệ thống"
        )

@app.get("/orders")
def get_orders():
    return {
        "message": "Danh sách đơn hàng",
        "data": orders_list
    }