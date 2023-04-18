"""Contains a class that connects with BLAB Controller via WebSocket.

Bots should implement subclasses of WebSocketBotClientConversation.
"""

from __future__ import annotations

import json
from logging import getLogger
from queue import Queue
from threading import Thread
from typing import Any, TypeVar, cast

from blab_chatbot_bot_client.conversation import BotClientConversation
from blab_chatbot_bot_client.data_structures import Message, OutgoingMessage
from blab_chatbot_bot_client.settings_format import (
    BlabWebSocketBotClientSettings,
    BlabWebSocketConnectionSettings,
)

SettingsType = TypeVar("SettingsType", bound=BlabWebSocketBotClientSettings)


class WebSocketBotClientConversation(BotClientConversation[SettingsType]):
    """Represents a conversation on the client, using WebSocket."""

    def __init__(self, *args: Any, **kwargs: Any):
        """Create an instance. Arguments are forwarded to the parent class."""
        super().__init__(*args, **kwargs)
        self._outgoing_message_queue: Queue[OutgoingMessage] = Queue()

    _instances: dict[str, WebSocketBotClientConversation[SettingsType]] = {}

    # noinspection PyPackageRequirements
    @classmethod
    def start_http_server(cls, settings: SettingsType) -> None:
        """Start an HTTP server, called when there is a new conversation.

        Args:
            settings: the bot settings
        """
        from flask import Flask, request
        from waitress import serve
        from websocket import WebSocketApp

        app = Flask(__name__)
        connection_settings = cast(
            BlabWebSocketConnectionSettings, settings.BLAB_CONNECTION_SETTINGS
        )
        ws_url = connection_settings["BLAB_CONTROLLER_WS_URL"]

        @app.route("/", methods=["POST"])
        def conversation_start() -> str:
            """Handle the start of a new conversation."""
            if not isinstance(request.json, dict):
                return ""
            conversation_id = request.json["conversation_id"]
            bot_participant_id = request.json["bot_participant_id"]
            conversation = cls(settings, conversation_id, bot_participant_id)

            def on_open(
                ws_app: WebSocketApp,
                conv: WebSocketBotClientConversation[SettingsType] = conversation,
            ) -> None:
                """Handle the successful WebSocket connection.

                Args:
                    ws_app: the WebSocket app
                    conv: instance of the conversation client
                """
                conv.on_connect()

                def _process_outgoing_messages() -> None:
                    while True:
                        message = conv._outgoing_message_queue.get()
                        ws_app.send(json.dumps(message.to_dict()))

                Thread(target=_process_outgoing_messages).start()

            def on_message(
                ws_app: WebSocketApp,
                m: str,
                conv: WebSocketBotClientConversation[SettingsType] = conversation,
            ) -> None:
                """Handle a new incoming message.

                Args:
                    ws_app: the WebSocket app
                    m: the raw message data
                    conv: instance of the conversation client
                """
                contents = json.loads(m)
                if "message" in contents:
                    message = Message.from_dict(contents["message"])
                    conv.on_receive_message(message)
                if "state" in contents:
                    conv.on_receive_state(contents["state"])

            ws = WebSocketApp(
                ws_url + "/ws/chat/" + conversation_id + "/",
                cookie="sessionid=" + request.json["session"],
                on_open=on_open,
                on_message=on_message,
            )
            Thread(target=ws.run_forever).start()
            return ""

        getLogger("waitress").setLevel("INFO")

        serve(
            app,
            host=connection_settings["BOT_HTTP_SERVER_HOSTNAME"],
            port=connection_settings["BOT_HTTP_SERVER_PORT"],
        )
