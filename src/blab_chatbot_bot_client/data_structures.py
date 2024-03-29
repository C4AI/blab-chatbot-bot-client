"""Contains definitions of useful data structures and enums."""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from datetime import datetime
from enum import Enum
from operator import attrgetter
from typing import Any


class MessageType(Enum):
    """Represents a message type."""

    SYSTEM = "S"
    """System message"""

    TEXT = "T"
    """Text message"""

    VOICE = "V"
    """Voice message (recorded ad hoc)"""

    AUDIO = "a"
    """Message with audio file"""

    VIDEO = "v"
    """Message with video file"""

    IMAGE = "i"
    """Message with video file"""

    ATTACHMENT = "A"
    """Message with arbitrary attachment"""


@dataclass
class Message:
    """Represents a message with data received from BLAB Controller."""

    id: str
    """Id of the message"""

    time: datetime
    """When the message was sent"""

    type: MessageType
    """Type of the message"""

    sent_by_human: bool
    """Whether the message was sent by a human user"""

    options: list[str] | None = None
    """List of options from which the user can choose, if any"""

    local_id: str | None = None
    """Local id of the message (generated by the sender)"""

    text: str | None = None
    """Text of the message, if any"""

    sender_id: str | None = None
    """Id of the message sender, if any"""

    additional_metadata: dict[str, Any] | None = None
    """Additional metadata (used in system messages)"""

    event: str | None = None
    """Event type (used in system messages instead of text)"""

    quoted_message_id: str | None = None
    """Id of the quoted message, if any"""

    def __post_init__(self) -> None:
        if isinstance(self.time, str):  # type: ignore[unreachable]
            t = self.time.replace("Z", "+00:00")  # type: ignore[unreachable]
            self.time = datetime.fromisoformat(t)
        if isinstance(self.type, str):
            self.type = MessageType(self.type)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Message:
        """Create an instance using data from a dict.

        Unknown or unsupported fields are ignored.

        Args:
            d: dictionary with the message data

        Returns:
            an instance with the provided data
        """
        supported_fields = set(map(attrgetter("name"), fields(cls)))
        return Message(**{k: v for k, v in d.items() if k in supported_fields})


@dataclass
class OutgoingMessage:
    """Represents a message that the bot will send to BLAB Controller."""

    local_id: str
    """Local id of the message (generated by the sender)"""

    type: MessageType
    """Type of the message"""

    text: str | None = None
    """Text of the message, if any"""

    quoted_message_id: str | None = None
    """Id of the quoted message, if any"""

    command: str | None = None
    """Command embedded in the message (only for manager bots)"""

    options: list[str] = field(default_factory=list)
    """List of options from which the user can choose, if any"""

    external_file_url: str | None = None
    """URL of the external file attached to the message"""

    def to_dict(self) -> dict[str, Any]:
        """Generate a dict with the data in this message.

        Returns
            a dict with the values in this instance
        """
        d: dict[str, str | list[str] | None] = {
            "local_id": self.local_id,
            "type": self.type.value,
            "text": self.text,
        }
        if self.options:
            d["options"] = self.options or []
        if self.quoted_message_id:
            d["quoted_message_id"] = self.quoted_message_id
        if self.command:
            d["command"] = self.command
        if (
            self.type
            in {
                MessageType.IMAGE,
                MessageType.VIDEO,
                MessageType.AUDIO,
                MessageType.ATTACHMENT,
            }
            and self.external_file_url
        ):
            d["external_file_url"] = self.external_file_url
        return d
