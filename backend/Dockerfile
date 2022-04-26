# # Local Development Stage
# FROM python:3.9.10-alpine3.15 as development-stage
# WORKDIR /app
# COPY Requirements.txt /app/
# RUN pip install -r Requirements.txt --no-cache-dir
# EXPOSE 8000
# ENTRYPOINT [ "python3", "src/main.py" ]

# # Production Build Stage
# FROM python:3.9.10-alpine3.15 as production-stage
# WORKDIR /app
# COPY Requirements.txt /app/
# RUN pip install -r Requirements.txt --no-cache-dir
# EXPOSE 8000
# ENTRYPOINT [ "python3", "src/main.py" ]

# Local Development Stage
FROM python:3.9.10-alpine3.15 as development-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
COPY  ./fixtures /app/fixtures
COPY ./src /app/src
<<<<<<< HEAD
ENTRYPOINT ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info --reload"]
=======
# ENTRYPOINT uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info --reload
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info", "--reload"]
>>>>>>> 1af43ab (Properly linted the dockerfile)

# Production Build Stage
FROM python:3.9.10-alpine3.15 as production-stage
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt
COPY  ./fixtures /app/fixtures
COPY ./src /app/src
<<<<<<< HEAD
ENTRYPOINT ["/bin/sh", "-c", "uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info"]
=======
# ENTRYPOINT uvicorn src.main:app --host 0.0.0.0 --port 8000 --log-level info
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
>>>>>>> 1af43ab (Properly linted the dockerfile)
