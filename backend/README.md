# README

## Setup

### Requirements

Project depdencies are listed in the `requirements.txt` file at the project's
root structure.

```sh
# From ./backend/

pip install -r requirements.txt
```

## Linting

This project uses `pylint` as a linting tool.

Running the linter:

```bash
# From ./backend/

pylint src tests
```

## Running

### Local Deployment

From the `src` folder:

```bash
# From project source folder: ./src

uvicorn main:app --reload
```

Now go to `localhost:port` in a web browser.

## Docker

To run the backend service in a docker container.

**Local Development Build:**

```bash
# From the base project folder: /backend

docker system prune -a --volumes

docker build --target="development-stage" --tag="backend" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for backend
# Also, the docker run command seems to want the full path to the diverGen folder

docker run -v <absolute_path_to_backend>/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

**Local Production Build:**

```bash
# From the base project folder: /backend

docker system prune -a --volumes

docker build --target="production-stage" --tag="backend" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for backend
# Also, the docker run command seems to want the full path to the diverGen folder

docker run -v <absolute_path_to_backend>/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

### Endpoints

#### **diverGen Endpoints**

`/analysis`
>
> [http://127.0.0.1:8000/analysis](http://127.0.0.1:8000/analysis)
>
>
>Shows a list of analysis available for diverGen

#### **Test Endpoints**

`/default`

> [http://127.0.0.1:8000/default](http://127.0.0.1:8000/default)
>
>{
> Hello: "World"
>}

## Testing

The backend service uses `pytest` as a testing framework for the Python code. The tests are broken out into unit,
integration, and system tests.

Note: The `-s` flag for the pytest routes the standard out to the console. It allows the `print()` statement to log
output of variables for development purposes.

From the root `./` directory of the project:

Unit Tests:

```bash
pytest -s tests/unit
```

Integration Tests:

```bash
pytest -s tests/integration
```
