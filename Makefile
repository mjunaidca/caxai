PATH  := $(PATH)
SHELL := /bin/bash

auth:
	cd auth-server && poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080

todo:	
	cd todo-server && poetry run uvicorn app.main:app  --reload --host 0.0.0.0 --port 8000

next:	
	cd nextjs-client && pnpm dev

docker-dev:
	docker compose up --build
