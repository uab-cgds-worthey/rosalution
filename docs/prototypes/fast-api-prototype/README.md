# Fast API Prototype

## Setup

### Requirements

Project requirements are listed in the `requirement.txt` file at the project's root structure.

```sh
# From project root: ./

pip install -r requirements.txt
```

## Running

### Local Deployment

From the `src` folder:

```bash
# From project source folder: ./src

uvicorn main:app --reload
```

Now go to `localhost:port` in a web browser. It should show an output of { "Hello": "World" }.

### Endpoints

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
