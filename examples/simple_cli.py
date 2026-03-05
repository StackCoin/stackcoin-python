"""Interactive StackCoin bot REPL with live gateway events.

Demonstrates the REST client and WebSocket gateway working together:
the REPL handles commands while the gateway prints real-time events
in the background.
"""

import asyncio
import os
import sys

import stackcoin


def print_help():
    print("\nAvailable commands:")
    print("  balance              - Get your bot's balance")
    print("  user <id>            - Get a user by ID")
    print("  users [discord_id]   - List/search users")
    print("  send <id> <amt> [label]    - Send STK to a user")
    print("  request <id> <amt> [label] - Request STK from a user")
    print("  requests [status]    - List payment requests")
    print("  accept <request_id>  - Accept a payment request")
    print("  deny <request_id>    - Deny a payment request")
    print("  transactions         - List recent transactions")
    print("  events [since_id]    - List recent events (REST)")
    print("  help                 - Show this help")
    print("  quit                 - Exit")


async def handle_command(client: stackcoin.Client, line: str):
    parts = line.split()
    cmd = parts[0].lower()

    if cmd == "help":
        print_help()

    elif cmd == "balance":
        me = await client.get_me()
        print(f"{me.username}: {me.balance} STK")

    elif cmd == "user" and len(parts) >= 2:
        user = await client.get_user(int(parts[1]))
        flags = []
        if user.admin:
            flags.append("ADMIN")
        if user.banned:
            flags.append("BANNED")
        flag_str = f" [{', '.join(flags)}]" if flags else ""
        print(f"#{user.id} {user.username}: {user.balance} STK{flag_str}")

    elif cmd == "users":
        discord_id = parts[1] if len(parts) > 1 else None
        users = await client.get_users(discord_id=discord_id)
        for u in users[:20]:
            print(f"  #{u.id} {u.username}: {u.balance} STK")
        print(f"({len(users)} total)")

    elif cmd == "send" and len(parts) >= 3:
        user_id = int(parts[1])
        amount = int(parts[2])
        label = " ".join(parts[3:]) or None
        result = await client.send(user_id, amount, label=label)
        print(f"Sent {result.amount} STK (txn #{result.transaction_id}). "
              f"Your balance: {result.from_new_balance} STK")

    elif cmd == "request" and len(parts) >= 3:
        user_id = int(parts[1])
        amount = int(parts[2])
        label = " ".join(parts[3:]) or None
        result = await client.create_request(user_id, amount, label=label)
        print(f"Request #{result.request_id} for {result.amount} STK "
              f"from {result.responder.username} ({result.status})")

    elif cmd == "requests":
        status = parts[1] if len(parts) > 1 else None
        reqs = await client.get_requests(status=status)
        for r in reqs[:10]:
            print(f"  #{r.id} {r.requester.username} -> {r.responder.username}: "
                  f"{r.amount} STK ({r.status})")
        print(f"({len(reqs)} total)")

    elif cmd == "accept" and len(parts) >= 2:
        result = await client.accept_request(int(parts[1]))
        print(f"Accepted request #{result.request_id} -> {result.status}")

    elif cmd == "deny" and len(parts) >= 2:
        result = await client.deny_request(int(parts[1]))
        print(f"Denied request #{result.request_id} -> {result.status}")

    elif cmd == "transactions":
        txns = await client.get_transactions()
        for t in txns[:10]:
            label_str = f" ({t.label})" if t.label else ""
            print(f"  #{t.id} {t.from_.username} -> {t.to.username}: "
                  f"{t.amount} STK{label_str}")
        print(f"({len(txns)} total)")

    elif cmd == "events":
        since = int(parts[1]) if len(parts) > 1 else 0
        events = await client.get_events(since_id=since)
        for e in events[:10]:
            print(f"  [{e['id']}] {e['type']}: {e['data']}")
        print(f"({len(events)} total)")

    else:
        print("Unknown command. Type 'help' for available commands.")


async def read_stdin_lines(queue: asyncio.Queue[str | None]):
    """Read lines from stdin in a thread and push them into a queue."""
    loop = asyncio.get_event_loop()
    while True:
        line = await loop.run_in_executor(None, sys.stdin.readline)
        if not line:
            await queue.put(None)
            break
        await queue.put(line.strip())


async def main():
    token = os.getenv("STACKCOIN_BOT_TOKEN")
    if not token:
        token = input("Enter your bot token: ").strip()
        if not token:
            print("Token is required")
            return

    base_url = os.getenv("STACKCOIN_BASE_URL", "https://stackcoin.world")
    ws_url = os.getenv("STACKCOIN_WS_URL",
                        base_url.replace("https://", "wss://")
                                .replace("http://", "ws://")
                        + "/ws")

    async with stackcoin.Client(base_url=base_url, token=token) as client:
        me = await client.get_me()
        print(f"Connected to {base_url} as {me.username} ({me.balance} STK)")

        # Set up gateway for live events
        gateway = stackcoin.Gateway(ws_url=ws_url, token=token)

        @gateway.on("transfer.completed")
        async def on_transfer(event: stackcoin.Event):
            d = event.data
            role = d.get("role", "?")
            if role == "sender":
                print(f"\n  [event] Sent {d['amount']} STK to user #{d['to_id']}")
            else:
                print(f"\n  [event] Received {d['amount']} STK from user #{d['from_id']}")
            print("> ", end="", flush=True)

        @gateway.on("request.created")
        async def on_request_created(event: stackcoin.Event):
            d = event.data
            print(f"\n  [event] New request #{d['request_id']} for {d['amount']} STK")
            print("> ", end="", flush=True)

        @gateway.on("request.accepted")
        async def on_request_accepted(event: stackcoin.Event):
            d = event.data
            print(f"\n  [event] Request #{d['request_id']} accepted")
            print("> ", end="", flush=True)

        @gateway.on("request.denied")
        async def on_request_denied(event: stackcoin.Event):
            d = event.data
            print(f"\n  [event] Request #{d['request_id']} denied")
            print("> ", end="", flush=True)

        # Run gateway in background
        gateway_task = asyncio.create_task(gateway.connect())

        # REPL loop using async stdin reader
        input_queue: asyncio.Queue[str | None] = asyncio.Queue()
        reader_task = asyncio.create_task(read_stdin_lines(input_queue))

        print_help()
        print("\nLive events from the gateway will appear inline.\n")

        try:
            while True:
                print("> ", end="", flush=True)
                line = await input_queue.get()
                if line is None:
                    break
                if not line:
                    continue
                if line.lower() == "quit":
                    break
                try:
                    await handle_command(client, line)
                except stackcoin.StackCoinError as e:
                    print(f"API error: {e}")
                except ValueError as e:
                    print(f"Invalid input: {e}")
        except KeyboardInterrupt:
            pass
        finally:
            gateway.stop()
            gateway_task.cancel()
            reader_task.cancel()
            print("\nBye!")


if __name__ == "__main__":
    asyncio.run(main())
