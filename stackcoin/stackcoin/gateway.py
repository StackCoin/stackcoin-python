"""StackCoin WebSocket Gateway client."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from .client import AnyEvent
from .models import Event

if TYPE_CHECKING:
    from .client import Client

EventHandler = Callable[[AnyEvent], Awaitable[None]]


class Gateway:
    """WebSocket gateway for receiving real-time StackCoin events.

    Usage::

        async with stackcoin.Client(token="...") as client:
            gateway = stackcoin.Gateway(token="...", client=client)

            @gateway.on("request.accepted")
            async def handle_accepted(event: stackcoin.RequestAcceptedEvent):
                print(event.data.request_id)

            await gateway.connect()

    If a ``client`` is provided and the bot has been offline too long (>100
    missed events), the gateway automatically catches up via the REST API
    before reconnecting.  Without a ``client``, the error is raised to the
    caller.
    """

    def __init__(
        self,
        token: str,
        *,
        ws_url: str = "wss://stackcoin.world/ws",
        client: Client | None = None,
        last_event_id: int = 0,
        on_event_id: Callable[[int], None] | None = None,
    ):
        self._ws_url = ws_url.rstrip("/")
        self._token = token
        self._client = client
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
        """Connect and listen for events. Reconnects automatically on failure.

        If the gateway rejects a join because too many events were missed
        and a ``client`` was provided, the gateway catches up via the REST
        API and reconnects.  Without a ``client``, raises
        :class:`TooManyMissedEventsError`.
        """
        import websockets

        from .errors import TooManyMissedEventsError

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

            except TooManyMissedEventsError:
                if self._client is None:
                    raise  # No client — caller must handle catch-up
                await self._catch_up_via_rest()
                # Loop back to reconnect with updated cursor
            except Exception:
                if self._running:
                    await asyncio.sleep(5)

    async def _catch_up_via_rest(self) -> None:
        """Paginate through missed events via the REST API.

        Dispatches each event through the registered handlers, exactly
        as if it arrived over the WebSocket.
        """
        assert self._client is not None
        events = await self._client.get_events(since_id=self._last_event_id)
        for event in events:
            await self._dispatch_event(event)

    async def _dispatch_event(self, typed_event: AnyEvent) -> None:
        """Dispatch a typed event to registered handlers and update the cursor."""
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

    async def _join_channel(self, ws: Any) -> None:
        """Join the user:self channel with event replay."""
        from .errors import TooManyMissedEventsError

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
        if reply[3] == "phx_reply" and reply[4].get("status") == "ok":
            return

        # Check for too_many_missed_events rejection
        response = reply[4].get("response", {})
        if response.get("reason") == "too_many_missed_events":
            raise TooManyMissedEventsError(
                missed_count=response.get("missed_count", 0),
                replay_limit=response.get("replay_limit", 0),
                message=response.get("message", "Too many missed events"),
            )

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
            await self._dispatch_event(typed_event)

    def stop(self) -> None:
        """Signal the gateway to stop."""
        self._running = False
