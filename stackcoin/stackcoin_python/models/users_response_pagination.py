from collections.abc import Mapping
from typing import Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

T = TypeVar("T", bound="UsersResponsePagination")


@_attrs_define
class UsersResponsePagination:
    """
    Attributes:
        limit (Union[Unset, int]): Items per page
        page (Union[Unset, int]): Current page
        total (Union[Unset, int]): Total items
        total_pages (Union[Unset, int]): Total pages
    """

    limit: Union[Unset, int] = UNSET
    page: Union[Unset, int] = UNSET
    total: Union[Unset, int] = UNSET
    total_pages: Union[Unset, int] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        limit = self.limit

        page = self.page

        total = self.total

        total_pages = self.total_pages

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if limit is not UNSET:
            field_dict["limit"] = limit
        if page is not UNSET:
            field_dict["page"] = page
        if total is not UNSET:
            field_dict["total"] = total
        if total_pages is not UNSET:
            field_dict["total_pages"] = total_pages

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        limit = d.pop("limit", UNSET)

        page = d.pop("page", UNSET)

        total = d.pop("total", UNSET)

        total_pages = d.pop("total_pages", UNSET)

        users_response_pagination = cls(
            limit=limit,
            page=page,
            total=total,
            total_pages=total_pages,
        )

        users_response_pagination.additional_properties = d
        return users_response_pagination

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
