# STAGE 1: Builder (Heavy Image)
# Purpose: Compile dependencies and create wheels
FROM python:3.12-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to cache the dependency step
COPY requirements.txt .

# Create Python 'wheels' (compiled binaries) for all dependencies
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# STAGE 2: Runner (Lightweight Image)
# Purpose: Run the application securely
FROM python:3.12-slim as runner

WORKDIR /app

# Install runtime dependencies for Postgres
RUN apt-get update && apt-get install -y libpq5 && rm -rf /var/lib/apt/lists/*

# Copy the pre-compiled wheels from the builder stage
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

# Install the wheels without reaching out to the internet
RUN pip install --no-cache /wheels/*

# Copy your actual application code
COPY ./app ./app

# Expose the port Identity Service runs on
EXPOSE 8001

# Run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]