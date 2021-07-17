__all__ = [
    'Peer'
]

import dataclasses
from asyncio import *


@dataclasses.dataclass
class Peer:
    w: StreamWriter
    address: str
    port: int

    def write(self, msg: str):
        self.w.write(msg.encode())

    def as_str(self) -> str:
        return f'{self.address}:{self.port}'
