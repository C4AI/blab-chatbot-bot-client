import argparse
from importlib import util as import_util

from pathlib import Path
from typing import Type, Any

from blab_chatbot_bot_client import make_path_absolute
from blab_chatbot_bot_client.conversation import BotClientConversation
from blab_chatbot_bot_client.conversation_websocket import (
    WebSocketBotClientConversation,
)
from blab_chatbot_bot_client.settings_format import BlabBotClientSettings


class BlabBotClientArgParser:
    def __init__(self, client: Type[BotClientConversation]):
        self._client = client
        self.arg_parser = argparse.ArgumentParser()
        self.arg_parser.add_argument("--config", default="settings.py")
        self.subparsers = self.arg_parser.add_subparsers(help="command", dest="command")
        self.subparsers.add_parser("startserver", help="start server")
        self.subparsers.add_parser("answer", help="answer question typed on terminal")

    @classmethod
    def _load_config(cls, path: str) -> BlabBotClientSettings:
        cfg_path = make_path_absolute(path)
        spec = import_util.spec_from_file_location(Path(cfg_path).name[:-3], cfg_path)
        assert spec
        assert spec.loader
        settings = import_util.module_from_spec(spec)
        spec.loader.exec_module(settings)
        if not isinstance(settings, BlabBotClientSettings):
            raise ValueError("Invalid settings file")
        return settings

    def parse_and_run(self, args: list[str] | None = None) -> bool:
        args = self.arg_parser.parse_args(args)
        settings = self._load_config(args.config)
        if args.command == "startserver":
            if issubclass(self._client, WebSocketBotClientConversation):
                self._client.start_http_server(settings)
        else:
            return False
        return True
