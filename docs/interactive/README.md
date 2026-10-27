# Model Selection Recommendation

Investigative work to derive features for a model recommendation algorithm for Rosalution.

## Requirements

- Python 3.11+
- uv - Experimenting with using uv package and environment manager for python to run this script  
        `brew install uv`

Optional

- Visual Studio Code
  - Python Extension
  - Jupyter Extension

## Configuration

The notebooks requires the following environment variables to connect, authenticate, and request data from a 
Rosalution installation:

- `ROSALUTION_BASE_URL`
- `ROSALUTION_CLIENT_ID`
- `ROSALUTION_CLIENT_SECRET`

These environment variables can either be sourced within a terminal session or saved in a `.env` file in the project's
root. Visit `<base-rosalution-url-path>/rosalution/account` in a web browser to get your account's Rosalution's API
Client ID and SECRET.

Example `{project-root}/.env`
```text
ROSALUTION_BASE_URL=https://local.rosalution.cgds/rosalution
ROSALUTION_CLIENT_ID=your-client-id
ROSALUTION_CLIENT_SECRET=your-client-secret
```

## Environment Setup

Within the 'model-recommendation-prototype' directory in a terminal create `uv`'s virtual environment and install
dependencies. This will create a virtual environment in `{project_root}/docs/interactive/.env/bin/python`. After
setting up the `uv` virtual environment, create the Jupyter notebook kernel using `uv`. If using visual studio
code, this will be the jupyter notebook kernel used to interact with the jupyter notebooks.

```bash
uv sync
uv run ipython kernel install --user --env VIRTUAL_ENV $(pwd)/.venv --name=rosalution-notebooks
```

## Running the Notebooks 

There are two methods to interact and develop with the Jupyter notebooks; either in a terminal or in visual studio code.

### Running notebooks in visual studio code

1. Ensure the Python and Jupyter extensions are installed.
3. Create a `.env` file in the the workspace root and populate the required variables above.
4. Open the notebook (`.ipynb`) file.
  4.a. If opening in visual studio code the first time, it will prompt you to ask to include the .env file within
       the workspace.  You will need to select the 'yes' option in order for the notebook to load the environment
       variables needed to authenticate with Rosalution.
5. Use the kernel picker in the top right corner in visual studio code to choose Jupyter Notebook kernel that
   `uv` created.  It should be `rosalution-notebooks in {project-root}/docs/interactive/.env/bin/python`. See
   [Visual Studio Code Jupyter Kernel Management documentation](https://code.visualstudio.com/docs/datascience/jupyter-kernel-management)
   and [Using uv with Jupyter](https://docs.astral.sh/uv/guides/integration/jupyter/#using-uv-with-jupyter)
   for more details on selecting the virtual environment to use for the Jupyter kernel.

> **Important note**  
> On MacOS, when using the file explorer to select the interpreter, hidden directories are not shown
> by default.  Use the following key-binding 'CMD + SHIFT + .' to show hidden directories in order to select
> `.venv/bin/python` as your interpreter.

###  Running notebook in terminal

1. Make expected environment variables available within the terminal. This can either be done with sourcing the terminal
   session with the `rosalutionrc.sh` script or by creating a `.env` file within the project root to instruct uv to use.
   
   ```bash
   source rosalutionrc.sh
   ```

2. Run the jupyter notebook service in the `{project-root}/docs/interactive` directory.

   ```bash
   uv run --env-file ../.env --with jupyter jupyter lab
   ```

3. Visit <http://localhost:8888/tree?> in the browser to interact with the Jupyter Notebook
