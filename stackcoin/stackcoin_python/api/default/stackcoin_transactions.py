from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.transactions_response import TransactionsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_user_id: Union[Unset, int] = UNSET,
    to_user_id: Union[Unset, int] = UNSET,
    from_discord_id: Union[Unset, str] = UNSET,
    to_discord_id: Union[Unset, str] = UNSET,
    includes_discord_id: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["from_user_id"] = from_user_id

    params["to_user_id"] = to_user_id

    params["from_discord_id"] = from_discord_id

    params["to_discord_id"] = to_discord_id

    params["includes_discord_id"] = includes_discord_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/transactions",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TransactionsResponse]]:
    if response.status_code == 200:
        response_200 = TransactionsResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, TransactionsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_user_id: Union[Unset, int] = UNSET,
    to_user_id: Union[Unset, int] = UNSET,
    from_discord_id: Union[Unset, str] = UNSET,
    to_discord_id: Union[Unset, str] = UNSET,
    includes_discord_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TransactionsResponse]]:
    """Get transactions for the authenticated user

     Retrieves transactions involving the authenticated user, with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_user_id (Union[Unset, int]):
        to_user_id (Union[Unset, int]):
        from_discord_id (Union[Unset, str]):
        to_discord_id (Union[Unset, str]):
        includes_discord_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        from_discord_id=from_discord_id,
        to_discord_id=to_discord_id,
        includes_discord_id=includes_discord_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_user_id: Union[Unset, int] = UNSET,
    to_user_id: Union[Unset, int] = UNSET,
    from_discord_id: Union[Unset, str] = UNSET,
    to_discord_id: Union[Unset, str] = UNSET,
    includes_discord_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TransactionsResponse]]:
    """Get transactions for the authenticated user

     Retrieves transactions involving the authenticated user, with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_user_id (Union[Unset, int]):
        to_user_id (Union[Unset, int]):
        from_discord_id (Union[Unset, str]):
        to_discord_id (Union[Unset, str]):
        includes_discord_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsResponse]
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        from_discord_id=from_discord_id,
        to_discord_id=to_discord_id,
        includes_discord_id=includes_discord_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_user_id: Union[Unset, int] = UNSET,
    to_user_id: Union[Unset, int] = UNSET,
    from_discord_id: Union[Unset, str] = UNSET,
    to_discord_id: Union[Unset, str] = UNSET,
    includes_discord_id: Union[Unset, str] = UNSET,
) -> Response[Union[ErrorResponse, TransactionsResponse]]:
    """Get transactions for the authenticated user

     Retrieves transactions involving the authenticated user, with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_user_id (Union[Unset, int]):
        to_user_id (Union[Unset, int]):
        from_discord_id (Union[Unset, str]):
        to_discord_id (Union[Unset, str]):
        includes_discord_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionsResponse]]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        from_user_id=from_user_id,
        to_user_id=to_user_id,
        from_discord_id=from_discord_id,
        to_discord_id=to_discord_id,
        includes_discord_id=includes_discord_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    from_user_id: Union[Unset, int] = UNSET,
    to_user_id: Union[Unset, int] = UNSET,
    from_discord_id: Union[Unset, str] = UNSET,
    to_discord_id: Union[Unset, str] = UNSET,
    includes_discord_id: Union[Unset, str] = UNSET,
) -> Optional[Union[ErrorResponse, TransactionsResponse]]:
    """Get transactions for the authenticated user

     Retrieves transactions involving the authenticated user, with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        from_user_id (Union[Unset, int]):
        to_user_id (Union[Unset, int]):
        from_discord_id (Union[Unset, str]):
        to_discord_id (Union[Unset, str]):
        includes_discord_id (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            from_discord_id=from_discord_id,
            to_discord_id=to_discord_id,
            includes_discord_id=includes_discord_id,
        )
    ).parsed
