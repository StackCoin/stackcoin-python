class StackCoinError(Exception):
    """Raised when the StackCoin API returns an error response."""

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
