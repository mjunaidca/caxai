from fastapi import APIRouter, HTTPException, Depends

from uuid import UUID

router = APIRouter(prefix="/api/hello", tags=["Todo Crud"])


@router.get("/")
def get_todos():
    return {"route": "Hello"}