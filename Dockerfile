FROM python:3.11

RUN mkdir /note

WORKDIR /note

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

RUN pip install gunicorn uvicorn

COPY . .

CMD ["gunicorn", "src.app.asgi:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]