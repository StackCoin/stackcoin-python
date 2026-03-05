"""StackCoin WebSocket Gateway client."""

import asyncio
import json
from typing import Any, Callable, Awaitable

from .client import AnyEvent
from .models import Event


EventHandler = Callable[[AnyEvent], Awaitable[None]]


class Gateway:
    """WebSocket gateway for receiving real-time StackCoin events.

    Usage::

        gateway = stackcoin.Gateway(
            ws_url="ws://localhost:4000/ws",
            token="...",
        )

        @gateway.on("request.accepted")
        async def handle_accepted(event: stackcoin.RequestAcceptedEvent):
            print(event.data.request_id)

        await gateway.connect()
    """

    def __init__(
        self,
        ws_url: str,
        token: str,
        last_event_id: int = 0,
        on_event_id: Callable[[int], None] | None = None,
    ):
        # ws_url should be the full websocket URL like "ws://localhost:4000/ws"
        self._ws_url = ws_url.rstrip("/")
        self._token = token
        self._handlers: dict[str, list[EventHandler]] = {}
        self._last_event_id = last_event_id
        self._on_event_id = on_event_id  # callback to persist cursor position
        self._ws = None
        self._running = False
        self._ref_counter = 0

    @property
    def last_event_id(self) -> int:
        return self._last_event_id

    def on(self, event_type: str) -> Callable[[EventHandler], EventHandler]:
        """Decorator to register an event handler."""

        def decorator(func: EventHandler) -> EventHandler:
            self.register_handler(event_type, func)
            return func

        return decorator

    def register_handler(self, event_type: str, handler: EventHandler) -> None:
        """Register an event handler programmatically."""
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def connect(self) -> None:
        """Connect and listen for events. Reconnects automatically on failure."""
        import websockets

        self._running = True

        while self._running:
            try:
                url = f"{self._ws_url}?token={self._token}&vsn=2.0.0"

                async with websockets.connect(url) as ws:
                    self._ws = ws
                    await self._join_channel(ws)

                    heartbeat_task = asyncio.create_task(self._heartbeat(ws))
                    try:
                        async for raw_msg in ws:
                            msg = json.loads(raw_msg)
                            await self._handle_message(msg)
                    finally:
                        heartbeat_task.cancel()

            except Exception:
                if self._running:
                    await asyncio.sleep(5)

    async def _join_channel(self, ws: Any) -> None:
        """Join the user:self channel with event replay."""
        self._ref_counter += 1
        join_msg = json.dumps(
            [
                None,
                str(self._ref_counter),
                "user:self",
                "phx_join",
                {"last_event_id": self._last_event_id},
            ]
        )
        await ws.send(join_msg)

        reply = json.loads(await asyncio.wait_for(ws.recv(), timeout=10))
        if not (reply[3] == "phx_reply" and reply[4].get("status") == "ok"):
            raise ConnectionError(f"Failed to join channel: {reply}")

    async def _heartbeat(self, ws: Any) -> None:
        """Send periodic heartbeats."""
        while True:
            await asyncio.sleep(30)
            self._ref_counter += 1
            hb = json.dumps([None, str(self._ref_counter), "phoenix", "heartbeat", {}])
            await ws.send(hb)

    async def _handle_message(self, msg: list[Any]) -> None:
        """Dispatch incoming message to registered handlers."""
        if len(msg) < 5:
            return

        event_name = msg[3]
        payload = msg[4]

        if event_name == "event":
            # Parse via discriminated union RootModel, then unwrap
            typed_event = Event.model_validate(payload).root

            if typed_event.id > self._last_event_id:
                self._last_event_id = typed_event.id

            for handler in self._handlers.get(typed_event.type, []):
                try:
                    await handler(typed_event)
                except Exception:
                    pass

            if typed_event.id > 0 and self._on_event_id:
                try:
                    self._on_event_id(typed_event.id)
                except Exception:
                    pass

    def stop(self) -> None:
        """Signal the gateway to stop."""
        self._running = False
