import dataclasses
import json


@dataclasses.dataclass
class Transaction:
    sender: str
    recipient: str
    amount: int

    def dumps(self):
        return json.dumps(dataclasses.asdict(self), sort_keys=True, indent=None)
