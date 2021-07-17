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

import structlog

from bcscratch.server import *

logger = structlog.get_logger()


class P2PError(Exception):
    pass


message_schema = {
    'meta': {
        'address': {
            'ip': '<external ip: str>',
            'port': '<external port: int>'
        },
        'client': 'bcscratch 0.1'
    },
    'message': {
        'name': '<message name: str>',
        'payload': '<message payload: object>'
    }
}


class P2PProtocol:
    def __init__(self, server: Server):
        self.server: Server = server
        self.blockchain = server.blockchain

    @staticmethod
    async def send_message(w: StreamWriter, msg: str):
        w.write(msg.encode() + b'\n')

    async def handle_message(self, msg: dict, w: StreamWriter):
        """
        This handles an incoming message passed by the server;

        It hands this message off to  a more specific method, named
          handle_<method_name>()
        Args:
            msg:
            w:

        Returns:

        """
        if msg['name'] == 'ping':
            await self.handle_ping(msg, w)
        elif msg['name'] == 'block':
            await self.handle_block(msg, w)
        elif msg['name'] == 'transaction':
            await self.handle_transaction(msg, w)
        elif msg['name'] == 'peers':
            await self.handle_peers(msg, w)
        else:
            raise P2PError('Missing handler name for message')

    async def handle_ping(self, msg: dict, w: StreamWriter):
        pass

    async def handle_block(self, msg: dict, w: StreamWriter):
        pass

    async def handle_transaction(self, msg: dict, w: StreamWriter):
        pass

    async def handle_peers(self, msg: dict, w: StreamWriter):
        pass
