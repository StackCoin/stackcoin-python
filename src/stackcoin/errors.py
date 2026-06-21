class StackCoinError(Exception):
    """Raised on any failure to reach or get a successful response from StackCoin.

    Covers both transport-level failures (connection refused, DNS error, timeout,
    etc.) and non-2xx HTTP responses. Callers should never need to catch
    ``httpx.HTTPError`` directly — anything that goes wrong talking to StackCoin
    is funnelled through this class.

    Attributes:
        status_code: HTTP status code, or ``0`` for transport failures that never
            produced a response (``error == "transport_error"``).
        error: Short machine-readable code. ``"transport_error"`` for network faults,
            otherwise the StackCoin API's own ``error`` field (or ``http_<status>``).
        message: Human-readable detail, if available.
    """

    # Sentinel status code for failures that produced no HTTP response at all.
    TRANSPORT_STATUS: int = 0
    TRANSPORT_ERROR: str = "transport_error"

    def __init__(self, status_code: int, error: str, message: str | None = None):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"{status_code} {error}: {message}")


class TooManyMissedEventsError(StackCoinError):
    """Raised when the WebSocket gateway rejects a join due to too many missed events."""

    def __init__(self, missed_count: int, replay_limit: int, message: str):
        super().__init__(status_code=0, error="too_many_missed_events", message=message)
        self.missed_count = missed_count
        self.replay_limit = replay_limit
