from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.transaction_response import TransactionResponse
from ...types import Response


def _get_kwargs(
    transaction_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/transaction/{transaction_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, TransactionResponse]]:
    if response.status_code == 200:
        response_200 = TransactionResponse.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, TransactionResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    transaction_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ErrorResponse, TransactionResponse]]:
    """Get transaction by ID

     Retrieves a single transaction by its ID.

    Args:
        transaction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    transaction_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ErrorResponse, TransactionResponse]]:
    """Get transaction by ID

     Retrieves a single transaction by its ID.

    Args:
        transaction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionResponse]
    """

    return sync_detailed(
        transaction_id=transaction_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    transaction_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ErrorResponse, TransactionResponse]]:
    """Get transaction by ID

     Retrieves a single transaction by its ID.

    Args:
        transaction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, TransactionResponse]]
    """

    kwargs = _get_kwargs(
        transaction_id=transaction_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    transaction_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ErrorResponse, TransactionResponse]]:
    """Get transaction by ID

     Retrieves a single transaction by its ID.

    Args:
        transaction_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, TransactionResponse]
    """

    return (
        await asyncio_detailed(
            transaction_id=transaction_id,
            client=client,
        )
    ).parsed
