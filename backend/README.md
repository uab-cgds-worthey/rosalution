# Rosalution Backend

Rosalution's backend uses FastAPI as a Python REST endpoint framework to accept and proccess frontend and user requests.

It is currently used to handle Rosalution's authentication system, interact with MongoDB for state management,
and the web accessible Swagger API documentation.

## Setup

### Dependencies

- [Python 3.8+](https://www.python.org/) - [Install](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/{"originTabId":1,"originWindowId":1}stable/) - [Install](https://pip.pypa.io/en/stable/installation/)

### Requirements

Dependencies for the Rosalution backend service and development are
managed within the `requirements.txt` file within the project's backend root structure.

### Local Development

To keep dependensies required for projects separate without changing global settings and packages we create
isolated virtual environments for these projects.

All packages necessary for Rosalution development are installed into the `./backend/rosalution_env/` virtual
environment in the setup.sh script.

To create this isolation we use the python virtual environment [venv](https://docs.python.org/3.8/library/venv.html).
Refer to the python virtual environment for documentation.

Note: Make sure setup.sh script is run as this installs the rosalution_env and all it's dependencies.

To use in your shell, activate the virtual environment by running the following commands:

```bash
cd backend
source rosalution_env/bin/activate
```

## Configuration

Rosalution uses Environment variables for configuring the application at the time
of startup.

- **ROSALUTION_ENV** Sets whether the application's environment is in production. This will run the backend with the
[-O flag](https://docs.python.org/3/using/cmdline.html#cmdoption-O) which will turn off `__debug__` statements
within the backend codebase when using the 'entrypoint-init.sh` to start the applicaiton.
- **MONGODB_HOST** Sets the host or host:port for the server host address for MongoDB.
    (default) rosalution-db
      - The default is the **docker compose** name for the service, so inside other docker containers within the same network,
      the **docker compose** name will resolve to that service
- **MONGODB_DB** Sets the database name to connect to at startup time
    (default) rosalution_db

### Production Authentication configuration

Currently Rosalution only supports Central Authentication System (CAS) authentication for the production deployment.
The default settings of Rosalution point the implementation to the UAB CAS.

Rosalution leverages the [python-cas package](https://github.com/python-cas/python-cas) to communicate with the UAB
CAS system. When the CAS object is instantiated, it accepts a `service_url` and a `server_url` which is specific to the
system the application is connecting to. The python-cas package's documentation can be found
[here](https://djangocas.dev/docs/latest/modules/python_cas.html).

If another entity has or wishes to employ a CAS authority, the defined configuration variables allow for this to happen.

 These variables are found in `./backend/src/config.py`

**auth_web_failure_redirect_route** = "/login"

- This is not CAS specific, but it is employed when CAS fails and redirects the user to a specific url in the app

**cas_api_service_url**: str = "http://dev.cgds.uab.edu/rosalution/api/auth/login?nexturl=%2F"

- The application's url and nexturl defines where to redirect when login is successful
- **nexturl** is a CAS parameter that tells the server where to redirect to in your application when completing the
CAS interaction. The **nexturl** parameter will use a relative path.

**cas_server_url**: str = "https://padlockdev.idm.uab.edu/cas/"

- Defines where the CAS url can be reached

**cas_login_enable**: bool = False

- This is relevant when the application is deployed with production, affects how the logout function works

## Linting

This project uses `pylint` as a linting tool.

Running the linter:

```bash
# From ./backend/

pylint src tests
```

## Formatting

Rosalution uses `yapf` to format the python codebase.  Configuration is maintained in `.style.yapf` within the
`./backend` directory.

To recursively format all Python files in place, run the following

```bash
# From ./backend/

yapf -ir .
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

### Local Development Build

```bash
# From the base project folder: /backend

docker system prune -a --volumes

docker build --target="development-stage" --tag="backend" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for backend
# Also, the docker run command seems to want the full path to the rosalution folder

docker run -v <absolute_path_to_backend>/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

### Local Production Build

```bash
# From the base project folder: /backend

docker system prune -a --volumes

docker build --target="production-stage" --tag="backend" -f "./Dockerfile" ./

docker images

# Grab the id from the container that was built for backend
# Also, the docker run command seems to want the full path to the rosalution folder

docker run -v <absolute_path_to_backend>/:/app/ -p 127.0.0.1:8000:8000 <image_id>
```

### Endpoints

#### **rosalution Endpoints**

`/analysis`
>
> [http://127.0.0.1:8000/analysis](http://127.0.0.1:8000/analysis)
>
>
>Shows a list of analysis available for rosalution

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

### Code Coverage

Code coverage is generated by coverage.py using the pytest-cov package.  It was the easiest way to
setup code coverage for unit testing to use pytest-cov and its default configuration, then to
configure coverage.py directly.

The unit tests rely on the .coveragerc file to omit the 'main.py' where the application routes are stored.
'main.py' is tested by integration tests and not unit tests.

To view an HTML report of coverage, change the option of `--cov-report=term` to `--cov-report=html`.
Read <https://pytest-cov.readthedocs.io/en/latest/config.html> to learn more about pytest code coverage
tool configuration.

```bash
pytest --cov=src --cov-fail-under=80 --cov-branch --cov-report=term tests/unit/
```
