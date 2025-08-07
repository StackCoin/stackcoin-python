from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response import ErrorResponse
from ...models.send_stk_params import SendStkParams
from ...models.send_stk_response import SendStkResponse
from ...types import Response


def _get_kwargs(
    user_id: int,
    *,
    body: SendStkParams,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/users/{user_id}/send",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[ErrorResponse, SendStkResponse]]:
    if response.status_code == 200:
        response_200 = SendStkResponse.from_dict(response.json())

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
    if response.status_code == 422:
        response_422 = ErrorResponse.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[ErrorResponse, SendStkResponse]]:
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
    body: SendStkParams,
) -> Response[Union[ErrorResponse, SendStkResponse]]:
    """Send STK to a user

     Transfers STK from the authenticated user to a specified user.

    Args:
        user_id (int):
        body (SendStkParams): Parameters for sending STK Example: {'amount': 100, 'label':
            'Payment for services'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SendStkResponse]]
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
    body: SendStkParams,
) -> Optional[Union[ErrorResponse, SendStkResponse]]:
    """Send STK to a user

     Transfers STK from the authenticated user to a specified user.

    Args:
        user_id (int):
        body (SendStkParams): Parameters for sending STK Example: {'amount': 100, 'label':
            'Payment for services'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SendStkResponse]
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
    body: SendStkParams,
) -> Response[Union[ErrorResponse, SendStkResponse]]:
    """Send STK to a user

     Transfers STK from the authenticated user to a specified user.

    Args:
        user_id (int):
        body (SendStkParams): Parameters for sending STK Example: {'amount': 100, 'label':
            'Payment for services'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse, SendStkResponse]]
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
    body: SendStkParams,
) -> Optional[Union[ErrorResponse, SendStkResponse]]:
    """Send STK to a user

     Transfers STK from the authenticated user to a specified user.

    Args:
        user_id (int):
        body (SendStkParams): Parameters for sending STK Example: {'amount': 100, 'label':
            'Payment for services'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse, SendStkResponse]
    """

    return (
        await asyncio_detailed(
            user_id=user_id,
            client=client,
            body=body,
        )
    ).parsed
