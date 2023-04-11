### Installation instructions

- Clone or download a repository that implements this library.

- In the project root, create a configuration file (.py) following the template provided by the repository.
  Modify it as needed, following the instructions in the file. It must contain the variable `BLAB_CONNECTION_SETTINGS`
  alongside the specific settings in other variable(s).

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

### Execution instructions

(In the following, replace *name_of_your_config_file.py* with the name of the file you created.)

- To open an interactive demo that answers questions on the terminal, run:

  ```shell
  poetry run ./run.py --config name_of_your_config_file.py answer
  ```

- Open your [BLAB Controller](../../../blab-controller) settings file (`dev.py` or `prod.py`) and update
  the `CHAT_INSTALLED_BOTS` dictionary to include the Example Bot settings:

  ```python
  CHAT_INSTALLED_BOTS.update({
      "Name of the bot": websocket_external_bot(url="http://localhost:25220"),
  })
  ```

Change the name and the port accordingly.

- To start the server that will interact with BLAB Controller, run:

  ```shell
  poetry run ./run.py --config name_of_your_config_file.py startserver
  ```
