# Local Development Stage
FROM python:3.11-slim-bookworm AS development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./src /app/src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]

# Production Build Stage
FROM python:3.11-slim-bookworm AS production-stage
WORKDIR /app
COPY logging.conf /app/logging.conf
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY ./src /app/src
COPY etc/entrypoint-init.sh /app/entrypoint-init.sh
RUN rm /app/src/routers/dev_router.py
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
