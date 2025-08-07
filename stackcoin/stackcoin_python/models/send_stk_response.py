from collections.abc import Mapping
from typing import Any, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="SendStkResponse")


@_attrs_define
class SendStkResponse:
    """Response schema for sending STK

    Example:
        {'amount': 100, 'from_new_balance': 900, 'success': True, 'to_new_balance': 600, 'transaction_id': 456}

    Attributes:
        amount (int): Amount sent
        from_new_balance (int): Sender's new balance
        success (bool): Whether the operation succeeded
        to_new_balance (int): Recipient's new balance
        transaction_id (int): Created transaction ID
    """

    amount: int
    from_new_balance: int
    success: bool
    to_new_balance: int
    transaction_id: int
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        amount = self.amount

        from_new_balance = self.from_new_balance

        success = self.success

        to_new_balance = self.to_new_balance

        transaction_id = self.transaction_id

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "amount": amount,
                "from_new_balance": from_new_balance,
                "success": success,
                "to_new_balance": to_new_balance,
                "transaction_id": transaction_id,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        amount = d.pop("amount")

        from_new_balance = d.pop("from_new_balance")

        success = d.pop("success")

        to_new_balance = d.pop("to_new_balance")

        transaction_id = d.pop("transaction_id")

        send_stk_response = cls(
            amount=amount,
            from_new_balance=from_new_balance,
            success=success,
            to_new_balance=to_new_balance,
            transaction_id=transaction_id,
        )

        send_stk_response.additional_properties = d
        return send_stk_response

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
