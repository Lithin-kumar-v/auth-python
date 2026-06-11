FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/srv

WORKDIR /srv

# System deps for Postgres
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Dependencies first (cache-friendly)
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY app ./app
COPY main.py ./main.py
COPY db.py ./db.py
COPY .env ./.env

EXPOSE 8000

# IMPORTANT: target main:app since main.py is at repo root
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
