from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class BalanceResponse(BaseModel):
    balance: int
    username: str


class ErrorResponse(BaseModel):
    error: str


class SendResponse(BaseModel):
    success: bool
    transaction_id: int
    amount: int
    from_new_balance: int
    to_new_balance: int


class User(BaseModel):
    id: int
    username: str


class RequestResponse(BaseModel):
    success: bool
    request_id: int
    amount: int
    status: str
    requested_at: datetime
    requester: User
    responder: User


class PaymentRequest(BaseModel):
    id: int
    amount: int
    status: str
    requested_at: datetime
    resolved_at: Optional[datetime]
    label: Optional[str]
    requester: User
    responder: User
    transaction_id: Optional[int]


class RequestsResponse(BaseModel):
    requests: List[PaymentRequest]


class RequestActionResponse(BaseModel):
    success: bool
    request_id: int
    status: str
    resolved_at: datetime
    transaction_id: Optional[int] = None