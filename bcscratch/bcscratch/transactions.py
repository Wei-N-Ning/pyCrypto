__all__ = ['TX', 'Transaction']

import dataclasses
import json

from marshmallow import Schema, fields


@dataclasses.dataclass
class TX:
    """
    TX is the internal model object.

    It is instantiated from a Schema Object "Transaction".
    """
    sender: str
    recipient: str
    amount: int

    def dumps(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True, indent=None)

    @staticmethod
    def validate(payload: str) -> bool:
        return False


class Transaction(Schema):
    """
    Transaction is a Schema Object.

    It is deserialized from the message payload if it passes schema validation.
    """
    timestamp = fields.Int(required=True)
    sender = fields.Str(required=True)
    receiver = fields.Str(required=True)
    amount = fields.Int(required=True)
    signature = fields.Str(required=True)

    class Meta:
        ordered = True
