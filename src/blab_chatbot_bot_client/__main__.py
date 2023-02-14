from sys import argv

from blab_chatbot_bot_client.cli import BlabBotClientArgParser
from blab_chatbot_bot_client.conversation_example import (
    ExampleWebSocketBotClientConversation,
)

BlabBotClientArgParser(ExampleWebSocketBotClientConversation).parse_and_run(argv[1:])
