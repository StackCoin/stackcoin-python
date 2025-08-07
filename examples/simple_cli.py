import asyncio
import os
from stackcoin_python import AuthenticatedClient
from stackcoin_python.models import (
    CreateRequestParams,
    SendStkParams,
    BalanceResponse,
    CreateRequestResponse,
    RequestsResponse,
    TransactionsResponse,
    UsersResponse,
    SendStkResponse,
    RequestActionResponse,
)
from stackcoin_python.api.default import (
    stackcoin_self_balance,
    stackcoin_user_balance,
    stackcoin_users,
    stackcoin_send_stk,
    stackcoin_create_request,
    stackcoin_requests,
    stackcoin_transactions,
    stackcoin_accept_request,
    stackcoin_deny_request,
)


def print_help():
    print("\nAvailable commands:")
    print("  balance - Get your bot's balance")
    print("  user <user_id> - Get a user's balance")
    print("  users [username] - List/search users")
    print("  send <user_id> <amount> [label] - Send tokens to a user")
    print("  request <user_id> <amount> [label] - Request tokens from a user")
    print("  requests [requester|responder] - List payment requests")
    print("  transactions [from_user_id] [to_user_id] - List transactions")
    print("  accept <request_id> - Accept a payment request")
    print("  deny <request_id> - Deny a payment request")
    print("  help - Show this help")
    print("  quit - Exit the REPL")


async def run_repl(client):
    print("StackCoin Bot REPL - Type 'help' for commands")

    while True:
        try:
            command = input("\n> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == "quit":
                break
            elif cmd == "help":
                print_help()
            elif cmd == "balance":
                balance = await stackcoin_self_balance.asyncio(client=client)
                if not isinstance(balance, BalanceResponse):
                    print("Error: Failed to get balance")
                    continue
                print(f"Bot: {balance.username}, Balance: {balance.balance} STK")
            elif cmd == "user" and len(parts) >= 2:
                user_id = int(parts[1])
                balance = await stackcoin_user_balance.asyncio(client=client, user_id=user_id)
                if not isinstance(balance, BalanceResponse):
                    print("Error: Failed to get user balance")
                    continue
                print(f"User: {balance.username}, Balance: {balance.balance} STK")
            elif cmd == "users":
                username_filter = parts[1] if len(parts) > 1 else None
                users_response = await stackcoin_users.asyncio(client=client, username=username_filter)
                if not isinstance(users_response, UsersResponse) or not isinstance(users_response.users, list):
                    print("Error: Failed to get users")
                    continue
                count = 0
                print("Users:")
                for user in users_response.users:
                    status_flags = []
                    if user.admin:
                        status_flags.append("ADMIN")
                    if user.banned:
                        status_flags.append("BANNED")
                    status_str = f" [{', '.join(status_flags)}]" if status_flags else ""
                    print(
                        f"  #{user.id}: {user.username} - {user.balance} STK{status_str}"
                    )
                    count += 1
                    if count >= 20:
                        break
                print(f"Showing first {count} users")
            elif cmd == "send" and len(parts) >= 3:
                user_id = int(parts[1])
                amount = int(parts[2])
                label = " ".join(parts[3:]) if len(parts) > 3 else None
                result = await stackcoin_send_stk.asyncio(
                    client=client,
                    user_id=user_id,
                    body=SendStkParams(amount=amount, label=label)
                )
                if not isinstance(result, SendStkResponse):
                    print("Error: Failed to send STK")
                    continue
                print(
                    f"Sent {result.amount} STK! Your new balance: {result.from_new_balance}"
                )
            elif cmd == "request" and len(parts) >= 3:
                user_id = int(parts[1])
                amount = int(parts[2])
                label = " ".join(parts[3:]) if len(parts) > 3 else None
                result = await stackcoin_create_request.asyncio(
                    client=client,
                    user_id=user_id,
                    body=CreateRequestParams(amount=amount, label=label)
                )
                if not isinstance(result, CreateRequestResponse):
                    print("Error: Failed to create request")
                    continue
                print(
                    f"Created request {result.request_id} for {result.amount} STK from {result.responder.username}"
                )
            elif cmd == "requests":
                role = parts[1] if len(parts) > 1 else "requester"
                requests_response = await stackcoin_requests.asyncio(client=client, role=role)
                if not isinstance(requests_response, RequestsResponse) or not isinstance(requests_response.requests, list):
                    print("Error: Failed to get requests")
                    continue
                count = 0
                print(f"Requests as {role}:")
                for req in requests_response.requests:
                    if role == "requester":
                        print(
                            f"  #{req.id}: {req.amount} STK to {req.responder.username} - {req.status}"
                        )
                    else:
                        print(
                            f"  #{req.id}: {req.amount} STK from {req.requester.username} - {req.status}"
                        )
                    count += 1
                    if count >= 10:
                        break
                print(f"Showing first {count} requests")
            elif cmd == "transactions":
                from_user_id = (
                    int(parts[1]) if len(parts) > 1 and parts[1].isdigit() else None
                )
                to_user_id = (
                    int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
                )
                transactions_response = await stackcoin_transactions.asyncio(
                    client=client, from_user_id=from_user_id, to_user_id=to_user_id
                )
                if not isinstance(transactions_response, TransactionsResponse) or not isinstance(transactions_response.transactions, list):
                    print("Error: Failed to get transactions")
                    continue
                count = 0
                print("Recent transactions:")
                for txn in transactions_response.transactions:
                    label_str = f" ({txn.label})" if txn.label else ""
                    print(
                        f"  #{txn.id}: {txn.from_.username} → {txn.to.username} {txn.amount} STK{label_str} at {txn.time}"
                    )
                    count += 1
                    if count >= 10:
                        break
                print(f"Showing first {count} transactions")
            elif cmd == "accept" and len(parts) >= 2:
                request_id = int(parts[1])
                result = await stackcoin_accept_request.asyncio(client=client, request_id=request_id)
                if not isinstance(result, RequestActionResponse):
                    print("Error: Failed to accept request")
                    continue
                print(f"Accepted request {result.request_id}, status: {result.status}")
            elif cmd == "deny" and len(parts) >= 2:
                request_id = int(parts[1])
                result = await stackcoin_deny_request.asyncio(client=client, request_id=request_id)
                if not isinstance(result, RequestActionResponse):
                    print("Error: Failed to deny request")
                    continue
                print(f"Denied request {result.request_id}, status: {result.status}")
            else:
                print("Unknown command. Type 'help' for available commands.")

        except KeyboardInterrupt:
            break
        except ValueError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            print(f"Error: {e}")


async def main():
    token = os.getenv("STACKCOIN_BOT_TOKEN")
    if not token:
        token = input("Enter your bot token: ").strip()
        if not token:
            print("Token is required")
            return

    base_url = os.getenv("STACKCOIN_BASE_URL", "https://stackcoin.world")

    client = AuthenticatedClient(base_url=base_url, token=token)
    async with client as client:
        print(f"Connected to {base_url}")
        await run_repl(client)


if __name__ == "__main__":
    asyncio.run(main())
