import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request_requester import RequestRequester
    from ..models.request_responder import RequestResponder


T = TypeVar("T", bound="Request")


@_attrs_define
class Request:
    """A STK request

    Example:
        {'amount': 200, 'id': 789, 'label': 'Payment request', 'requested_at': '2019-09-12T12:34:55Z', 'requester':
            {'id': 123, 'username': 'johndoe'}, 'resolved_at': None, 'responder': {'id': 456, 'username': 'janedoe'},
            'status': 'pending', 'transaction_id': None}

    Attributes:
        amount (int): Requested amount
        id (int): Request ID
        requested_at (datetime.datetime): Request timestamp
        requester (RequestRequester):
        responder (RequestResponder):
        status (str): Request status
        label (Union[None, Unset, str]): Request label
        resolved_at (Union[None, Unset, datetime.datetime]): Resolution timestamp
        transaction_id (Union[None, Unset, int]): Associated transaction ID
    """

    amount: int
    id: int
    requested_at: datetime.datetime
    requester: "RequestRequester"
    responder: "RequestResponder"
    status: str
    label: Union[None, Unset, str] = UNSET
    resolved_at: Union[None, Unset, datetime.datetime] = UNSET
    transaction_id: Union[None, Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        id = self.id

        requested_at = self.requested_at.isoformat()

        requester = self.requester.to_dict()

        responder = self.responder.to_dict()

        status = self.status

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        resolved_at: Union[None, Unset, str]
        if isinstance(self.resolved_at, Unset):
            resolved_at = UNSET
        elif isinstance(self.resolved_at, datetime.datetime):
            resolved_at = self.resolved_at.isoformat()
        else:
            resolved_at = self.resolved_at

        transaction_id: Union[None, Unset, int]
        if isinstance(self.transaction_id, Unset):
            transaction_id = UNSET
        else:
            transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "id": id,
                "requested_at": requested_at,
                "requester": requester,
                "responder": responder,
                "status": status,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if resolved_at is not UNSET:
            field_dict["resolved_at"] = resolved_at
        if transaction_id is not UNSET:
            field_dict["transaction_id"] = transaction_id

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.request_requester import RequestRequester
        from ..models.request_responder import RequestResponder

        d = dict(src_dict)
        amount = d.pop("amount")

        id = d.pop("id")

        requested_at = isoparse(d.pop("requested_at"))

        requester = RequestRequester.from_dict(d.pop("requester"))

        responder = RequestResponder.from_dict(d.pop("responder"))

        status = d.pop("status")

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        def _parse_resolved_at(data: object) -> Union[None, Unset, datetime.datetime]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                resolved_at_type_0 = isoparse(data)

                return resolved_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, Unset, datetime.datetime], data)

        resolved_at = _parse_resolved_at(d.pop("resolved_at", UNSET))

        def _parse_transaction_id(data: object) -> Union[None, Unset, int]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, int], data)

        transaction_id = _parse_transaction_id(d.pop("transaction_id", UNSET))

        request = cls(
            amount=amount,
            id=id,
            requested_at=requested_at,
            requester=requester,
            responder=responder,
            status=status,
            label=label,
            resolved_at=resolved_at,
            transaction_id=transaction_id,
        )

        request.additional_properties = d
        return request

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
