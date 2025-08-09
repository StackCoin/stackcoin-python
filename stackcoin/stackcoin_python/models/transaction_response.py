import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transaction_response_from import TransactionResponseFrom
    from ..models.transaction_response_to import TransactionResponseTo


T = TypeVar("T", bound="TransactionResponse")


@_attrs_define
class TransactionResponse:
    """Response schema for single transaction

    Example:
        {'amount': 100, 'from': {'id': 123, 'username': 'johndoe'}, 'id': 456, 'label': 'Payment for services', 'time':
            '2019-09-12T12:34:55Z', 'to': {'id': 789, 'username': 'janedoe'}}

    Attributes:
        amount (int): Transaction amount
        from_ (TransactionResponseFrom):
        id (int): Transaction ID
        time (datetime.datetime): Transaction timestamp
        to (TransactionResponseTo):
        label (Union[None, Unset, str]): Transaction label
    """

    amount: int
    from_: "TransactionResponseFrom"
    id: int
    time: datetime.datetime
    to: "TransactionResponseTo"
    label: Union[None, Unset, str] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        from_ = self.from_.to_dict()

        id = self.id

        time = self.time.isoformat()

        to = self.to.to_dict()

        label: Union[None, Unset, str]
        if isinstance(self.label, Unset):
            label = UNSET
        else:
            label = self.label

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "from": from_,
                "id": id,
                "time": time,
                "to": to,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction_response_from import TransactionResponseFrom
        from ..models.transaction_response_to import TransactionResponseTo

        d = dict(src_dict)
        amount = d.pop("amount")

        from_ = TransactionResponseFrom.from_dict(d.pop("from"))

        id = d.pop("id")

        time = isoparse(d.pop("time"))

        to = TransactionResponseTo.from_dict(d.pop("to"))

        def _parse_label(data: object) -> Union[None, Unset, str]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            return cast(Union[None, Unset, str], data)

        label = _parse_label(d.pop("label", UNSET))

        transaction_response = cls(
            amount=amount,
            from_=from_,
            id=id,
            time=time,
            to=to,
            label=label,
        )

        transaction_response.additional_properties = d
        return transaction_response

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
