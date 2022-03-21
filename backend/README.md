# README

## Setup

### Requirements

Project requirements are listed in the `requirement.txt` file at the project's root structure.

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

Now go to `localhost:port` in a web browser. It should show an output of { "Hello": "World" }.

### Endpoints

`/default`

> [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
>
>{
> Hello: "World"
>}
