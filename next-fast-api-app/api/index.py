from fastapi import FastAPI
from .web import hello

app = FastAPI()
app.include_router(hello.router)

@app.get("/api/python")
def hello_world():
    return {"message": "Hello World"}

@app.get("/api")
def get_todsos():
    return {"route": "api"}