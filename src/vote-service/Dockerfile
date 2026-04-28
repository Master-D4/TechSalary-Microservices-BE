FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the app folder explicitly
COPY ./app ./app

EXPOSE 8005

# Tell Uvicorn to look inside the app folder for main.py
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]