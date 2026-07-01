from fastapi import FastAPI, Query

app = FastAPI()

products = [
    {"id": 1, "name": "Laptop", "price": 15000000},
    {"id": 2, "name": "Mouse", "price": 200000},
    {"id": 3, "name": "Keyboard", "price": 500000},
    {"id": 4, "name": "Monitor", "price": 3000000}
]

@app.get("/products")
def get_products(
    keyword: str = Query(default=None),
    max_price: float = Query(default=None)
):
    if max_price is not None and max_price < 0:
        return {"message": "max_price không được âm"}

    result = []

    for product in products:
        if keyword is not None:
            if keyword.lower() not in product["name"].lower():
                continue

        if max_price is not None:
            if product["price"] > max_price:
                continue

        result.append(product)

    return result