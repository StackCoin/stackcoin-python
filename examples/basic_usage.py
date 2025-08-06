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
        requester_count = 0
        async for req in client.stream_requests(role="requester"):
            requester_count += 1
        print(f"You have {requester_count} outgoing requests")

        # List pending requests where bot is the responder
        pending_count = 0
        first_pending_req = None
        async for req in client.stream_requests(role="responder", status="pending"):
            if first_pending_req is None:
                first_pending_req = req
            pending_count += 1
        print(f"You have {pending_count} pending requests to respond to")

        # List recent transactions
        transaction_count = 0
        print("Recent transactions:")
        async for txn in client.stream_transactions():
            label_str = f" ({txn.label})" if txn.label else ""
            print(f"  {txn.from_.username} → {txn.to.username}: {txn.amount} STK{label_str}")
            transaction_count += 1
            if transaction_count >= 5:
                break
        print(f"Showing {transaction_count} recent transactions")

        # List top users by balance
        user_count = 0
        print("Top users by balance:")
        async for user in client.stream_users():
            status_flags = []
            if user.admin:
                status_flags.append("ADMIN")
            if user.banned:
                status_flags.append("BANNED")
            status_str = f" [{', '.join(status_flags)}]" if status_flags else ""
            print(f"  {user.username}: {user.balance} STK{status_str}")
            user_count += 1
            if user_count >= 5:
                break
        print(f"Showing top {user_count} users")

        # Accept a request (commented out for safety)
        # if first_pending_req:
        #     result = await client.accept_request(first_pending_req.id)
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
