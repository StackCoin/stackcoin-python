from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.request_response import RequestResponse
from ...types import Response


def _get_kwargs(
    request_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/request/{request_id}",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, RequestResponse]]:
    if response.status_code == 200:
        response_200 = RequestResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, RequestResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    request_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ErrorResponse, RequestResponse]]:
    """Get request by ID

     Retrieves a single request by its ID.

    Args:
        request_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RequestResponse]]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    request_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ErrorResponse, RequestResponse]]:
    """Get request by ID

     Retrieves a single request by its ID.

    Args:
        request_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RequestResponse]
    """

    return sync_detailed(
        request_id=request_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    request_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[Union[ErrorResponse, RequestResponse]]:
    """Get request by ID

     Retrieves a single request by its ID.

    Args:
        request_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RequestResponse]]
    """

    kwargs = _get_kwargs(
        request_id=request_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    request_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[Union[ErrorResponse, RequestResponse]]:
    """Get request by ID

     Retrieves a single request by its ID.

    Args:
        request_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RequestResponse]
    """

    return (
        await asyncio_detailed(
            request_id=request_id,
            client=client,
        )
    ).parsed
