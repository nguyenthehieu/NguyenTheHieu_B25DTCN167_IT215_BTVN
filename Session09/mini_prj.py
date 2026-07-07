from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

app = FastAPI()

VALID_STATUSES = ("todo", "in_progress", "done")
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_204_NO_CONTENT = 204
HTTP_400_BAD_REQUEST = 400
HTTP_404_NOT_FOUND = 404
HTTP_422_UNPROCESSABLE_ENTITY = 422
HTTP_500_INTERNAL_SERVER_ERROR = 500

tasks_db = [
    {
        "id": 1, 
        "title": "Thiet ke database Shop AI", 
        "description": "Xay dung bang va toi uu index", 
        "assignee": "QuyDev", 
        "priority": 1, 
        "status": "todo",
        "created_at": "2026-07-01T09:00:00Z"
    },
    {
        "id": 2, 
        "title": "Code bo API Authen", 
        "description": "Trien khai filter verify JWT token", 
        "assignee": "FixerQ", 
        "priority": 2, 
        "status": "done",
        "created_at": "2026-07-01T10:00:00Z"
    }
]

class TaskCreateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=2)
    priority: int = Field(..., ge=1, le=5)

class TaskUpdateSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150)
    description: str = Field(..., min_length=1)
    assignee: str = Field(..., min_length=2)
    priority: int = Field(..., ge=1, le=5)
    status: str

class TaskPublicResponse(BaseModel):
    id: int
    title: str
    description: str
    assignee: str
    priority: int
    status: str
    created_at: str

class ResponseModel(BaseModel):
    statusCode: int
    message: str
    data: dict | list | None
    error: str | None
    timestamp: str
    path: str

def get_time():
    return ""

def success_response(status_code: int, message: str, data, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "data": data,
        "error": None,
        "timestamp": get_time(),
        "path": path,
    }

def to_public_task(task: dict):
    return TaskPublicResponse(**task).dict()

def to_public_tasks(tasks: list[dict]):
    return [to_public_task(task) for task in tasks]

def error_response(status_code: int, message: str, error: str, path: str):
    return {
        "statusCode": status_code,
        "message": message,
        "data": None,
        "error": error,
        "timestamp": get_time(),
        "path": path,
    }


def raise_error(status_code: int, message: str, error_code: str, error: str):
    raise HTTPException(
        status_code=status_code,
        detail={
            "message": message,
            "error": f"{error_code}: {error}",
        },
    )

def find_task_index(task_id: int):
    for index, task in enumerate(tasks_db):
        if task["id"] == task_id:
            return index
    return None

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        content = error_response(
            exc.status_code,
            exc.detail["message"],
            exc.detail["error"],
            request.url.path,
        )
    else:
        content = error_response(
            exc.status_code,
            str(exc.detail),
            exc.__class__.__name__,
            request.url.path,
        )

    return JSONResponse(status_code=exc.status_code, content=content)


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content=error_response(
            HTTP_500_INTERNAL_SERVER_ERROR,
            "Loi he thong!",
            "Internal Server Error",
            request.url.path,
        ),
    )

@app.post("/tasks", status_code=HTTP_201_CREATED, response_model=ResponseModel,)
def create_task(task: TaskCreateSchema):
    for current_task in tasks_db:
        if current_task["title"].lower() == task.title.lower():
            raise_error(
                HTTP_400_BAD_REQUEST,
                "Loi: Tieu de cong viec nay da ton tai trong nhom!",
                "ERR-TASK-01",
                "Task conflict: Title field values duplicates an existing record in the temporary database storage.",
            )

    new_id = max((current_task["id"] for current_task in tasks_db), default=0) + 1
    new_task = {
        "id": new_id,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "priority": task.priority,
        "status": "todo",
        "created_at": get_time(),
        "internal_notes": "Du lieu quan tri noi bo, khong tra ve client.",
    }

    tasks_db.append(new_task)
    return success_response(
        HTTP_201_CREATED,
        "Tao moi cong viec nhom thanh cong!",
        to_public_task(new_task),
        "/tasks",
    )

@app.get("/tasks/search", status_code=HTTP_200_OK, response_model=ResponseModel)
def search_tasks(keyword: str | None = None, task_status: str | None = Query(default=None, alias="status")):
    keyword_lower = keyword.lower() if keyword else None

    results = [
        task
        for task in tasks_db
        if (
            keyword_lower is None
            or keyword_lower in task["title"].lower()
            or keyword_lower in task["assignee"].lower()
        )
        and (task_status is None or task["status"] == task_status)
    ]

    return success_response(
        HTTP_200_OK,
        "Tim kiem cong viec thanh cong!",
        {"total": len(results), "items": to_public_tasks(results)},
        "/tasks/search",
    )

@app.get("/tasks/{task_id}", status_code=HTTP_200_OK, response_model=ResponseModel,)
def get_task_detail(task_id: int):
    task_index = find_task_index(task_id)
    if task_index is None:
        raise_error(
            HTTP_404_NOT_FOUND,
            "Loi: Khong tim thay ID cong viec yeu cau trong he thong!",
            "ERR-TASK-04",
            "Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )

    return success_response(
        HTTP_200_OK,
        "Lay chi tiet cong viec thanh cong!",
        to_public_task(tasks_db[task_index]),
        f"/tasks/{task_id}",
    )

@app.put("/tasks/{task_id}", status_code=HTTP_200_OK, response_model=ResponseModel,)
def update_task(task_id: int, task_update: TaskUpdateSchema):
    task_index = find_task_index(task_id)
    if task_index is None:
        raise_error(
            HTTP_404_NOT_FOUND,
            "Loi: Khong tim thay ID cong viec yeu cau trong he thong!",
            "ERR-TASK-04",
            "Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )

    if task_update.status not in VALID_STATUSES:
        raise_error(
            HTTP_400_BAD_REQUEST,
            "Loi: Trang thai cong viec cap nhat khong dung quy dinh!",
            "ERR-TASK-03",
            "Business logic error: Invalid task status value. Allowed enumerated selection list: ['todo', 'in_progress', 'done'].",
        )

    old_task = tasks_db[task_index]
    updated_task = old_task.copy()
    updated_task.update(task_update.dict())
    updated_task["id"] = old_task["id"]
    updated_task["created_at"] = old_task["created_at"]
    tasks_db[task_index] = updated_task

    return success_response(
        HTTP_200_OK,
        "Cap nhat cong viec thanh cong!",
        to_public_task(updated_task),
        f"/tasks/{task_id}",
    )

@app.delete("/tasks/{task_id}", status_code=HTTP_204_NO_CONTENT)
def delete_task(task_id: int):
    task_index = find_task_index(task_id)
    if task_index is None:
        raise_error(
            HTTP_404_NOT_FOUND,
            "Loi: Khong tim thay ID cong viec yeu cau trong he thong!",
            "ERR-TASK-04",
            "Resource missing error: Target task entity parameter [task_id] can not be located within current active database scope.",
        )

    tasks_db.pop(task_index)
    return None
