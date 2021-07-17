"""
This module contains the logic to handle the pool of
active connections communicating with our node

"""

from bcscratch.peers import *

from typing import *
from more_itertools import take


class ConnectionPool:
    def __init__(self):
        self.pool: Dict[str, Peer] = dict()

    def add_peer(self, p: Peer):
        self.pool[p.as_str()] = p

    def remove_peer(self, p: Peer):
        try:
            del self.pool[p.as_str()]
        except KeyError:
            pass

    def get_alive_peers(self, count: int) -> List[Peer]:
        return take(count, self.pool.values())

    def broadcast(self, msg: str):
        for _, p in self.pool.items():
            p.write(msg)
