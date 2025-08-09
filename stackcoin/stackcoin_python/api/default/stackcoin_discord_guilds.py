from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.discord_guilds_response import DiscordGuildsResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    snowflake: Union[Unset, str] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["page"] = page

    params["limit"] = limit

    params["name"] = name

    params["snowflake"] = snowflake

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/discord/guilds",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[DiscordGuildsResponse]:
    if response.status_code == 200:
        response_200 = DiscordGuildsResponse.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DiscordGuildsResponse]:
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
    name: Union[Unset, str] = UNSET,
    snowflake: Union[Unset, str] = UNSET,
) -> Response[DiscordGuildsResponse]:
    """Get Discord guilds

     Retrieves Discord guilds with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        name (Union[Unset, str]):
        snowflake (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiscordGuildsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        name=name,
        snowflake=snowflake,
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
    name: Union[Unset, str] = UNSET,
    snowflake: Union[Unset, str] = UNSET,
) -> Optional[DiscordGuildsResponse]:
    """Get Discord guilds

     Retrieves Discord guilds with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        name (Union[Unset, str]):
        snowflake (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiscordGuildsResponse
    """

    return sync_detailed(
        client=client,
        page=page,
        limit=limit,
        name=name,
        snowflake=snowflake,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    snowflake: Union[Unset, str] = UNSET,
) -> Response[DiscordGuildsResponse]:
    """Get Discord guilds

     Retrieves Discord guilds with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        name (Union[Unset, str]):
        snowflake (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DiscordGuildsResponse]
    """

    kwargs = _get_kwargs(
        page=page,
        limit=limit,
        name=name,
        snowflake=snowflake,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    page: Union[Unset, int] = UNSET,
    limit: Union[Unset, int] = UNSET,
    name: Union[Unset, str] = UNSET,
    snowflake: Union[Unset, str] = UNSET,
) -> Optional[DiscordGuildsResponse]:
    """Get Discord guilds

     Retrieves Discord guilds with optional filtering and pagination.

    Args:
        page (Union[Unset, int]):
        limit (Union[Unset, int]):
        name (Union[Unset, str]):
        snowflake (Union[Unset, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DiscordGuildsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            page=page,
            limit=limit,
            name=name,
            snowflake=snowflake,
        )
    ).parsed
