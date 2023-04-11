### Execution instructions

(In the following, replace *name_of_your_config_file.py* with the name of the file you created.)

- Optionally, run `poetry shell` to open a shell that uses the virtual environment, so that
  all the commands can be executed on that shell without prefixing them with `poetry run`.


- To open an interactive demo that answers questions on the terminal, run:

  ```shell
  poetry run ./run.py --config name_of_your_config_file.py answer
  ```

- Open your [BLAB Controller](../../../blab-controller) settings file (`dev.py` or `prod.py`) and update
  the `CHAT_INSTALLED_BOTS` dictionary to include the bot:

  ```python
  CHAT_INSTALLED_BOTS.update({
      "Name of the bot": websocket_external_bot(url="http://localhost:25220"),
  })
  ```

  Change the name and the port accordingly (use the same port defined in `BOT_HTTP_SERVER_PORT`).

- To start the server that will interact with BLAB Controller, run:

  ```shell
  poetry run ./run.py --config name_of_your_config_file.py startserver
  ```
