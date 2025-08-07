import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.create_request_response_requester import CreateRequestResponseRequester
    from ..models.create_request_response_responder import CreateRequestResponseResponder


T = TypeVar("T", bound="CreateRequestResponse")


@_attrs_define
class CreateRequestResponse:
    """Response schema for creating a request

    Example:
        {'amount': 200, 'request_id': 789, 'requested_at': '2019-09-12T12:34:55Z', 'requester': {'id': 123, 'username':
            'johndoe'}, 'responder': {'id': 456, 'username': 'janedoe'}, 'status': 'pending', 'success': True}

    Attributes:
        amount (int): Requested amount
        request_id (int): Created request ID
        requested_at (datetime.datetime): Request timestamp
        requester (CreateRequestResponseRequester):
        responder (CreateRequestResponseResponder):
        status (str): Request status
        success (bool): Whether the operation succeeded
    """

    amount: int
    request_id: int
    requested_at: datetime.datetime
    requester: "CreateRequestResponseRequester"
    responder: "CreateRequestResponseResponder"
    status: str
    success: bool
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        request_id = self.request_id

        requested_at = self.requested_at.isoformat()

        requester = self.requester.to_dict()

        responder = self.responder.to_dict()

        status = self.status

        success = self.success

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "request_id": request_id,
                "requested_at": requested_at,
                "requester": requester,
                "responder": responder,
                "status": status,
                "success": success,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.create_request_response_requester import CreateRequestResponseRequester
        from ..models.create_request_response_responder import CreateRequestResponseResponder

        d = dict(src_dict)
        amount = d.pop("amount")

        request_id = d.pop("request_id")

        requested_at = isoparse(d.pop("requested_at"))

        requester = CreateRequestResponseRequester.from_dict(d.pop("requester"))

        responder = CreateRequestResponseResponder.from_dict(d.pop("responder"))

        status = d.pop("status")

        success = d.pop("success")

        create_request_response = cls(
            amount=amount,
            request_id=request_id,
            requested_at=requested_at,
            requester=requester,
            responder=responder,
            status=status,
            success=success,
        )

        create_request_response.additional_properties = d
        return create_request_response

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
