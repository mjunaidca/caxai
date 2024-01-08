FROM python:3.12

WORKDIR /caliai

COPY ./requirements.txt /caliai/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /caliai/requirements.txt

COPY ./app /caliai/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
