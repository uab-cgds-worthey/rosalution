# Local Development Stage
FROM python:3.11-slim-bookworm AS development-stage
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends samtools=1.16.1-1 tabix=1.16+ds-3
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY etc/entrypoint-init.sh /app/etc/entrypoint-init.sh
COPY annotation-render-layout.json /app/annotation-render-layout.json
COPY logging.conf /app/logging.conf
COPY ./src /app/src
ENTRYPOINT [ "./etc/entrypoint-init.sh" ]
CMD [ "--reload"]

# Production Build Stage
FROM python:3.11-slim-bookworm AS production-stage
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends samtools=1.16.1-1 tabix=1.16+ds-3 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY annotation-render-layout.json /app/annotation-render-layout.json
COPY etc/entrypoint-init.sh /app/entrypoint-init.sh
COPY logging.conf /app/logging.conf
COPY ./src /app/src
RUN rm /app/src/routers/dev_router.py
ENTRYPOINT [ "./entrypoint-init.sh" ]
