from typing import Protocol, TypedDict, runtime_checkable


class BlabConnectionSettings(TypedDict):
    pass


class BlabWebSocketConnectionSettings(TypedDict):
    BOT_HTTP_SERVER_HOSTNAME: str
    BOT_HTTP_SERVER_PORT: int
    BLAB_CONTROLLER_WS_URL: str


@runtime_checkable
class BlabBotClientSettings(Protocol):
    BLAB_CONNECTION_SETTINGS: BlabConnectionSettings
