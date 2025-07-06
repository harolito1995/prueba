.PHONY: help install dev test docker-up docker-down clean lint format

help:
	@echo "Available commands:"
	@echo "  install     - Install dependencies"
	@echo "  dev         - Run development server"
	@echo "  test        - Run tests"
	@echo "  docker-up   - Start services with Docker"
	@echo "  docker-down - Stop Docker services"
	@echo "  clean       - Clean up containers and volumes"
	@echo "  lint        - Run linting"
	@echo "  format      - Format code"

install:
	pip install -r requirements.txt

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

test:
	python run_tests.py

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

clean:
	docker-compose down -v
	docker system prune -f

lint:
	flake8 . --max-line-length=88 --extend-ignore=E203,W503
	black --check .

format:
	black .
	isort .