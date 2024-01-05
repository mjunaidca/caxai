from fastapi import FastAPI
from .web import todos_crud

app = FastAPI()

app.include_router(todos_crud.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
