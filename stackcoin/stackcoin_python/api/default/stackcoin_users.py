from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.users_response import UsersResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    username: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    banned: Union[Unset, bool] = UNSET,
    admin: Union[Unset, bool] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["username"] = username

    params["discord_id"] = discord_id

    params["banned"] = banned

    params["admin"] = admin

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/users",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[UsersResponse]:
    if response.status_code == 200:
        response_200 = UsersResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[UsersResponse]:
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
    username: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    banned: Union[Unset, bool] = UNSET,
    admin: Union[Unset, bool] = UNSET,
) -> Response[UsersResponse]:
    """Get users

     Retrieves users with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        username (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        banned (Union[Unset, bool]):
        admin (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsersResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        username=username,
        discord_id=discord_id,
        banned=banned,
        admin=admin,
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
    username: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    banned: Union[Unset, bool] = UNSET,
    admin: Union[Unset, bool] = UNSET,
) -> Optional[UsersResponse]:
    """Get users

     Retrieves users with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        username (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        banned (Union[Unset, bool]):
        admin (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsersResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        username=username,
        discord_id=discord_id,
        banned=banned,
        admin=admin,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    username: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    banned: Union[Unset, bool] = UNSET,
    admin: Union[Unset, bool] = UNSET,
) -> Response[UsersResponse]:
    """Get users

     Retrieves users with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        username (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        banned (Union[Unset, bool]):
        admin (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[UsersResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        username=username,
        discord_id=discord_id,
        banned=banned,
        admin=admin,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    username: Union[Unset, str] = UNSET,
    discord_id: Union[Unset, str] = UNSET,
    banned: Union[Unset, bool] = UNSET,
    admin: Union[Unset, bool] = UNSET,
) -> Optional[UsersResponse]:
    """Get users

     Retrieves users with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        username (Union[Unset, str]):
        discord_id (Union[Unset, str]):
        banned (Union[Unset, bool]):
        admin (Union[Unset, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        UsersResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            username=username,
            discord_id=discord_id,
            banned=banned,
            admin=admin,
        )
    ).parsed
