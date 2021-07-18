__all__ = [
    'PeerWriter', 'Peer'
]

import dataclasses
from asyncio import *
from time import time
from marshmallow import Schema, fields


@dataclasses.dataclass
class PeerWriter:
    w: StreamWriter
    address: str
    port: int

    def write(self, msg: str):
        self.w.write(msg.encode())

    def as_str(self) -> str:
        return f'{self.address}:{self.port}'


class Peer(Schema):
    ip = fields.Str(required=True)
    port = fields.Int(required=True)
    last_seen = fields.Int(missing=lambda: int(time()))
