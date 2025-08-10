from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.requests_response import RequestsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    role: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["role"] = role

    params["status"] = status

    params["discord_id"] = discord_id

    params["since"] = since

    params["page"] = page

    params["limit"] = limit

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/requests",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, RequestsResponse]]:
    if response.status_code == 200:
        response_200 = RequestsResponse.from_dict(response.json())

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
) -> Response[Union[ErrorResponse, RequestsResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    role: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorResponse, RequestsResponse]]:
    """Get requests for the authenticated user

     Retrieves requests involving the authenticated user, with optional filtering and pagination.

    Args:
        role (Union[Unset, str]):
        status (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        since (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RequestsResponse]]
    """

    kwargs = _get_kwargs(
        role=role,
        status=status,
        discord_id=discord_id,
        since=since,
        page=page,
        limit=limit,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    role: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorResponse, RequestsResponse]]:
    """Get requests for the authenticated user

     Retrieves requests involving the authenticated user, with optional filtering and pagination.

    Args:
        role (Union[Unset, str]):
        status (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        since (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RequestsResponse]
    """

    return sync_detailed(
        client=client,
        role=role,
        status=status,
        discord_id=discord_id,
        since=since,
        page=page,
        limit=limit,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    role: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Response[Union[ErrorResponse, RequestsResponse]]:
    """Get requests for the authenticated user

     Retrieves requests involving the authenticated user, with optional filtering and pagination.

    Args:
        role (Union[Unset, str]):
        status (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        since (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, RequestsResponse]]
    """

    kwargs = _get_kwargs(
        role=role,
        status=status,
        discord_id=discord_id,
        since=since,
        page=page,
        limit=limit,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    role: Union[Unset, str] = UNSET,
    status: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    since: Union[Unset, str] = UNSET,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
) -> Optional[Union[ErrorResponse, RequestsResponse]]:
    """Get requests for the authenticated user

     Retrieves requests involving the authenticated user, with optional filtering and pagination.

    Args:
        role (Union[Unset, str]):
        status (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        since (Union[Unset, str]):
        page (Union[Unset, int]):
        limit (Union[Unset, int]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, RequestsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            role=role,
            status=status,
            discord_id=discord_id,
            since=since,
            page=page,
            limit=limit,
        )
    ).parsed
