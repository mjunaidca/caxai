PATH  := $(PATH)
SHELL := /bin/bash

api-start:
	poetry run uvicorn api.index:app --reload

dev:
	pnpm dev

start:
	pnpm build && start
