from __future__ import annotations

from queue import Queue
from typing import Any
from uuid import uuid4

from blab_chatbot_bot_client.data_structures import OutgoingMessage, Message
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

    def enqueue_message(self, message: OutgoingMessage) -> None:
        self._outgoing_message_queue.put(message)

    def on_connect(self):
        pass

    def on_receive_message(self, message: Message) -> None:
        pass

    def on_receive_state(self, event: dict[str, Any]) -> None:
        pass

    def generate_answer(self, message: Message) -> list[OutgoingMessage]:
        return []

    @classmethod
    def generate_local_id(cls) -> str:
        return str(uuid4()).replace("-", "")
