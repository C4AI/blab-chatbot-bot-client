from overrides import overrides

from blab_chatbot_bot_client.conversation_websocket import (
    WebSocketBotClientConversation,
)
from blab_chatbot_bot_client.data_structures import (
    OutgoingMessage,
    MessageType,
    Message,
)


class ExampleWebSocketBotClientConversation(WebSocketBotClientConversation):
    @overrides
    def on_connect(self):
        greeting = OutgoingMessage(
            type=MessageType.TEXT,
            text="Hello!",
            local_id=self.generate_local_id(),
        )
        self.enqueue_message(greeting)

    @overrides
    def on_receive_message(self, message: Message) -> None:
        if message.sent_by_human and message.type == MessageType.TEXT:
            answer = OutgoingMessage(
                type=MessageType.TEXT,
                text="You said: " + message.text,
                local_id=self.generate_local_id(),
            )
            self.enqueue_message(answer)
