"""Async REST client for the StackCoin API."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import StackCoinError
from .models import (
    CreateRequestResponse,
    DiscordBotResponse,
    DiscordGuild,
    DiscordGuildsResponse,
    EventsResponse,
    Request,
    RequestAcceptedEvent,
    RequestActionResponse,
    RequestCreatedEvent,
    RequestDeniedEvent,
    RequestsResponse,
    SendStkResponse,
    Transaction,
    TransactionsResponse,
    TransferCompletedEvent,
    User,
    UsersResponse,
)

# Union of all concrete event types (unwrapped from Event RootModel)
AnyEvent = TransferCompletedEvent | RequestCreatedEvent | RequestAcceptedEvent | RequestDeniedEvent


class Client:
    """Async client for the StackCoin REST API.

    Usage::

        async with Client(token="sk-...") as client:
            me = await client.get_me()
            print(me.username, me.balance)
    """

    def __init__(
        self,
        token: str,
        *,
        base_url: str = "https://stackcoin.world",
        timeout: float = 10.0,
    ) -> None:
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            },
            timeout=timeout,
        )

    async def __aenter__(self) -> Client:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying HTTP connection pool."""
        await self._http.aclose()

    @staticmethod
    def _raise_for_error(resp: httpx.Response) -> None:
        """Raise :class:`StackCoinError` on any 4xx/5xx response."""
        if resp.status_code >= 400:
            try:
                body = resp.json()
            except Exception:
                body = {}
            error = body.get("error", f"http_{resp.status_code}")
            message = body.get("message")
            raise StackCoinError(resp.status_code, error, message)

    async def get_me(self) -> User:
        """Return the authenticated user's profile."""
        resp = await self._http.get("/api/user/me")
        self._raise_for_error(resp)
        return User.model_validate(resp.json())

    async def get_user(self, user_id: int) -> User:
        """Return a user by their ID."""
        resp = await self._http.get(f"/api/user/{user_id}")
        self._raise_for_error(resp)
        return User.model_validate(resp.json())

    async def get_users(self, *, discord_id: str | None = None) -> list[User]:
        """Return a list of users, optionally filtered by Discord ID."""
        params: dict[str, Any] = {}
        if discord_id is not None:
            params["discord_id"] = discord_id
        resp = await self._http.get("/api/users", params=params)
        self._raise_for_error(resp)
        wrapper = UsersResponse.model_validate(resp.json())
        return wrapper.users or []

    async def send(
        self,
        to_user_id: int,
        amount: int,
        *,
        label: str | None = None,
        idempotency_key: str | None = None,
    ) -> SendStkResponse:
        """Send STK to another user."""
        body: dict[str, Any] = {"amount": amount}
        if label is not None:
            body["label"] = label
        headers: dict[str, str] = {}
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        resp = await self._http.post(
            f"/api/user/{to_user_id}/send",
            json=body,
            headers=headers,
        )
        self._raise_for_error(resp)
        return SendStkResponse.model_validate(resp.json())

    async def create_request(
        self,
        to_user_id: int,
        amount: int,
        *,
        label: str | None = None,
        idempotency_key: str | None = None,
        use_preauth: bool = False,
    ) -> CreateRequestResponse:
        """Create a STK request to another user."""
        body: dict[str, Any] = {"amount": amount}
        if label is not None:
            body["label"] = label
        if use_preauth:
            body["use_preauth"] = True
        headers: dict[str, str] = {}
        if idempotency_key is not None:
            headers["Idempotency-Key"] = idempotency_key
        resp = await self._http.post(
            f"/api/user/{to_user_id}/request",
            json=body,
            headers=headers,
        )
        self._raise_for_error(resp)
        return CreateRequestResponse.model_validate(resp.json())

    async def create_preauth(
        self,
        user_id: int,
        max_amount: int,
        window_hours: int,
    ) -> dict:
        """Request a preauthorization from a user."""
        resp = await self._http.post(
            f"/api/user/{user_id}/preauth",
            json={"max_amount": max_amount, "window_hours": window_hours},
        )
        self._raise_for_error(resp)
        return resp.json()

    async def get_preauths(self, *, user_id: int | None = None) -> list[dict]:
        """List preauths for this bot, optionally filtered by user_id."""
        params: dict[str, Any] = {}
        if user_id is not None:
            params["user_id"] = user_id
        resp = await self._http.get("/api/preauths", params=params)
        self._raise_for_error(resp)
        return resp.json().get("preauths", [])

    async def get_request(self, request_id: int) -> Request:
        """Return a single request by its ID."""
        resp = await self._http.get(f"/api/request/{request_id}")
        self._raise_for_error(resp)
        return Request.model_validate(resp.json())

    async def get_requests(self, *, status: str | None = None) -> list[Request]:
        """Return requests for the authenticated user, optionally filtered by status."""
        params: dict[str, Any] = {}
        if status is not None:
            params["status"] = status
        resp = await self._http.get("/api/requests", params=params)
        self._raise_for_error(resp)
        wrapper = RequestsResponse.model_validate(resp.json())
        return wrapper.requests or []

    async def accept_request(self, request_id: int) -> RequestActionResponse:
        """Accept a pending STK request."""
        resp = await self._http.post(f"/api/requests/{request_id}/accept")
        self._raise_for_error(resp)
        return RequestActionResponse.model_validate(resp.json())

    async def deny_request(self, request_id: int) -> RequestActionResponse:
        """Deny a pending STK request."""
        resp = await self._http.post(f"/api/requests/{request_id}/deny")
        self._raise_for_error(resp)
        return RequestActionResponse.model_validate(resp.json())

    async def get_transactions(self) -> list[Transaction]:
        """Return transactions for the authenticated user."""
        resp = await self._http.get("/api/transactions")
        self._raise_for_error(resp)
        wrapper = TransactionsResponse.model_validate(resp.json())
        return wrapper.transactions or []

    async def get_transaction(self, transaction_id: int) -> Transaction:
        """Return a single transaction by its ID."""
        resp = await self._http.get(f"/api/transaction/{transaction_id}")
        self._raise_for_error(resp)
        return Transaction.model_validate(resp.json())

    async def get_events(self, *, since_id: int = 0) -> list[AnyEvent]:
        """Return typed events since the given ID.

        Automatically paginates through all available events.
        """
        all_events: list[AnyEvent] = []
        cursor = since_id

        while True:
            params: dict[str, Any] = {}
            if cursor > 0:
                params["since_id"] = cursor
            resp = await self._http.get("/api/events", params=params)
            self._raise_for_error(resp)
            wrapper = EventsResponse.model_validate(resp.json())
            page = [e.root for e in wrapper.events]
            all_events.extend(page)

            if not wrapper.has_more or not page:
                break
            cursor = page[-1].id

        return all_events

    async def get_discord_bot_id(self) -> str:
        """Return the Discord user ID of the StackCoin bot."""
        resp = await self._http.get("/api/discord/bot")
        self._raise_for_error(resp)
        bot = DiscordBotResponse.model_validate(resp.json())
        return bot.discord_id

    async def get_discord_guilds(self) -> list[DiscordGuild]:
        """Return all Discord guilds."""
        resp = await self._http.get("/api/discord/guilds")
        self._raise_for_error(resp)
        wrapper = DiscordGuildsResponse.model_validate(resp.json())
        return wrapper.guilds or []

    async def get_discord_guild(self, snowflake: str) -> DiscordGuild:
        """Return a single Discord guild by its snowflake ID."""
        resp = await self._http.get(f"/api/discord/guild/{snowflake}")
        self._raise_for_error(resp)
        return DiscordGuild.model_validate(resp.json())
