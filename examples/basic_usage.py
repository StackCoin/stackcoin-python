"""Basic usage of the stackcoin library."""

import asyncio
import getpass
import os

import stackcoin


async def main(token: str, base_url: str):
    async with stackcoin.Client(token, base_url=base_url) as client:
        # Who am I?
        me = await client.get_me()
        print(f"Logged in as {me.username} with balance {me.balance} STK")

        # Create a request
        req = await client.create_request(to_user_id=2, amount=100, label="pay up buddy")
        print(f"Created request #{req.request_id} to {req.responder.username} for {req.amount} STK")

        # List pending requests
        requests = await client.get_requests()
        print(f"\n{len(requests)} request(s):")
        for r in requests:
            print(f"  #{r.id} -> {r.responder.username}: {r.amount} STK ({r.status})")

        # List recent transactions
        transactions = await client.get_transactions()
        print(f"\n{len(transactions)} transaction(s):")
        for txn in transactions:
            print(f"  #{txn.id} {txn.from_.username} -> {txn.to.username}: {txn.amount} STK")

        # List users
        users = await client.get_users()
        print(f"\n{len(users)} user(s):")
        for user in users:
            print(f"  #{user.id} {user.username} ({user.balance} STK)")


if __name__ == "__main__":
    token = os.getenv("STACKCOIN_BOT_TOKEN")
    if not token:
        token = getpass.getpass("Enter your bot token: ").strip()
        if not token:
            print("Token is required")
            exit(1)

    # Can be omitted to hit production (https://stackcoin.world).
    # Set STACKCOIN_BASE_URL for local development, e.g. http://localhost:4000
    base_url = os.getenv("STACKCOIN_BASE_URL", "https://stackcoin.world")
    asyncio.run(main(token, base_url))
