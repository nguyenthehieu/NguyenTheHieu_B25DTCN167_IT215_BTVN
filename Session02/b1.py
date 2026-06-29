"""
Việc trả về chuỗi (string) có một số nhược điểm:
- Dữ liệu không có cấu trúc rõ ràng.
- Client phải xử lý chuỗi thủ công.
- Khó mở rộng khi cần bổ sung thêm thông tin.

Endpoint: /getStudents chưa tuân theo quy tắc đặt tên RESTful
"""

from fastapi import FastAPI

app = FastAPI()
students = ["An", "Binh", "Cuong"]

@app.get("/students")
def get_students():
    return students