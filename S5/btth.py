from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
products = [
    {"id": 1, "name": "Keyboard", "price": 500000},
    {"id": 2, "name": "Mouse", "price": 300000}
]

class Product(BaseModel):
    name: str
    price: float

@app.post("/products", status_code=201)
def create_product(product: Product):
    if product.name.strip() == "":
        return {
            "detail": "Product name is required"
        }
    if product.price <= 0:
        return {
            "detail": "Price must be greater than 0"
        }

    new_product = {
        "id": len(products) + 1,
        "name": product.name,
        "price": product.price
    }
    products.append(new_product)

    return {
        "message": "Create product successfully",
        "data": new_product
    }

@app.get("/products")
def get_products():
    return {
        "data": products
    }

@app.delete("/products/{product_id}")
def delete_product(product_id: int):
    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": "Delete product successfully"
            }

    return {
        "detail": "Product not found"
    }