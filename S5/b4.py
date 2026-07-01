from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
products = [
    {
        "id": 1,
        "code": "SP001",
        "name": "Keyboard",
        "price": 500000,
        "stock": 10
    },
    {
        "id": 2,
        "code": "SP002",
        "name": "Mouse",
        "price": 300000,
        "stock": 5
    }
]

class Product(BaseModel):
    code: str
    name: str
    price: int
    stock: int

@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    product_found = None
    for p in products:
        if p["id"] == product_id:
            product_found = p
            break

    if product_found is None:
        return {
            "detail": "Product not found"
        }
    for p in products:
        if p["id"] != product_id and p["code"] == product.code:
            return {
                "detail": "Product code already exists"
            }
    if product.name.strip() == "":
        return {
            "detail": "Product name is required"
        }
    if product.price <= 0:
        return {
            "detail": "Price must be greater than 0"
        }
    if product.stock < 0:
        return {
            "detail": "Stock must be greater than or equal to 0"
        }

    product_found["code"] = product.code
    product_found["name"] = product.name
    product_found["price"] = product.price
    product_found["stock"] = product.stock

    return {
        "message": "Update product successfully",
        "data": product_found
    }