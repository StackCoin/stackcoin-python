from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.request import Request
    from ..models.requests_response_pagination import RequestsResponsePagination


T = TypeVar("T", bound="RequestsResponse")


@_attrs_define
class RequestsResponse:
    """Response schema for multiple requests

    Example:
        {'pagination': {'limit': 20, 'page': 1, 'total': 1, 'total_pages': 1}, 'requests': [{'amount': 200, 'id': 789,
            'label': 'Payment request', 'requested_at': '2019-09-12T12:34:55Z', 'requester': {'id': 123, 'username':
            'johndoe'}, 'resolved_at': None, 'responder': {'id': 456, 'username': 'janedoe'}, 'status': 'pending',
            'transaction_id': None}]}

    Attributes:
        pagination (Union[Unset, RequestsResponsePagination]):
        requests (Union[Unset, list['Request']]): The requests list
    """

    pagination: Union[Unset, "RequestsResponsePagination"] = UNSET
    requests: Union[Unset, list["Request"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pagination: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        requests: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.requests, Unset):
            requests = []
            for requests_item_data in self.requests:
                requests_item = requests_item_data.to_dict()
                requests.append(requests_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pagination is not UNSET:
            field_dict["pagination"] = pagination
        if requests is not UNSET:
            field_dict["requests"] = requests

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.request import Request
        from ..models.requests_response_pagination import RequestsResponsePagination

        d = dict(src_dict)
        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, RequestsResponsePagination]
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = RequestsResponsePagination.from_dict(_pagination)

        requests = []
        _requests = d.pop("requests", UNSET)
        for requests_item_data in _requests or []:
            requests_item = Request.from_dict(requests_item_data)

            requests.append(requests_item)

        requests_response = cls(
            pagination=pagination,
            requests=requests,
        )

        requests_response.additional_properties = d
        return requests_response

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
