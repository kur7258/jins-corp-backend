from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

from typing import Literal

# from api.routers.test.test_handler

router = APIRouter(dependencies=[])

class CreateUserRequest(BaseModel):
    id: int
    user_id: str
    user_name: str

user_data = {
    1: {
        "id": 1,
        "user_id": "jin",
        "user_name": "seokjin",
        "use_yn": 'Y'
    },
    2: {
        "id": 2,
        "user_id": "lim",
        "user_name": "jina",
        "use_yn": 'Y'
    },
    3: {
        "id": 3,
        "user_id": "test",
        "user_name": "test_man",
        "use_yn": 'N'
    }
}

@router.get("/users", status_code=200)
def get_users_router(order: str | None = None):
    ret =list(user_data.values())
    if order and order == 'DESC':
        return ret[::-1]
    return ret
    
@router.get("/users/{user_id}", status_code=200)
def get_user_router(user_id: int):
    if user_id not in user_data:
        raise HTTPException(status_code=404, detail="User not found")
    return user_data[user_id]

@router.post("/users", status_code=201)
def post_user_router(user: CreateUserRequest):
    if user.id in user_data:
        raise HTTPException(status_code=400, detail="User already exists")
    user_data[user.id] = user.dict()
    return user.dict()

@router.patch("/users/{user_id}", status_code=200)
def update_user_router(
    user_id: int,
    use_yn: Literal["Y", "N"] = Body(..., embed=True),
):
    user = user_data.get(user_id)
    if user:
        user["use_yn"] = use_yn
        return user
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/users/{user_id}", status_code=204)
def delete_user_router(user_id: int):
    if user_id not in user_data:
        raise HTTPException(status_code=404, detail="User not found")
    del user_data[user_id]