import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="RequestActionResponse")


@_attrs_define
class RequestActionResponse:
    """Response schema for request actions (accept/deny)

    Example:
        {'request_id': 789, 'resolved_at': '2025-09-12T13:34:55Z', 'status': 'accepted', 'success': True,
            'transaction_id': 456}

    Attributes:
        request_id (int): Request ID
        resolved_at (datetime.datetime): Resolution timestamp
        status (str): New request status
        success (bool): Whether the operation succeeded
        transaction_id (Union[None, Unset, int]): Associated transaction ID
    """

    request_id: int
    resolved_at: datetime.datetime
    status: str
    success: bool
    transaction_id: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        request_id = self.request_id

        resolved_at = self.resolved_at.isoformat()

        status = self.status

        success = self.success

        transaction_id: Union[None, Unset, int]
        if isinstance(self.transaction_id, Unset):
            transaction_id = UNSET
        else:
            transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "request_id": request_id,
                "resolved_at": resolved_at,
                "status": status,
                "success": success,
            }
        )
        if transaction_id is not UNSET:
            field_dict["transaction_id"] = transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        request_id = d.pop("request_id")

        resolved_at = isoparse(d.pop("resolved_at"))

        status = d.pop("status")

        success = d.pop("success")

        def _parse_transaction_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id", UNSET))

        request_action_response = cls(
            request_id=request_id,
            resolved_at=resolved_at,
            status=status,
            success=success,
            transaction_id=transaction_id,
        )

        request_action_response.additional_properties = d
        return request_action_response

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
