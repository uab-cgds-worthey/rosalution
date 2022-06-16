# Fast API Prototype

## Setup

### Requirements

Project requirements are listed in the `requirement.txt` file at the project's root structure.

```sh
# From docs/prototypes/fast-api-prototypes

pip install -r requirements.txt --user
```

## Running

### Local Deployment

From the `src` folder:

```bash
# From the base project folder: docs/prototypes/fast-api-prototype

python3 src/main.py
```

Now go to `localhost:port` in a web browser. It should show an output of { "Hello": "World" }.

## Docker

One can run the FastAPI prototype in a docker container.

**Local Development Build:**

```bash
# From the base project folder: docs/prototypes/fast-api-prototype

docker build --target="development-stage" --tag="fast-api-prototype" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for FastAPI prototype
# Also, the docker run command seems to want the full path to the prototype folder in rosalution

docker run -v <absolute_path_to_prototype>/fast-api-prototype/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

**Local Production Build:**

```bash
# From the base project folder: docs/prototypes/fast-api-prototype

docker build --target="production-stage" --tag="fast-api-prototype" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for FastAPI prototype
# Also, the docker run command seems to want the full path to the prototype folder in rosalution

docker run -v <absolute_path_to_prototype>/fast-api-prototype/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

### Endpoints

#### **rosalution Endpoints**

`/analysis`
>
> [http://127.0.0.1:8000/analysis](http://127.0.0.1:8000/analysis)
>
>
>Shows a list of analysis available for rosalution

#### **Example FastAPI Endpoints**

`/cat`

> [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
>
>{
> Hello: "World"
>}

`/fruit/{fruit_id}`

> [http://127.0.0.1:8000/fruit/2](http://127.0.0.1:8000/fruit/2)
>
>{
> fruit: "banana"
>}
>

`/items/{item_id}?q`
>
> [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)
>
>{
> item_id: 5,
> q: "somequery"
>}

`/docs`
>
> [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
>
>
>Shows a list of endpoints available to try

## Testing

This prototype uses `pytest` as a testing framework for the Python code. The tests are broken out into unit,
integration, and system tests.

Note: The `-s` flag for the pytest routes the standard out to the console. It allows the `print()` statement
to log output of variables for development purposes.

From the root `./` directory of the project:

Unit Tests:

```bash
pytest -s tests/unit
```

Integration Tests:

```bash
pytest -s tests/integration
```

System Tests:

```bash
pytest -s tests/system
```

## Linting

This project uses `pylint` as a linting tool.

Running the linter:

```bash
# From prototype project root: docs/prototypes/fast-api-prototypes/

pylint src tests
```
