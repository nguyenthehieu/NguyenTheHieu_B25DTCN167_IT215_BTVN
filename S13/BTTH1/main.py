from fastapi import FastAPI, Depends, Request
from sqlalchemy.orm import Session
from datetime import datetime
import schemas
import service
from database import engine, get_db

app = FastAPI()

@app.post("/menu-items")
def create_menu_item(menu: schemas.MenuItemCreate, request: Request, db: Session = Depends(get_db)):
    if menu.dish_name.strip() == "":
        return {
            "statusCode": 400,
            "message": "Dish name cannot be empty",
            "error": "Bad Request",
            "data": None,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat()
        }

    if menu.status not in ["AVAILABLE", "OUT_OF_STOCK"]:
        return {
            "statusCode": 400,
            "message": "Status must be AVAILABLE or OUT_OF_STOCK",
            "error": "Bad Request",
            "data": None,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat()
        }

    try:
        result = service.create_menu_item(db, menu)

        if result is None:
            return {
                "statusCode": 400,
                "message": "Dish code already exists",
                "error": "Bad Request",
                "data": None,
                "path": request.url.path,
                "timestamp": datetime.now().isoformat()
            }

        return {
            "statusCode": 201,
            "message": "Thêm món ăn thành công",
            "error": None,
            "data": result,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat()
        }

    except Exception:
        return {
            "statusCode": 500,
            "message": "Lỗi hệ thống",
            "error": "Internal Server Error",
            "data": None,
            "path": request.url.path,
            "timestamp": datetime.now().isoformat()
        }