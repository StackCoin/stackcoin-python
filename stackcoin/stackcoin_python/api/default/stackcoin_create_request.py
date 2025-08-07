from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.create_request_params import CreateRequestParams
from ...models.create_request_response import CreateRequestResponse
from ...models.error_response import ErrorResponse
from ...types import Response


def _get_kwargs(
    user_id: int,
    *,
    body: CreateRequestParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/users/{user_id}/request",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[CreateRequestResponse, ErrorResponse]]:
    if response.status_code == 200:
        response_200 = CreateRequestResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400
    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403
    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[CreateRequestResponse, ErrorResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    user_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRequestParams,
) -> Response[Union[CreateRequestResponse, ErrorResponse]]:
    """Create a STK request

     Creates a request for STK from a specified user.

    Args:
        user_id (int):
        body (CreateRequestParams): Parameters for creating a STK request Example: {'amount': 200,
            'label': 'Payment request'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateRequestResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    user_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRequestParams,
) -> Optional[Union[CreateRequestResponse, ErrorResponse]]:
    """Create a STK request

     Creates a request for STK from a specified user.

    Args:
        user_id (int):
        body (CreateRequestParams): Parameters for creating a STK request Example: {'amount': 200,
            'label': 'Payment request'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateRequestResponse, ErrorResponse]
    """

    return sync_detailed(
        user_id=user_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    user_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRequestParams,
) -> Response[Union[CreateRequestResponse, ErrorResponse]]:
    """Create a STK request

     Creates a request for STK from a specified user.

    Args:
        user_id (int):
        body (CreateRequestParams): Parameters for creating a STK request Example: {'amount': 200,
            'label': 'Payment request'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[CreateRequestResponse, ErrorResponse]]
    """

    kwargs = _get_kwargs(
        user_id=user_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    user_id: int,
    *,
    client: Union[AuthenticatedClient, Client],
    body: CreateRequestParams,
) -> Optional[Union[CreateRequestResponse, ErrorResponse]]:
    """Create a STK request

     Creates a request for STK from a specified user.

    Args:
        user_id (int):
        body (CreateRequestParams): Parameters for creating a STK request Example: {'amount': 200,
            'label': 'Payment request'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[CreateRequestResponse, ErrorResponse]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
