from __future__ import annotations

from dataclasses import dataclass, fields
from datetime import datetime
from enum import Enum
from operator import attrgetter
from typing import Any


class MessageType(Enum):
    SYSTEM = "S"
    TEXT = "T"
    VOICE = "V"
    AUDIO = "a"
    VIDEO = "v"
    IMAGE = "i"
    ATTACHMENT = "A"


@dataclass
class Message:
    id: str
    time: datetime
    type: MessageType
    sent_by_human: bool
    options: list[str] | None = None
    local_id: str | None = None
    text: str | None = None
    sender_id: str | None = None
    additional_metadata: dict[str, Any] | None = None
    event: str | None = None
    quoted_message_id: str | None = None

    def __post_init__(self):
        if isinstance(self.time, str):
            self.time = datetime.fromisoformat(self.time.replace("Z", "+00:00"))
        if isinstance(self.type, str):
            self.type = MessageType(self.type)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> Message:
        supported_fields = set(map(attrgetter("name"), fields(cls)))
        return Message(**{k: v for k, v in d.items() if k in supported_fields})


@dataclass
class OutgoingMessage:
    local_id: str
    type: MessageType
    text: str | None = None
    quoted_message_id: str | None = None

    def to_dict(self):
        return {
            "local_id": self.local_id,
            "type": self.type.value,
            "text": self.text,
            "quoted_message_id": self.quoted_message_id,
        }
