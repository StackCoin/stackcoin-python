# Core exceptions


class StackCoinException(Exception):
    pass


class UnexpectedState(StackCoinException):
    pass


# ws(s)://


class WebSocketError(StackCoinException):
    pass


class UnknownWSState(WebSocketError):
    pass


class ClosedWS(WebSocketError):
    pass


# http(s)://


class RequestError(StackCoinException):
    pass


class AuthenticationFailure(RequestError):
    pass


class TransferFailure(RequestError):
    pass
