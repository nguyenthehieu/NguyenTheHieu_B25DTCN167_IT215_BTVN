from fastapi import FastAPI

app = FastAPI()
books = [
    {
        "id": 1,
        "title": "Python Basic",
        "author": "Nguyen Van A",
        "category": "programming",
        "year": 2022,
        "is_available": True
    },
    {
        "id": 2,
        "title": "Web API Design",
        "author": "Tran Van B",
        "category": "web",
        "year": 2021,
        "is_available": False
    },
    {
        "id": 3,
        "title": "Database Fundamentals",
        "author": "Le Van C",
        "category": "database",
        "year": 2020,
        "is_available": True
    },
    {
        "id": 4,
        "title": "Machine Learning",
        "author": "Pham Van D",
        "category": "AI",
        "year": 2023,
        "is_available": False
    }
]

@app.get("/books/available")
def get_available_books():
    result = []
    
    for book in books:
        if book['is_available'] == True:
            result.append(book)
    return result

@app.get("/books/borrowed")
def get_borrowed_books():
    result = []

    for book in books:
        if book['is_available'] == False:
            result.append(book)
    return result
