FROM python:3.12

WORKDIR /todos_crud

COPY ./requirements.txt /todos_crud/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /todos_crud/requirements.txt

COPY ./app /todos_crud/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
