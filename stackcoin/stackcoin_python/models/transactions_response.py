from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.transaction import Transaction
    from ..models.transactions_response_pagination import TransactionsResponsePagination


T = TypeVar("T", bound="TransactionsResponse")


@_attrs_define
class TransactionsResponse:
    """Response schema for multiple transactions

    Example:
        {'pagination': {'limit': 20, 'page': 1, 'total': 1, 'total_pages': 1}, 'transactions': [{'amount': 100, 'from':
            {'id': 123, 'username': 'johndoe'}, 'id': 456, 'label': 'Payment for services', 'time': '2019-09-12T12:34:55Z',
            'to': {'id': 789, 'username': 'janedoe'}}]}

    Attributes:
        pagination (Union[Unset, TransactionsResponsePagination]):
        transactions (Union[Unset, list['Transaction']]): The transactions list
    """

    pagination: Union[Unset, "TransactionsResponsePagination"] = UNSET
    transactions: Union[Unset, list["Transaction"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        pagination: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.pagination, Unset):
            pagination = self.pagination.to_dict()

        transactions: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.transactions, Unset):
            transactions = []
            for transactions_item_data in self.transactions:
                transactions_item = transactions_item_data.to_dict()
                transactions.append(transactions_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if pagination is not UNSET:
            field_dict["pagination"] = pagination
        if transactions is not UNSET:
            field_dict["transactions"] = transactions

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.transaction import Transaction
        from ..models.transactions_response_pagination import TransactionsResponsePagination

        d = dict(src_dict)
        _pagination = d.pop("pagination", UNSET)
        pagination: Union[Unset, TransactionsResponsePagination]
        if isinstance(_pagination, Unset):
            pagination = UNSET
        else:
            pagination = TransactionsResponsePagination.from_dict(_pagination)

        transactions = []
        _transactions = d.pop("transactions", UNSET)
        for transactions_item_data in _transactions or []:
            transactions_item = Transaction.from_dict(transactions_item_data)

            transactions.append(transactions_item)

        transactions_response = cls(
            pagination=pagination,
            transactions=transactions,
        )

        transactions_response.additional_properties = d
        return transactions_response

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
