from typing import Optional, AsyncGenerator
import httpx
from .models import (
    BalanceResponse,
    SendResponse,
    RequestResponse,
    RequestsResponse,
    RequestActionResponse,
    PaymentRequest,
    Transaction,
    TransactionsResponse,
    UserInfo,
    UsersResponse,
)


class StackCoinClient:
    """
    Async client for interacting with the StackCoin Bot API.

    This client provides methods to manage bot balances, send/request payments,
    view transactions, and manage payment requests. Must be used as an async
    context manager.

    Args:
        token: Bot authentication token (required)
        base_url: API base URL (default: "https://stackcoin.world")
        **kwargs: Additional arguments passed to httpx.AsyncClient

    Raises:
        ValueError: If token is None or empty string

    Example:
        async with StackCoinClient("your_bot_token") as client:
            balance = await client.get_my_balance()
            print(f"Bot balance: {balance.balance} STK")
    """

    def __init__(self, token: str, base_url: str = "https://stackcoin.world", **kwargs):
        if token is None or token == "":
            raise ValueError("Token is required")

        self.token = token
        self.base_url = base_url.rstrip("/")
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }
        self._client_kwargs = kwargs
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(headers=self.headers, **self._client_kwargs)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    def _handle_response(self, response: httpx.Response) -> dict:
        """Handle HTTP response and raise for status while preserving response JSON for debugging."""
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Include response JSON in the error for debugging
            try:
                error_json = response.json()
                error_msg = f"HTTP {response.status_code}: {error_json}"
            except (ValueError, TypeError):
                # Fallback if response is not JSON
                error_msg = f"HTTP {response.status_code}: {response.text}"

            raise httpx.HTTPStatusError(
                error_msg, request=e.request, response=e.response
            )

        return response.json()

    async def get_my_balance(self) -> BalanceResponse:
        """
        Get the bot's current balance and username.

        Returns:
            BalanceResponse: Object containing the bot's balance (in tokens) and username

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails

        Example:
            balance = await client.get_my_balance()
            print(f"Bot: {balance.username}, Balance: {balance.balance} STK")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.get(f"{self.base_url}/api/bot/self/balance")
        response_data = self._handle_response(response)
        return BalanceResponse.model_validate(response_data)

    async def get_balance(self, user_id: int) -> BalanceResponse:
        """
        Get another user's balance and username by their user ID.

        Args:
            user_id: The ID of the user whose balance to retrieve

        Returns:
            BalanceResponse: Object containing the user's balance (in tokens) and username

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails (e.g., user not found)

        Example:
            user_balance = await client.get_balance(123)
            print(f"User {user_balance.username} has {user_balance.balance} STK")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.get(
            f"{self.base_url}/api/bot/user/{user_id}/balance"
        )
        response_data = self._handle_response(response)
        return BalanceResponse.model_validate(response_data)

    async def send(
        self, to_user_id: int, amount: int, label: Optional[str] = None
    ) -> SendResponse:
        """
        Send tokens from the bot's balance to another user.

        Args:
            to_user_id: ID of the user to send tokens to
            amount: Number of tokens to send (must be positive)
            label: Optional description for the transaction

        Returns:
            SendResponse: Object containing transaction details and updated balances

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails (e.g., insufficient balance,
                                 user not found, invalid amount)

        Example:
            result = await client.send(123, 50, "Payment for services")
            print(f"Sent {result.amount} STK! New balance: {result.from_new_balance}")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        data = {"amount": amount}
        if label:
            data["label"] = label

        response = await self._client.post(
            f"{self.base_url}/api/bot/user/{to_user_id}/send", json=data
        )
        response_data = self._handle_response(response)
        return SendResponse.model_validate(response_data)

    async def request_payment(
        self, from_user_id: int, amount: int, label: Optional[str] = None
    ) -> RequestResponse:
        """
        Create a payment request asking another user to pay the bot.

        This creates a pending payment request that the target user can accept or deny.
        The bot acts as the requester and the target user as the responder.

        Args:
            from_user_id: ID of the user to request payment from
            amount: Number of tokens to request (must be positive)
            label: Optional description for the payment request

        Returns:
            RequestResponse: Object containing the created request details

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails (e.g., user not found,
                                 invalid amount)

        Example:
            request = await client.request_payment(123, 25, "Service fee")
            print(f"Created request #{request.request_id} for {request.amount} STK")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        data = {"amount": amount}
        if label:
            data["label"] = label

        response = await self._client.post(
            f"{self.base_url}/api/bot/user/{from_user_id}/request", json=data
        )
        response_data = self._handle_response(response)
        return RequestResponse.model_validate(response_data)

    async def get_requests(
        self,
        role: Optional[str] = None,
        status: Optional[str] = None,
        discord_id: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
    ) -> RequestsResponse:
        """
        Get payment requests for the bot with pagination and filtering.

        Args:
            role: Filter by bot's role - "requester" (bot requested payment) or
                 "responder" (bot received payment request). Default: "requester"
            status: Filter by request status - "pending", "accepted", "denied", or "expired"
            discord_id: Filter by Discord ID of the other party (requester or responder,
                       depending on the role parameter)
            page: Page number to retrieve (1-based)
            limit: Number of requests per page (max 100)

        Returns:
            RequestsResponse: Object containing list of requests and pagination info

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails

        Example:
            # Get pending requests where bot is the responder
            pending = await client.get_requests(role="responder", status="pending")
            print(f"Found {len(pending.requests)} pending requests")

            # Get requests made to Discord user 123456789
            discord_requests = await client.get_requests(role="requester", discord_id=123456789)
            print(f"Found {len(discord_requests.requests)} requests to Discord user")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if role:
            params["role"] = role
        if status:
            params["status"] = status
        if discord_id is not None:
            params["discord_id"] = discord_id

        response = await self._client.get(
            f"{self.base_url}/api/bot/requests", params=params
        )
        response_data = self._handle_response(response)
        return RequestsResponse.model_validate(response_data)

    async def stream_requests(
        self,
        role: Optional[str] = None,
        status: Optional[str] = None,
        discord_id: Optional[int] = None,
        limit: int = 20,
    ) -> AsyncGenerator[PaymentRequest, None]:
        """
        Stream all payment requests for the bot, handling pagination automatically.

        This async generator yields individual PaymentRequest objects across all pages,
        making it easy to iterate over all requests without manual pagination handling.

        Args:
            role: Filter by bot's role - "requester" or "responder". Default: "requester"
            status: Filter by request status - "pending", "accepted", "denied", or "expired"
            discord_id: Filter by Discord ID of the other party (requester or responder,
                       depending on the role parameter)
            limit: Number of requests to fetch per API call (affects performance, not results)

        Yields:
            PaymentRequest: Individual payment request objects

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If any API request fails

        Example:
            # Process all pending requests where bot is responder
            async for request in client.stream_requests(role="responder", status="pending"):
                print(f"Request #{request.id}: {request.amount} STK from {request.requester.username}")

            # Process requests made to Discord user 123456789
            async for request in client.stream_requests(role="requester", discord_id=123456789):
                print(f"Request #{request.id}: {request.amount} STK to Discord user")
        """
        page = 1
        while True:
            response = await self.get_requests(
                role=role, status=status, discord_id=discord_id, page=page, limit=limit
            )

            for request in response.requests:
                yield request

            if not response.pagination or page >= response.pagination.total_pages:
                break

            page += 1

    async def get_transactions(
        self,
        from_user_id: Optional[int] = None,
        to_user_id: Optional[int] = None,
        from_discord_id: Optional[int] = None,
        to_discord_id: Optional[int] = None,
        includes_discord_id: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
    ) -> TransactionsResponse:
        """
        Get transaction history for the bot with pagination and filtering.

        Args:
            from_user_id: Filter transactions sent FROM this user ID to the bot
            to_user_id: Filter transactions sent FROM the bot TO this user ID
            from_discord_id: Filter transactions sent by this Discord ID
            to_discord_id: Filter transactions sent to this Discord ID
            includes_discord_id: Filter transactions where either sender OR recipient matches this Discord ID
            page: Page number to retrieve (1-based)
            limit: Number of transactions per page (max 100)

        Returns:
            TransactionsResponse: Object containing list of transactions and pagination info

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails

        Example:
            # Get transactions where bot sent tokens to user 123
            sent_txns = await client.get_transactions(to_user_id=123)
            print(f"Found {len(sent_txns.transactions)} transactions sent to user 123")

            # Get transactions sent by Discord user 123456789
            discord_sent = await client.get_transactions(from_discord_id=123456789)
            print(f"Found {len(discord_sent.transactions)} transactions from Discord user")

            # Get all transactions involving Discord user 123456789
            all_discord = await client.get_transactions(includes_discord_id=123456789)
            print(f"Found {len(all_discord.transactions)} transactions involving Discord user")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if from_user_id:
            params["from_user_id"] = from_user_id
        if to_user_id:
            params["to_user_id"] = to_user_id
        if from_discord_id is not None:
            params["from_discord_id"] = from_discord_id
        if to_discord_id is not None:
            params["to_discord_id"] = to_discord_id
        if includes_discord_id is not None:
            params["includes_discord_id"] = includes_discord_id

        response = await self._client.get(
            f"{self.base_url}/api/bot/transactions", params=params
        )
        response_data = self._handle_response(response)
        return TransactionsResponse.model_validate(response_data)

    async def stream_transactions(
        self,
        from_user_id: Optional[int] = None,
        to_user_id: Optional[int] = None,
        from_discord_id: Optional[int] = None,
        to_discord_id: Optional[int] = None,
        includes_discord_id: Optional[int] = None,
        limit: int = 20,
    ) -> AsyncGenerator[Transaction, None]:
        """
        Stream all transactions for the bot, handling pagination automatically.

        This async generator yields individual Transaction objects across all pages,
        making it easy to iterate over transaction history without manual pagination.

        Args:
            from_user_id: Filter transactions sent FROM this user ID to the bot
            to_user_id: Filter transactions sent FROM the bot TO this user ID
            from_discord_id: Filter transactions sent by this Discord ID
            to_discord_id: Filter transactions sent to this Discord ID
            includes_discord_id: Filter transactions where either sender OR recipient matches this Discord ID
            limit: Number of transactions to fetch per API call (affects performance, not results)

        Yields:
            Transaction: Individual transaction objects with sender, recipient, amount, and timestamp

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If any API request fails

        Example:
            # Process all transactions involving the bot
            async for txn in client.stream_transactions():
                print(f"{txn.from_.username} → {txn.to.username}: {txn.amount} STK")

            # Process transactions sent by Discord user 123456789
            async for txn in client.stream_transactions(from_discord_id=123456789):
                print(f"Discord user sent: {txn.amount} STK to {txn.to.username}")

            # Process all transactions involving Discord user 123456789
            async for txn in client.stream_transactions(includes_discord_id=123456789):
                print(f"Transaction: {txn.from_.username} → {txn.to.username}: {txn.amount} STK")
        """
        page = 1
        while True:
            response = await self.get_transactions(
                from_user_id=from_user_id,
                to_user_id=to_user_id,
                from_discord_id=from_discord_id,
                to_discord_id=to_discord_id,
                includes_discord_id=includes_discord_id,
                page=page,
                limit=limit,
            )

            for transaction in response.transactions:
                yield transaction

            if not response.pagination or page >= response.pagination.total_pages:
                break

            page += 1

    async def get_users(
        self,
        username: Optional[str] = None,
        banned: Optional[bool] = None,
        admin: Optional[bool] = None,
        discord_id: Optional[int] = None,
        page: int = 1,
        limit: int = 20,
    ) -> UsersResponse:
        """
        Get users with pagination and filtering.

        Users are ordered by balance (highest first), then by username.

        Args:
            username: Filter by username (case-insensitive partial match)
            banned: Filter by banned status (True for banned users, False for active users)
            admin: Filter by admin status (True for admins, False for regular users)
            discord_id: Look up user by Discord ID to get internal user information
            page: Page number to retrieve (1-based)
            limit: Number of users per page (max 100)

        Returns:
            UsersResponse: Object containing list of users and pagination info

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails

        Example:
            # Get first page of users with "john" in their username
            users = await client.get_users(username="john", limit=10)
            for user in users.users:
                print(f"{user.username}: {user.balance} STK")

            # Look up user by Discord ID
            discord_user = await client.get_users(discord_id=123456789)
            if discord_user.users:
                user = discord_user.users[0]
                print(f"Discord user: {user.username} (ID: {user.id})")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if username:
            params["username"] = username
        if banned is not None:
            params["banned"] = str(banned).lower()
        if admin is not None:
            params["admin"] = str(admin).lower()
        if discord_id is not None:
            params["discord_id"] = discord_id

        response = await self._client.get(
            f"{self.base_url}/api/bot/users", params=params
        )
        response_data = self._handle_response(response)
        return UsersResponse.model_validate(response_data)

    async def stream_users(
        self,
        username: Optional[str] = None,
        banned: Optional[bool] = None,
        admin: Optional[bool] = None,
        discord_id: Optional[int] = None,
        limit: int = 20,
    ) -> AsyncGenerator[UserInfo, None]:
        """
        Stream all users, handling pagination automatically.

        This async generator yields individual UserInfo objects across all pages,
        ordered by balance (highest first), then by username.

        Args:
            username: Filter by username (case-insensitive partial match)
            banned: Filter by banned status (True for banned users, False for active users)
            admin: Filter by admin status (True for admins, False for regular users)
            discord_id: Look up user by Discord ID to get internal user information
            limit: Number of users to fetch per API call (affects performance, not results)

        Yields:
            UserInfo: Individual user objects with id, username, balance, admin, and banned status

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If any API request fails

        Example:
            # Find all active admin users
            async for user in client.stream_users(admin=True, banned=False):
                print(f"Admin: {user.username} ({user.balance} STK)")

            # Look up user by Discord ID
            async for user in client.stream_users(discord_id=123456789):
                print(f"Found Discord user: {user.username} (internal ID: {user.id})")
        """
        page = 1
        while True:
            response = await self.get_users(
                username=username,
                banned=banned,
                admin=admin,
                discord_id=discord_id,
                page=page,
                limit=limit,
            )

            for user in response.users:
                yield user

            if not response.pagination or page >= response.pagination.total_pages:
                break

            page += 1

    async def accept_request(self, request_id: int) -> RequestActionResponse:
        """
        Accept a pending payment request.

        This processes a payment request where the bot is the responder, transferring
        the requested amount from the bot's balance to the requester.

        Args:
            request_id: ID of the payment request to accept

        Returns:
            RequestActionResponse: Object containing the request ID, new status, resolution
                                 timestamp, and transaction ID if successful

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails (e.g., request not found,
                                 already processed, insufficient balance)

        Example:
            result = await client.accept_request(123)
            print(f"Accepted request #{result.request_id}, transaction: {result.transaction_id}")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(
            f"{self.base_url}/api/bot/requests/{request_id}/accept"
        )
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)

    async def deny_request(self, request_id: int) -> RequestActionResponse:
        """
        Deny a pending payment request.

        This rejects a payment request where the bot is the responder, changing
        the request status to "denied" without transferring any tokens.

        Args:
            request_id: ID of the payment request to deny

        Returns:
            RequestActionResponse: Object containing the request ID, new status ("denied"),
                                 and resolution timestamp

        Raises:
            RuntimeError: If client is not used within async context manager
            httpx.HTTPStatusError: If the API request fails (e.g., request not found,
                                 already processed)

        Example:
            result = await client.deny_request(123)
            print(f"Denied request #{result.request_id}, status: {result.status}")
        """
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(
            f"{self.base_url}/api/bot/requests/{request_id}/deny"
        )
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)
