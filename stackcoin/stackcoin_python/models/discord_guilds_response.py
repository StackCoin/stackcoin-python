from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.discord_guild import DiscordGuild
    from ..models.discord_guilds_response_pagination import DiscordGuildsResponsePagination


T = TypeVar("T", bound="DiscordGuildsResponse")


@_attrs_define
class DiscordGuildsResponse:
    """Response schema for multiple Discord guilds

    Example:
        {'guilds': [{'designated_channel_snowflake': '987654321098765432', 'id': 123, 'last_updated':
            '2019-09-12T12:34:55Z', 'name': 'My Discord Server', 'snowflake': '123456789012345678'},
            {'designated_channel_snowflake': None, 'id': 456, 'last_updated': '2019-09-13T10:11:12Z', 'name': 'Another
            Server', 'snowflake': '876543210987654321'}], 'pagination': {'limit': 20, 'page': 1, 'total': 2, 'total_pages':
            1}}

    Attributes:
        guilds (Union[Unset, list['DiscordGuild']]): The guilds list
        pagination (Union[Unset, DiscordGuildsResponsePagination]):
    """

    guilds: Union[Unset, list["DiscordGuild"]] = UNSET
    pagination: Union[Unset, "DiscordGuildsResponsePagination"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        guilds: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.guilds, Unset):
            guilds = []
            for guilds_item_data in self.guilds:
                guilds_item = guilds_item_data.to_dict()
                guilds.append(guilds_item)

        pagination: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if guilds is not UNSET:
            field_dict["guilds"] = guilds
        if pagination is not UNSET:
            field_dict["pagination"] = pagination

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.discord_guild import DiscordGuild
        from ..models.discord_guilds_response_pagination import DiscordGuildsResponsePagination

        d = dict(src_dict)
        guilds = []
        _guilds = d.pop("guilds", UNSET)
        for guilds_item_data in _guilds or []:
            guilds_item = DiscordGuild.from_dict(guilds_item_data)

            guilds.append(guilds_item)

        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, DiscordGuildsResponsePagination]
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = DiscordGuildsResponsePagination.from_dict(_pagination)

        discord_guilds_response = cls(
            guilds=guilds,
            pagination=pagination,
        )

        discord_guilds_response.additional_properties = d
        return discord_guilds_response

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
