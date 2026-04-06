FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install fastapi uvicorn pydantic openenv requests

EXPOSE 8000

CMD ["python", "-m", "robotics_env.server.app"]
