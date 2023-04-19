"""Contains a class that interacts with BLAB Controller.

The actual behaviour is implemented in subclasses
(such as `WebSocketBotClientConversation`).
"""

from __future__ import annotations

from queue import Queue
from typing import TYPE_CHECKING, Any, Generic, TypeVar
from uuid import uuid4

if TYPE_CHECKING:
    from blab_chatbot_bot_client.data_structures import Message, OutgoingMessage

from blab_chatbot_bot_client.settings_format import BlabBotClientSettings

SettingsType = TypeVar("SettingsType", bound=BlabBotClientSettings)


# noinspection PyMethodMayBeStatic
class BotClientConversation(Generic[SettingsType]):
    """Represents a conversation on the client."""

    def __init__(
        self,
        settings: SettingsType,
        conversation_id: str,
        bot_participant_id: str,
    ):
        """Create an instance.

        Args:
        ----
            settings: bot settings
            conversation_id: id of the conversation
            bot_participant_id: id of the participant correspondent to the bot
        """
        self.settings = settings
        self.conversation_id = conversation_id
        self.bot_participant_id = bot_participant_id
        self._outgoing_message_queue: Queue[OutgoingMessage] = Queue()
        self.state: dict[str, Any] = {}

    def enqueue_message(self, message: OutgoingMessage) -> None:
        """Enqueue a message to be sent to the controller.

        Args:
        ----
            message: the message to be sent
        """
        self._outgoing_message_queue.put(message)

    def on_connect(self) -> None:
        """Handle the successful connection with the controller.

        This method does nothing. The behaviour is defined by subclasses.
        """

    def on_receive_message(self, message: Message) -> None:
        """Handle the arrival of a new message.

        This method does nothing. The behaviour is defined by subclasses.

        Note that this method is also called when the bot's own messages
        are delivered.

        Args:
        ----
            message: the incoming message
        """

    def on_receive_state(self, event: dict[str, Any]) -> None:
        """Handle the arrival of a new event message describing the current state.

        This method updates the internal cached state.

        Args:
        ----
            event: the event data
        """
        self.state.update(event)

    def generate_answer(self, message: Message) -> list[OutgoingMessage]:
        """Generate zero or more answers to a given message.

        This method returns an empty list.
        Subclasses should implement the desired behaviour.

        Args:
        ----
            message: the message which should be answered

        Returns:
        -------
            a list with the answers
        """
        return []

    def generate_greeting(self) -> list[OutgoingMessage]:
        """Generate zero or more greetings to the user.

        This method returns an empty list.
        Subclasses should implement the desired behaviour.

        Returns
        -------
            a list with the greetings
        """
        return []

    @classmethod
    def bot_sends_first_message(cls) -> bool:
        """Whether the bot sends the first message.

        This method returns `False` by default, but subclasses
        should override it if the bots can initiate a conversation.

        Returns
        -------
            `true` if this bot sends a greeting message to the user
            before their first message
        """
        return False

    @classmethod
    def generate_local_id(cls) -> str:
        """Generate a unique local id to a message.

        Each outgoing message should have a new local id.
        It is used by the controller to discard repeated attempts to
        send the same message after one successful delivery.
        It can also be used by bots to be notified when its own messages
        have been delivered.

        Return:
        ------
            the generated local id
        """
        return str(uuid4()).replace("-", "")
