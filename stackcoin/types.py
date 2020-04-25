from typing import Dict

from pydantic import BaseModel


class TransferSuccess(BaseModel):
    timestamp: str  # TODO native python datetime object? - 2020-04-25T21:49:04Z
    uuid: str  # TODO native python uuid? - b83666fb-8531-4695-93ab-77c19440b05a
    message: str
    from_id: int
    from_bal: int
    to_id: int
    to_bal: int
    amount: int


class User(BaseModel):
    id: str
    bal: int


class Users(BaseModel):
    __root__: Dict[str, User]
