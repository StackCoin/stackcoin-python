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
        """Get bot's current balance and username."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.get(f"{self.base_url}/api/bot/self/balance")
        response_data = self._handle_response(response)
        return BalanceResponse.model_validate(response_data)

    async def get_balance(self, user_id: int) -> BalanceResponse:
        """Get another user's balance by their user ID."""
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
        """Send tokens from bot's balance to another user."""
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
        """Create a payment request from another user."""
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
        self, role: Optional[str] = None, status: Optional[str] = None, page: int = 1, limit: int = 20
    ) -> RequestsResponse:
        """Get payment requests for the bot with pagination."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if role:
            params["role"] = role
        if status:
            params["status"] = status

        response = await self._client.get(
            f"{self.base_url}/api/bot/requests", params=params
        )
        response_data = self._handle_response(response)
        return RequestsResponse.model_validate(response_data)

    async def stream_requests(
        self, role: Optional[str] = None, status: Optional[str] = None, limit: int = 20
    ) -> AsyncGenerator[PaymentRequest, None]:
        """Stream all payment requests for the bot, handling pagination automatically."""
        page = 1
        while True:
            response = await self.get_requests(role=role, status=status, page=page, limit=limit)
            
            for request in response.requests:
                yield request
            
            if not response.pagination or page >= response.pagination.total_pages:
                break
                
            page += 1

    async def get_transactions(
        self, from_user_id: Optional[int] = None, to_user_id: Optional[int] = None, page: int = 1, limit: int = 20
    ) -> TransactionsResponse:
        """Get transactions for the bot with pagination."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if from_user_id:
            params["from_user_id"] = from_user_id
        if to_user_id:
            params["to_user_id"] = to_user_id

        response = await self._client.get(
            f"{self.base_url}/api/bot/transactions", params=params
        )
        response_data = self._handle_response(response)
        return TransactionsResponse.model_validate(response_data)

    async def stream_transactions(
        self, from_user_id: Optional[int] = None, to_user_id: Optional[int] = None, limit: int = 20
    ) -> AsyncGenerator[Transaction, None]:
        """Stream all transactions for the bot, handling pagination automatically."""
        page = 1
        while True:
            response = await self.get_transactions(from_user_id=from_user_id, to_user_id=to_user_id, page=page, limit=limit)
            
            for transaction in response.transactions:
                yield transaction
            
            if not response.pagination or page >= response.pagination.total_pages:
                break
                
            page += 1

    async def get_users(
        self, username: Optional[str] = None, banned: Optional[bool] = None, admin: Optional[bool] = None, page: int = 1, limit: int = 20
    ) -> UsersResponse:
        """Get users with pagination and filtering."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {"page": page, "limit": limit}
        if username:
            params["username"] = username
        if banned is not None:
            params["banned"] = str(banned).lower()
        if admin is not None:
            params["admin"] = str(admin).lower()

        response = await self._client.get(
            f"{self.base_url}/api/bot/users", params=params
        )
        response_data = self._handle_response(response)
        return UsersResponse.model_validate(response_data)

    async def stream_users(
        self, username: Optional[str] = None, banned: Optional[bool] = None, admin: Optional[bool] = None, limit: int = 20
    ) -> AsyncGenerator[UserInfo, None]:
        """Stream all users, handling pagination automatically."""
        page = 1
        while True:
            response = await self.get_users(username=username, banned=banned, admin=admin, page=page, limit=limit)
            
            for user in response.users:
                yield user
            
            if not response.pagination or page >= response.pagination.total_pages:
                break
                
            page += 1

    async def accept_request(self, request_id: int) -> RequestActionResponse:
        """Accept a payment request."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(
            f"{self.base_url}/api/bot/requests/{request_id}/accept"
        )
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)

    async def deny_request(self, request_id: int) -> RequestActionResponse:
        """Deny a payment request."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(
            f"{self.base_url}/api/bot/requests/{request_id}/deny"
        )
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)
