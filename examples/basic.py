import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)

from stackcoin import StackCoin

client = StackCoin(base_url="http://localhost:3000", token="abc", user_id=123,)
print(client.user())
print(client.users())
print(client.transfer(224890702218133505, 10))
