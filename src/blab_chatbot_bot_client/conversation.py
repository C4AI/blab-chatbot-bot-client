from __future__ import annotations

import json
from queue import Queue
from typing import Any
from uuid import uuid4

from blab_chatbot_bot_client.data_structures import (
    OutgoingMessage,
    Message,
    MessageType,
)
from blab_chatbot_bot_client.settings_format import BlabBotClientSettings


# noinspection PyMethodMayBeStatic
class BotClientConversation:
    def __init__(
        self,
        settings: BlabBotClientSettings,
        conversation_id: str,
        bot_participant_id: str,
    ):
        self.settings = settings
        self.conversation_id = conversation_id
        self.bot_participant_id = bot_participant_id
        self._outgoing_message_queue: Queue[OutgoingMessage] = Queue()
        self.state = {}

    def enqueue_message(self, message: OutgoingMessage) -> None:
        self._outgoing_message_queue.put(message)

    def on_connect(self):
        pass

    def on_receive_message(self, message: Message) -> None:
        pass

    def on_receive_state(self, event: dict[str, Any]) -> None:
        self.state.update(event)

    def generate_answer(self, message: Message) -> list[OutgoingMessage]:
        return []

    @classmethod
    def generate_local_id(cls) -> str:
        return str(uuid4()).replace("-", "")

    @classmethod
    def generate_approval_command(
        cls, message_id: str, optional_text: str = ""
    ) -> OutgoingMessage:
        return OutgoingMessage(
            type=MessageType.TEXT,
            text=optional_text,
            command=json.dumps(dict(action="approve"), quoted_message_id=message_id),
            local_id=cls.generate_local_id(),
        )

    @classmethod
    def generate_redirection_command(
        cls, message_id: str, optional_text=""
    ) -> OutgoingMessage:
        return OutgoingMessage(
            type=MessageType.TEXT,
            text=optional_text,
            command=json.dumps(dict(action="approve"), quoted_message_id=message_id),
            local_id=cls.generate_local_id(),
        )
