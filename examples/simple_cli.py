import asyncio
import os
from stackcoin_python import StackCoinClient


def print_help():
    print("\nAvailable commands:")
    print("  balance - Get your bot's balance")
    print("  user <user_id> - Get a user's balance")
    print("  send <user_id> <amount> [label] - Send tokens to a user")
    print("  request <user_id> <amount> [label] - Request tokens from a user")
    print("  requests [requester|responder] - List payment requests")
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
                balance = await client.get_my_balance()
                print(f"Bot: {balance.username}, Balance: {balance.balance} STK")
            elif cmd == "user" and len(parts) >= 2:
                user_id = int(parts[1])
                balance = await client.get_balance(user_id)
                print(f"User: {balance.username}, Balance: {balance.balance} STK")
            elif cmd == "send" and len(parts) >= 3:
                user_id = int(parts[1])
                amount = int(parts[2])
                label = " ".join(parts[3:]) if len(parts) > 3 else None
                result = await client.send(user_id, amount, label)
                print(f"Sent {result.amount} STK! Your new balance: {result.from_new_balance}")
            elif cmd == "request" and len(parts) >= 3:
                user_id = int(parts[1])
                amount = int(parts[2])
                label = " ".join(parts[3:]) if len(parts) > 3 else None
                result = await client.request_payment(user_id, amount, label)
                print(f"Created request {result.request_id} for {result.amount} STK from {result.responder.username}")
            elif cmd == "requests":
                role = parts[1] if len(parts) > 1 else "requester"
                requests = await client.get_requests(role=role)
                print(f"Found {len(requests.requests)} requests as {role}:")
                for req in requests.requests[:10]:
                    if role == "requester":
                        print(f"  #{req.id}: {req.amount} STK to {req.responder.username} - {req.status}")
                    else:
                        print(f"  #{req.id}: {req.amount} STK from {req.requester.username} - {req.status}")
            elif cmd == "accept" and len(parts) >= 2:
                request_id = int(parts[1])
                result = await client.accept_request(request_id)
                print(f"Accepted request {result.request_id}, status: {result.status}")
            elif cmd == "deny" and len(parts) >= 2:
                request_id = int(parts[1])
                result = await client.deny_request(request_id)
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
    
    async with StackCoinClient(token, base_url=base_url) as client:
        await run_repl(client)


if __name__ == "__main__":
    asyncio.run(main())
