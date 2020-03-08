import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from stackcoin import StackCoin

client = StackCoin(token="test", account_id=123)
