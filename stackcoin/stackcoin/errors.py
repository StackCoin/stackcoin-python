class StackCoinError(Exception):
    """Raised when the StackCoin API returns an error response."""

    def __init__(self, status_code: int, error: str, message: str | None = None):
        self.status_code = status_code
        self.error = error
        self.message = message
        super().__init__(f"{status_code} {error}: {message}")
