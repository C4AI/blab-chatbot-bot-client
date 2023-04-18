"""Defines the expected fields of a configuration file."""

from typing import Protocol, TypedDict, runtime_checkable


class BlabConnectionSettings(TypedDict):
    """Contains settings to interact with BLAB Controller."""


class BlabWebSocketConnectionSettings(BlabConnectionSettings):
    """Contains settings to interact with BLAB Controller via WebSocket."""

    BOT_HTTP_SERVER_HOSTNAME: str
    """Address of the (usually local) HTTP server that the controller will connect to"""

    BOT_HTTP_SERVER_PORT: int
    """Port of the aforementioned server"""

    BLAB_CONTROLLER_WS_URL: str
    """BLAB Controller address for WebSocket connections"""


@runtime_checkable
class BlabBotClientSettings(Protocol):
    """Protocol of classes whose instances contain all the settings for a bot client.

    This class only contains BLAB connection settings, which are shared among all
    bot clients. Subclasses may add other fields.
    """

    BLAB_CONNECTION_SETTINGS: BlabConnectionSettings
    """Configuration parameters used to connect with BLAB Controller"""


@runtime_checkable
class BlabWebSocketBotClientSettings(BlabBotClientSettings, Protocol):
    """Protocol of classes whose instances contain all the settings for a bot client.

    This class only contains BLAB WebSocket connection settings, which are shared
    among all WebSocket bot clients. Subclasses may add other fields.
    """

    BLAB_CONNECTION_SETTINGS: BlabWebSocketConnectionSettings
    """Configuration parameters used to connect with BLAB Controller"""
