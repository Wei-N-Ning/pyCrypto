"""
This module contains the logic to handle the pool of
active connections communicating with our node

"""

from asyncio import StreamWriter


class ConnectionPool:
    def __init__(self):
        self.pool = set()

    def add_peer(self, w: StreamWriter):
        self.pool.add(w)

    def remove_peer(self, w: StreamWriter):
        self.pool.remove(w)
