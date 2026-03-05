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

## Examples

- `examples/basic_usage.py` -- REST client basics (balance, requests, transactions)
- `examples/simple_cli.py` -- interactive REPL with live gateway events

## Development

Models are generated from the StackCoin OpenAPI spec using `datamodel-codegen`:

```sh
STACKCOIN_ROOT=/path/to/StackCoin just generate
```

This regenerates `stackcoin/stackcoin/models.py` from `openapi.json`.
