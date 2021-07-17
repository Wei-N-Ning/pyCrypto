import dataclasses
import hashlib
import json
from typing import List

from bcscratch.transactions import Transaction


@dataclasses.dataclass
class Block:
    height: int
    transactions: List[Transaction]
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
