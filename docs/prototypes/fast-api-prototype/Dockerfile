# Local Development Stage
FROM python:3.9.10-alpine3.15 as development-stage
WORKDIR /app
COPY Requirements.txt /app/
RUN pip install -r Requirements.txt --no-cache-dir
EXPOSE 8000
ENTRYPOINT [ "python3", "src/main.py" ]

# Production Build Stage
FROM python:3.9.10-alpine3.15 as production-stage
WORKDIR /app
COPY Requirements.txt /app/
RUN pip install -r Requirements.txt --no-cache-dir
EXPOSE 8000
ENTRYPOINT [ "python3", "src/main.py" ]
