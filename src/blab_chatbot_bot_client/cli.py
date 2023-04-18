"""Contains methods used by the command-line interface."""

from __future__ import annotations

import argparse
from datetime import datetime
from importlib import util as import_util
from pathlib import Path
from typing import Any

from blab_chatbot_bot_client import make_path_absolute
from blab_chatbot_bot_client.conversation import BotClientConversation
from blab_chatbot_bot_client.conversation_websocket import (
    WebSocketBotClientConversation,
)
from blab_chatbot_bot_client.data_structures import (
    Message,
    MessageType,
    OutgoingMessage,
)
from blab_chatbot_bot_client.settings_format import BlabBotClientSettings


def _is_interactive() -> bool:
    """Detect if this is an interactive terminal session.

    Return:
        `True` if the terminal session is iterative, `False` otherwise
    """
    from os import fstat
    from stat import S_ISFIFO, S_ISREG
    from sys import stdin

    mode = fstat(stdin.fileno()).st_mode
    return not (S_ISFIFO(mode) or S_ISREG(mode))


# noinspection PyMethodMayBeStatic
class BlabBotClientArgParser:
    """Parses the arguments and settings and performs the specified actions."""

    def __init__(self, client: type[BotClientConversation[Any]]):
        """Create an instance of the parser.

        Args:
            client: the conversation instance on the client
        """
        self._client = client
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--config", default="settings.py")
        self.subparsers = self.arg_parser.add_subparsers(help="command", dest="command")
        self.subparsers.add_parser("startserver", help="start server")
        self.subparsers.add_parser("answer", help="answer questions typed on terminal")

    @classmethod
    def _load_config(cls, path: str) -> BlabBotClientSettings:
        """Load a configuration file. It must be a .py file.

        Args:
            path: path to the configuration file
        """
        if not path.lower().endswith(".py"):
            raise ValueError("The config file must end with .py")
        cfg_path = make_path_absolute(path)
        spec = import_util.spec_from_file_location(Path(cfg_path).name[:-3], cfg_path)
        assert spec
        assert spec.loader
        settings = import_util.module_from_spec(spec)
        spec.loader.exec_module(settings)
        if not isinstance(settings, BlabBotClientSettings):
            raise ValueError("Invalid settings file")
        return settings

    def parse_and_run(self, arguments: list[str] | None = None) -> bool:
        """Parse the command-line arguments and run the specified command.

        Args:
            arguments: the raw command-line arguments

        Returns:
            whether the execution was successful
        """
        args = self.arg_parser.parse_args(arguments)
        settings = self._load_config(args.config)
        return self.run(args, settings)

    def run(
        self, arguments: argparse.Namespace, settings: BlabBotClientSettings
    ) -> bool:
        """Execute the specified action.

        Args:
            arguments: the parsed command-line arguments
            settings: the loaded configuration
        """
        if arguments.command == "startserver":
            if issubclass(self._client, WebSocketBotClientConversation):
                self._client.start_http_server(settings)
        elif arguments.command == "answer":
            if issubclass(self._client, BotClientConversation):
                self._start_console_chat(settings)
        else:
            return False
        return True

    def get_user_message(self, nth: int) -> str:
        """Read a message from the user.

        If this is the first message, only read it if this bot is not
        expected to initiate the conversation.

        Args:
            nth: the sequential number of the message in the conversation

        Return:
            the message typed by the user, or an empty string if
            nothing should be read
        """
        if nth == 1 and self._client.bot_sends_first_message():
            return ""
        return input()

    def _start_console_chat(self, settings: BlabBotClientSettings) -> None:
        from colorama import init as init_colorama

        init_colorama()
        interactive = _is_interactive()

        bot = self._client(settings, "conv0", "part0")  # dummy ids

        n = 1
        you_display = "YOU"
        bot_display = "BOT"
        while True:
            if n == 1 and self._client.bot_sends_first_message():
                bot_messages = bot.generate_greeting()
            else:
                try:
                    if interactive:
                        self._display_prompt_on_terminal(you_display)
                    question = input()

                    if not interactive:
                        self._display_prompt_on_terminal(you_display)
                        self._display_message_on_terminal(question)
                except (EOFError, KeyboardInterrupt):
                    break
                user_message = Message(
                    type=MessageType.TEXT,
                    text=question,
                    sent_by_human=True,
                    sender_id="part1",
                    time=datetime.now(),
                    id=f"m{n}",
                    local_id=f"user_m{n}",
                )
                bot_messages = bot.generate_answer(user_message)
            n += 1
            for a in bot_messages or []:
                self._display_prompt_on_terminal(bot_display)
                self._display_message_on_terminal(a)
                n += 1

    def _display_prompt_on_terminal(self, sender_name: str) -> None:
        from colorama import Style

        print(
            f"{Style.RESET_ALL}{Style.BRIGHT}\n>> {sender_name}"
            f"{Style.RESET_ALL}{Style.BRIGHT}:{Style.RESET_ALL}",
            end=" ",
        )

    def _display_message_on_terminal(
        self, message: Message | OutgoingMessage | str
    ) -> None:
        from colorama import Fore, Style

        if isinstance(message, (Message, OutgoingMessage)):
            text = message.text
            options = message.options or []
        else:
            text = str(message)
            options = []
        print(f"{Style.RESET_ALL}{Fore.YELLOW}{text}{Style.RESET_ALL}")
        for option in options:
            print(f"        - {Style.RESET_ALL}{Fore.CYAN}{option}{Style.RESET_ALL}")
