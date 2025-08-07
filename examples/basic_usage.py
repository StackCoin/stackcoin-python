import asyncio
import os
from stackcoin_python import AuthenticatedClient
from stackcoin_python.models import (
    CreateRequestParams,
    BalanceResponse,
    CreateRequestResponse,
    RequestsResponse,
    TransactionsResponse,
    UsersResponse,
)
from stackcoin_python.api.default import (
    stackcoin_self_balance,
    stackcoin_create_request,
    stackcoin_users,
    stackcoin_requests,
    stackcoin_transactions,
)


async def main(token, base_url):
    client = AuthenticatedClient(base_url=base_url, token=token)

    async with client as client:
        print("Getting balance")

        my_balance = await stackcoin_self_balance.asyncio(client=client)

        if not isinstance(my_balance, BalanceResponse):
            raise Exception("Failed to get balance")

        print(f"Logged in as {my_balance.username} with balance {my_balance.balance}")

        print("Creating request")

        request = await stackcoin_create_request.asyncio(
            client=client,
            user_id=2,
            body=CreateRequestParams(
                amount=100,
                label="pay up buddy",
            ),
        )

        if not isinstance(request, CreateRequestResponse):
            raise Exception("Failed to create request")

        print(
            f"Created request {request.request_id} to {request.responder.username} with amount {request.amount}"
        )

        print("Getting requests")

        requests = await stackcoin_requests.asyncio(client=client)

        if not isinstance(requests, RequestsResponse):
            raise Exception("Failed to get requests")

        if not isinstance(requests.requests, list):
            raise Exception("Failed to get requests")

        for request in requests.requests:
            print(
                f"Request {request.id} to {request.responder.username} with amount {request.amount}"
            )

        print("Getting transactions")

        transactions = await stackcoin_transactions.asyncio(client=client)

        if not isinstance(transactions, TransactionsResponse):
            raise Exception("Failed to get transactions")

        if not isinstance(transactions.transactions, list):
            raise Exception("Failed to get transactions")

        for transaction in transactions.transactions:
            print(
                f"Transaction {transaction.id} from {transaction.from_.username} to {transaction.to.username} with amount {transaction.amount}"
            )

        print("Getting users")

        users = await stackcoin_users.asyncio(client=client)

        if not isinstance(users, UsersResponse):
            raise Exception("Failed to get users")

        if not isinstance(users.users, list):
            raise Exception("Failed to get users")

        for user in users.users:
            print(f"User {user.id} {user.username}")


if __name__ == "__main__":
    token = os.getenv("STACKCOIN_BOT_TOKEN")
    if not token:
        token = input("Enter your bot token: ").strip()
        if not token:
            print("Token is required")
            exit(1)

    base_url = os.getenv("STACKCOIN_BASE_URL", "https://stackcoin.world")

    asyncio.run(main(token, base_url))
