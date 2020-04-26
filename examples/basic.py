# some hacks to work around pulling in stackcoin a directory above
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
# you don't need this in your code :)

from stackcoin import StackCoin

client = StackCoin(token="abc", user_id=123)


print(client.user())
print(client.users())
print(client.transfer(321, 10))
