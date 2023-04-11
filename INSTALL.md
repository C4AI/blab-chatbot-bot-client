### Installation instructions

- Clone or download a repository that implements this library.

- In the project root, create the configuration file (.py):
  make a local copy (with a different name) of the template file provided by the repository and
  modify it as needed, following the instructions in the file. It must contain the
  variable `BLAB_CONNECTION_SETTINGS`
  alongside the specific settings in other variable(s).

  Note:
  - Non-absolute paths will be relative to the root directory.
  - In `BLAB_CONNECTION_SETTINGS`:
    - `BOT_HTTP_SERVER_HOSTNAME` should be `127.0.0.1` to accept only local connections from the controller;
    - `BOT_HTTP_SERVER_PORT` is arbitrary as long as it is available;
    - `BLAB_CONTROLLER_WS_URL` is the controller address and must start with `ws://` or `wss://`
      (the same path used by the frontend).

- Install [Poetry](https://python-poetry.org/) ≥ 1.2:

  ```shell
  curl -sSL https://install.python-poetry.org | python3 -
  ```
  If *~/.local/bin* is not in `PATH`, add it as suggested by the output of Poetry installer.

- Run Poetry to install the dependencies in a new virtual environment (_.venv_):

  ```shell
  POETRY_VIRTUALENVS_IN_PROJECT=true poetry install
  ```

- Note that some programs may require additional steps. Check the corresponding documentation.
