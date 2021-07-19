__all__ = ['Blk', 'Block']

import dataclasses
import hashlib
import json
from typing import List

from marshmallow import Schema, fields, validates_schema, ValidationError

from bcscratch.transactions import TX, Transaction


@dataclasses.dataclass
class Blk:
    height: int
    transactions: List[TX]
    prev_hash: str
    # P/48
    # think of nonce as a one-off random number, which will be
    # used as an important source of randomness for our blocks
    nonce: str  # non-sense
    target: str
    timestamp: float

    def __post_init__(self):
        # reference on post_init:
        # https://www.python.org/dev/peps/pep-0557/#post-init-processing
        self._hash: str = \
            hashlib.sha256(self.dumps().encode()).hexdigest()

    def dumps(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True, indent=None)

    @property
    def index(self):
        # this book uses index and height interchangeably, BAD
        return self.height

    @property
    def hash(self):
        return self._hash


class Block(Schema):
    """
    Note:
        how to model nested fields correctly:
        https://marshmallow.readthedocs.io/en/stable/nesting.html

        (do not instantiate the child schema, just pass its type)
    """
    mined_by = fields.Str(required=False)
    transactions = fields.Nested(Transaction, many=True)
    height = fields.Int(required=True)
    target = fields.Str(required=True)
    hash = fields.Str(required=True)
    prev_hash = fields.Str(required=True)
    nonce = fields.Str(required=True)
    timestamp = fields.Int(required=True)

    class Meta:
        ordered = True

    @validates_schema
    def validate_hash(self, data: dict, **kwargs):
        block = data.copy()
        block.pop('hash')
        if data['hash'] != hashlib.sha256(json.dumps(block, sort_keys=True, indent=None).encode()).hexdigest():
            raise ValidationError('Fraudulent block: hashes do not match')
