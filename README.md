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

Pass a `client` to the Gateway so it can automatically catch up on missed events
via the REST API if the bot has been offline too long (>100 events). Without a
client, a `TooManyMissedEventsError` is raised and you must handle catch-up
yourself.

```python
import stackcoin

async with stackcoin.Client(token="...") as client:
    gateway = stackcoin.Gateway(token="...", client=client)

    @gateway.on("transfer.completed")
    async def on_transfer(event: stackcoin.TransferCompletedEvent):
        print(f"Transfer of {event.data.amount} STK from #{event.data.from_id} to #{event.data.to_id}")

    @gateway.on("request.accepted")
    async def on_accepted(event: stackcoin.RequestAcceptedEvent):
        print(f"Request #{event.data.request_id} accepted")

    await gateway.connect()
```

The Gateway also accepts `last_event_id` to resume from a known cursor, and
`on_event_id` as a callback to persist the cursor position after each event:

```python
gateway = stackcoin.Gateway(
    token="...",
    client=client,
    last_event_id=saved_cursor,
    on_event_id=lambda eid: save_cursor(eid),
)
```

## Examples

- `examples/basic_usage.py` -- REST client basics (balance, requests, transactions)
- `examples/simple_cli.py` -- interactive REPL with live gateway events

## Development

Models are generated from the StackCoin OpenAPI spec using `datamodel-codegen`:

```sh
STACKCOIN_ROOT=/path/to/StackCoin just generate
```

This regenerates `stackcoin/stackcoin/models.py` from `openapi.json`.
