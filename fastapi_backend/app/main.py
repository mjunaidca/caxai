from fastapi import FastAPI
from .web import todos_crud

app = FastAPI(
    title="FastAPI Backend",
    description="This is a backend application built with FastAPI.",
    tags=["Main Route"]
)

app.include_router(todos_crud.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}
