from typing import Optional
import httpx
from .models import (
    BalanceResponse, 
    SendResponse, 
    RequestResponse, 
    RequestsResponse, 
    RequestActionResponse
)


class StackCoinClient:
    def __init__(self, token: str, base_url: str = "https://stackcoin.com", **kwargs):
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

        response = await self._client.get(f"{self.base_url}/api/bot/user/{user_id}/balance")
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

        response = await self._client.post(f"{self.base_url}/api/bot/user/{to_user_id}/send", json=data)
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

        response = await self._client.post(f"{self.base_url}/api/bot/user/{from_user_id}/request", json=data)
        response_data = self._handle_response(response)
        return RequestResponse.model_validate(response_data)

    async def get_requests(
        self, role: Optional[str] = None, status: Optional[str] = None
    ) -> RequestsResponse:
        """Get payment requests for the bot."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        params = {}
        if role:
            params["role"] = role
        if status:
            params["status"] = status

        response = await self._client.get(f"{self.base_url}/api/bot/requests", params=params)
        response_data = self._handle_response(response)
        return RequestsResponse.model_validate(response_data)

    async def accept_request(self, request_id: int) -> RequestActionResponse:
        """Accept a payment request."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(f"{self.base_url}/api/bot/requests/{request_id}/accept")
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)

    async def deny_request(self, request_id: int) -> RequestActionResponse:
        """Deny a payment request."""
        if not self._client:
            raise RuntimeError("Client must be used within async context manager")

        response = await self._client.post(f"{self.base_url}/api/bot/requests/{request_id}/deny")
        response_data = self._handle_response(response)
        return RequestActionResponse.model_validate(response_data)
