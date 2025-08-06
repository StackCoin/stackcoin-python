from pydantic import BaseModel, Field
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


class PaginationInfo(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class RequestsResponse(BaseModel):
    requests: List[PaymentRequest]
    pagination: Optional[PaginationInfo] = None


class Transaction(BaseModel):
    id: int
    from_: User = Field(alias="from")
    to: User
    amount: int
    time: datetime
    label: Optional[str]


class TransactionsResponse(BaseModel):
    transactions: List[Transaction]
    pagination: Optional[PaginationInfo] = None


class UserInfo(BaseModel):
    id: int
    username: str
    balance: int
    admin: bool
    banned: bool


class UsersResponse(BaseModel):
    users: List[UserInfo]
    pagination: Optional[PaginationInfo] = None


class RequestActionResponse(BaseModel):
    success: bool
    request_id: int
    status: str
    resolved_at: datetime
    transaction_id: Optional[int] = None