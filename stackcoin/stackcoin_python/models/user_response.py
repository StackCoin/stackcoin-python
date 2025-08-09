import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="UserResponse")


@_attrs_define
class UserResponse:
    """Response schema for single user

    Example:
        {'admin': False, 'balance': 1000, 'banned': False, 'id': 123, 'inserted_at': '2019-09-12T12:34:55Z',
            'updated_at': '2025-09-13T10:11:12Z', 'username': 'johndoe'}

    Attributes:
        admin (bool): Whether user is an admin
        balance (int): User's STK balance
        banned (bool): Whether user is banned
        username (str): Username
        id (Union[Unset, int]): User ID
        inserted_at (Union[Unset, datetime.datetime]): Creation timestamp
        updated_at (Union[Unset, datetime.datetime]): Update timestamp
    """

    admin: bool
    balance: int
    banned: bool
    username: str
    id: Union[Unset, int] = UNSET
    inserted_at: Union[Unset, datetime.datetime] = UNSET
    updated_at: Union[Unset, datetime.datetime] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        admin = self.admin

        balance = self.balance

        banned = self.banned

        username = self.username

        id = self.id

        inserted_at: Union[Unset, str] = UNSET
        if not isinstance(self.inserted_at, Unset):
            inserted_at = self.inserted_at.isoformat()

        updated_at: Union[Unset, str] = UNSET
        if not isinstance(self.updated_at, Unset):
            updated_at = self.updated_at.isoformat()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "admin": admin,
                "balance": balance,
                "banned": banned,
                "username": username,
            }
        )
        if id is not UNSET:
            field_dict["id"] = id
        if inserted_at is not UNSET:
            field_dict["inserted_at"] = inserted_at
        if updated_at is not UNSET:
            field_dict["updated_at"] = updated_at

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        admin = d.pop("admin")

        balance = d.pop("balance")

        banned = d.pop("banned")

        username = d.pop("username")

        id = d.pop("id", UNSET)

        _inserted_at = d.pop("inserted_at", UNSET)
        inserted_at: Union[Unset, datetime.datetime]
        if isinstance(_inserted_at, Unset):
            inserted_at = UNSET
        else:
            inserted_at = isoparse(_inserted_at)

        _updated_at = d.pop("updated_at", UNSET)
        updated_at: Union[Unset, datetime.datetime]
        if isinstance(_updated_at, Unset):
            updated_at = UNSET
        else:
            updated_at = isoparse(_updated_at)

        user_response = cls(
            admin=admin,
            balance=balance,
            banned=banned,
            username=username,
            id=id,
            inserted_at=inserted_at,
            updated_at=updated_at,
        )

        user_response.additional_properties = d
        return user_response

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
