from datetime import datetime
from uuid import UUID
from typing import Dict

from pydantic import BaseModel


class TransferSuccess(BaseModel):
    timestamp: datetime
    uuid: UUID
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
