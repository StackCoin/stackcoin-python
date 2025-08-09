import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DiscordGuildResponse")


@_attrs_define
class DiscordGuildResponse:
    """Response schema for single Discord guild

    Example:
        {'designated_channel_snowflake': '987654321098765432', 'id': 123, 'last_updated': '2019-09-12T12:34:55Z',
            'name': 'My Discord Server', 'snowflake': '123456789012345678'}

    Attributes:
        id (int): Guild ID
        last_updated (datetime.datetime): Last updated timestamp
        name (str): Guild name
        snowflake (str): Discord guild snowflake ID
        designated_channel_snowflake (Union[None, Unset, str]): Designated channel snowflake ID
    """

    id: int
    last_updated: datetime.datetime
    name: str
    snowflake: str
    designated_channel_snowflake: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = self.id

        last_updated = self.last_updated.isoformat()

        name = self.name

        snowflake = self.snowflake

        designated_channel_snowflake: Union[None, Unset, str]
        if isinstance(self.designated_channel_snowflake, Unset):
            designated_channel_snowflake = UNSET
        else:
            designated_channel_snowflake = self.designated_channel_snowflake

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "last_updated": last_updated,
                "name": name,
                "snowflake": snowflake,
            }
        )
        if designated_channel_snowflake is not UNSET:
            field_dict["designated_channel_snowflake"] = designated_channel_snowflake

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = d.pop("id")

        last_updated = isoparse(d.pop("last_updated"))

        name = d.pop("name")

        snowflake = d.pop("snowflake")

        def _parse_designated_channel_snowflake(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        designated_channel_snowflake = _parse_designated_channel_snowflake(d.pop("designated_channel_snowflake", UNSET))

        discord_guild_response = cls(
            id=id,
            last_updated=last_updated,
            name=name,
            snowflake=snowflake,
            designated_channel_snowflake=designated_channel_snowflake,
        )

        discord_guild_response.additional_properties = d
        return discord_guild_response

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
