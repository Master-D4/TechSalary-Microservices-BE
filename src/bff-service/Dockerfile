# STAGE 1: Builder
FROM python:3.12-slim as builder

WORKDIR /build

COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# STAGE 2: Runner
FROM python:3.12-slim as runner

WORKDIR /app

COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

RUN pip install --no-cache /wheels/*

COPY ./app ./app

# Expose the port BFF Service runs on
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]