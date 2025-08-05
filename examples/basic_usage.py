import asyncio
import os
from stackcoin_python import StackCoinClient


async def main(token, base_url):
    """Basic usage examples for the StackCoin client."""
    async with StackCoinClient(token, base_url=base_url) as client:
        # Get bot's balance
        balance = await client.get_my_balance()
        print(f"Bot: {balance.username}")
        print(f"Balance: {balance.balance} STK")

        # Get another user's balance
        try:
            user_balance = await client.get_balance(1)
            print(f"User {user_balance.username} has {user_balance.balance} STK")
        except Exception as e:
            print(f"Could not get user balance: {e}")

        # Send tokens (commented out for safety)
        # result = await client.send(123, 10, "Test payment")
        # print(f"Sent {result.amount} STK! New balance: {result.from_new_balance}")

        # Create a payment request
        try:
            request = await client.request_payment(2, 5, "Service fee")
            print(
                f"Created payment request #{request.request_id} for {request.amount} STK"
            )
        except Exception as e:
            print(f"Could not create request: {e}")

        # List payment requests where bot is the requester
        requests = await client.get_requests(role="requester")
        print(f"You have {len(requests.requests)} outgoing requests")

        # List pending requests where bot is the responder
        pending = await client.get_requests(role="responder", status="pending")
        print(f"You have {len(pending.requests)} pending requests to respond to")

        # Accept a request (commented out for safety)
        # if pending.requests:
        #     req = pending.requests[0]
        #     result = await client.accept_request(req.id)
        #     print(f"Accepted request #{result.request_id}")


if __name__ == "__main__":
    token = os.getenv("STACKCOIN_BOT_TOKEN")
    if not token:
        token = input("Enter your bot token: ").strip()
        if not token:
            print("Token is required")
            exit(1)

    base_url = os.getenv("STACKCOIN_BASE_URL", "https://stackcoin.world")

    asyncio.run(main(token, base_url))
