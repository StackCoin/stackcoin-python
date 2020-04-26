# some hacks to work around pulling in stackcoin a directory above
import sys
import os.path

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
# you don't need this in your code :)

from stackcoin import StackCoin
from stackcoin.types import TransferSuccess

client = StackCoin(token="abc", user_id=123)


@client.notification()
def return_to_sender(event):
    """
    Once sent STK, returns to sender
    """
    print(f"Got event: {event}")
    if isinstance(event, TransferSuccess):
        print(f"Sending {event.amount} back to {event.from_id}")
        client.transfer(event.from_id, event.amount)


client.run()
