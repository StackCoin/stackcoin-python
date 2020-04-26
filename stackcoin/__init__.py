import json
from json.decoder import JSONDecodeError
from typing import Dict, Optional

import requests
from requests.exceptions import RequestException
import aiohttp
import asyncio

from .exceptions import *
from .types import TransferSuccess, User, Users

WS_EVENTS = {"TransferSuccess": TransferSuccess}

DOMAIN = "stackcoin.world"
DEFAULT_HTTP_BASE_URL = f"https://{DOMAIN}"
DEFAULT_WS_BASE_URL = f"wss://{DOMAIN}/ws"


class StackCoin:
    def __init__(
        self,
        *,
        base_http_url=DEFAULT_HTTP_BASE_URL,
        base_ws_url=DEFAULT_WS_BASE_URL,
        token,
        user_id,
    ):
        self.base_http_url = base_http_url
        self.base_ws_url = base_ws_url
        self.token = token
        self.user_id = user_id
        self._access_token = None

        self._notification_decorator = None

        self._access_token = self._authenticate()
        print(f"Authenticated with the StackCoin HTTP API as {self.user_id}")

    def notification(self):
        def decorator(func):
            if self._notification_decorator is not None:
                raise StackCoinException(
                    "Already assigned a notification decorator, there can only be one!"
                )

            self._notification_decorator = func

        return decorator

    def ensure_decorator(self):
        if self._notification_decorator is None:
            raise StackCoinException(
                "Can't run without assigning the notification decorator first!"
            )

    def run(self):
        self.ensure_decorator()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._notification(loop))

    async def start(self):
        self.ensure_decorator()
        await self._notification()

    async def _handle_ws_handle(self, ws):
        state = None

        async for msg in ws:
            try:
                data = json.loads(msg.data.replace("\n", ""))
            except JSONDecodeError as e:
                raise UnknownWSState(
                    f"Failed to parse message from ws server as json: {msg.data}"
                )

            if msg.type == aiohttp.WSMsgType.TEXT:
                if "state" in data:
                    state = data["state"]

                if state == "Hello":
                    await ws.send_json({"token": self.token})

                elif state == "Ready":

                    if "success" in data:
                        success = data["success"]

                        if success in WS_EVENTS:
                            self._notification_decorator(TransferSuccess(**data))
                        else:
                            raise UnknownWSState(
                                "Got success '{data}' that wasn't a known ws event"
                            )

                        if "uuid" not in data:
                            raise UnknownWSState("Got success '{data}' without UUID")

                        await ws.send_json({"acknowledge": data["uuid"]})

                    elif "error" in data:
                        # TODO currently no error results are sent, maybe they never will be via this route?
                        pass

                    elif "state" in data:
                        pass

                    else:
                        raise UnknownWSState(
                            "Got data '{data}' while in state '{state}'"
                        )

                elif state == "AwaitingAcknowledgement":
                    # TODO do we store the last sent uuid instead of sending on getting?
                    pass

                elif state == "Closed":
                    raise ClosedWS()

                else:
                    raise UnknownWSState(state)

            elif msg.type == aiohttp.WSMsgType.ERROR:
                # TODO maybe raise expetion, print to stderr, logging instead?
                print(data)
                break

    async def _notification(self):
        loop = asyncio.get_event_loop()

        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.ws_connect(
                f"{self.base_ws_url}/notification/{self.user_id}"
            ) as ws:
                print(
                    f"Connected to the StackCoin WS Notification endpoint as {self.user_id}"
                )
                try:
                    await self._handle_ws_handle(ws)
                finally:
                    await session.close()

    def _request(self, http_verb, path_postfix, *, json=None, should_retry=True):
        headers = {}
        if self._access_token is not None:
            headers["X-Access-Token"] = self._access_token

        while True:
            resp = requests.request(
                http_verb,
                f"{self.base_http_url}/{path_postfix}",
                headers=headers,
                json=json,
            )

            if resp.status_code == 401:
                if not should_retry:
                    raise UnexpectedState(resp.text)

                self._access_token = self._authenticate()
                headers["X-Access-Token"] = self._access_token

                should_retry = False
            else:
                break

        try:
            resp_json = resp.json()
            if "error" in resp_json:
                if "message" in resp_json:
                    message = resp_json["message"]

                external_exception = type(resp_json["error"], (StackCoinException,), {})
                raise external_exception(message)
        except ValueError as e:
            raise UnexpectedState(e)

        try:
            resp.raise_for_status()
        except RequestException as e:
            raise RequestError(f"{e}: {resp.text}")

        return resp_json

    def _authenticate(self):
        try:
            resp_json = self._request(
                "POST",
                "auth",
                json={"token": self.token, "user_id": self.user_id},
                should_retry=False,
            )
        except RequestError as e:
            raise AuthenticationFailure(e)
        except UnexpectedState as e:
            raise AuthenticationFailure(e)

        if "access_token" in resp_json:
            return resp_json["access_token"]
        else:
            raise UnexpectedState(resp_json)

    def users(self) -> Dict[str, User]:
        try:
            return Users(__root__=self._request("GET", "user/")).__root__
        except RequestError:
            raise UnexpectedState(e)

    def user(self, user_id=None) -> Optional[User]:
        if user_id is None:
            user_id = self.user_id

        try:
            return User(**self._request("GET", f"user/{user_id}"))
        except RequestError:
            return None

    def transfer(self, to_id, amount) -> TransferSuccess:
        try:
            return TransferSuccess(
                **self._request(
                    "POST", "ledger/", json={"to_id": to_id, "amount": amount}
                )
            )
        except RequestError as e:
            raise TransferFailure(e)
