"""
This module contains logic to handle the propagation of messages
that peers may send us:

- how we communicate

will call this the P2PProtocol

(Note this module was called "peers" in the book;
here the peers.py module defines the actual Peer class
that represents each connected peer, wrapping the
StreamWriter)
"""

from asyncio import *


class P2PError(Exception):
    pass


class P2PProtocol:
    def __init__(self, server):
        pass

    @staticmethod
    async def send_message(w: StreamWriter, msg: str):
        pass

    async def handle_message(self, msg: str, w: StreamWriter):
        """
        This handles an incoming message passed by the server;

        It hands this message off to  a more specific method, named
          handle_<method_name>()
        Args:
            msg:
            w:

        Returns:

        """
        pass

    async def handle_ping(self, msg: str, w: StreamWriter):
        pass

    async def handle_block(self, msg: str, w: StreamWriter):
        pass

    async def handle_transaction(self, msg: str, w: StreamWriter):
        pass

    async def handle_peers(self, msg: str, w: StreamWriter):
        pass

