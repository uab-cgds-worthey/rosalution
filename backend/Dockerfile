# Local Development Stage
FROM python:3.9.10 as development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
COPY etc/entrypoint-init.sh /app/entrypoint-init.sh
ENTRYPOINT ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info --reload"]

# Production Build Stage
FROM python:3.9.10 as production-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app/src
COPY etc/entrypoint-init.sh /app/entrypoint-init.sh
ENTRYPOINT ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info"]
