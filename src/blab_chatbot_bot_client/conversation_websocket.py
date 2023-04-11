from __future__ import annotations

import json
from logging import getLogger
from queue import Queue
from threading import Thread
from typing import Any, cast

from blab_chatbot_bot_client.conversation import BotClientConversation
from blab_chatbot_bot_client.data_structures import OutgoingMessage, Message
from blab_chatbot_bot_client.settings_format import (
    BlabBotClientSettings,
    BlabWebSocketConnectionSettings,
)


class WebSocketBotClientConversation(BotClientConversation):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self._outgoing_message_queue: Queue[OutgoingMessage] = Queue()

    _instances: dict[str, WebSocketBotClientConversation] = {}

    # noinspection PyPackageRequirements
    @classmethod
    def start_http_server(cls, settings: BlabBotClientSettings):

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
            conversation_id = request.json["conversation_id"]
            bot_participant_id = request.json["bot_participant_id"]
            conversation = cls(settings, conversation_id, bot_participant_id)

            def on_open(
                ws_app: WebSocketApp,
                conv: WebSocketBotClientConversation = conversation,
            ) -> None:
                conv.on_connect()

                def _process_outgoing_messages():
                    while True:
                        message = conv._outgoing_message_queue.get()
                        ws_app.send(json.dumps(message.to_dict()))

                Thread(target=_process_outgoing_messages).start()

            def on_message(
                ws_app: WebSocketApp,
                m: str,
                conv: WebSocketBotClientConversation = conversation,
            ) -> None:
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
