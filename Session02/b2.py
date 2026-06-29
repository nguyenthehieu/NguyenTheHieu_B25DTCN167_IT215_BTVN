"""
1. Endpoint ban đầu là: @app.get("/student")
2. FastAPI sẽ tìm endpoint /students. Tuy nhiên chỉ khai báo: @app.get("/student")
"""

from fastapi import FastAPI

app = FastAPI()
students = [
    {"id": 1, "name": "An"},
    {"id": 2, "name": "Binh"},
    {"id": 3, "name": "Cuong"}
]

@app.get("/students")
def get_students():
    return students