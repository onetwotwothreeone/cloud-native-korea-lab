FROM python:3.13-slim

LABEL org.opencontainers.image.source="https://github.com/onetwotwothreeone/cloud-native-korea-lab"
LABEL org.opencontainers.image.description="Cloud Native Korea Lab FastAPI Mini Platform"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
