from .exceptions import *

class StackCoin:
    def __init__(self, *, token=None, account_id=None):
        if not token:
            raise InvalidToken

        if not account_id:
            raise InvalidAccountId
