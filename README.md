# stackcoin-python

Python library for the StackCoin API. Provides a typed async REST client and a WebSocket gateway for real-time events.

## Install

```sh
pip install stackcoin
```

Requires Python 3.13+. Dependencies: `httpx`, `pydantic>=2`, `websockets`.

## Quick start

```python
import asyncio
import stackcoin

async def main():
    async with stackcoin.Client(token="...") as client:
        me = await client.get_me()
        print(f"{me.username}: {me.balance} STK")

        events = await client.get_events()
        for event in events:
            print(f"[{event.type}] {event.data}")

asyncio.run(main())
```

## Gateway (real-time events)

```python
import stackcoin

gateway = stackcoin.Gateway(token="...")

@gateway.on("transfer.completed")
async def on_transfer(event: stackcoin.TransferCompletedEvent):
    print(f"Transfer of {event.data.amount} STK from #{event.data.from_id} to #{event.data.to_id}")

@gateway.on("request.accepted")
async def on_accepted(event: stackcoin.RequestAcceptedEvent):
    print(f"Request #{event.data.request_id} accepted")

await gateway.connect()
```

## Catching up on missed events

If your bot persists its cursor position and reconnects with a `last_event_id`,
the server replays up to 100 missed events. If more than 100 were missed, the
join is rejected — pass a `client` so the Gateway can automatically catch up
via the REST API. Without a client, a `TooManyMissedEventsError` is raised.

```python
async with stackcoin.Client(token="...") as client:
    gateway = stackcoin.Gateway(
        token="...",
        client=client,
        last_event_id=saved_cursor,
        on_event_id=lambda eid: save_cursor(eid),
    )

    @gateway.on("transfer.completed")
    async def on_transfer(event: stackcoin.TransferCompletedEvent):
        ...

    await gateway.connect()
```

## Examples

- `examples/basic_usage.py` -- REST client basics (balance, requests, transactions)
- `examples/simple_cli.py` -- interactive REPL with live gateway events

## Testing

Tests for this library live in the main
[StackCoin/StackCoin](https://github.com/StackCoin/StackCoin) repository as
end-to-end tests that boot a real StackCoin server:

```sh
cd /path/to/StackCoin/test/e2e/py
uv sync
uv run pytest
```

The E2E suite covers the REST client, WebSocket gateway, event pagination, and
the [LuckyPot](https://github.com/StackCoin/LuckyPot) bot integration.

## Development

Models are generated from the StackCoin OpenAPI spec using `datamodel-codegen`:

```sh
STACKCOIN_ROOT=/path/to/StackCoin just generate
```

This regenerates `src/stackcoin/models.py` from `openapi.json`.
