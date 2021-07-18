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
import asyncio
from asyncio import *

import structlog

from bcscratch.messages import create_peers_message, create_block_message, create_transaction_message, \
    create_ping_message
from bcscratch.peers import PeerWriter
from bcscratch.server import *
from bcscratch.transactions import Transaction

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
        block_height = msg['payload']['block_height']
        w.__setattr__('is_miner', msg['payload']['is_miner'])
        peers = self.server.connection_pool.get_alive_peers(20)
        peers_message = create_peers_message(
            self.server.external_ip,
            self.server.external_port,
            peers)
        await self.send_message(w, peers_message)

        if block_height < self.server.blockchain.last_block().height:
            for block in self.server.blockchain.chain[block_height + 1:]:
                await self.send_message(
                    w,
                    create_block_message(
                        self.server.external_ip,
                        self.server.external_port,
                        block
                    )
                )

    async def handle_transaction(self, msg: dict, _: StreamWriter):
        tx = msg['payload']
        if Transaction.validate(tx):
            if tx not in self.server.blockchain.pending_transactions:
                self.server.blockchain.pending_transactions.append(tx)
                for peer in self.server.connection_pool.get_alive_peers(20):
                    await self.send_message(
                        peer,
                        create_transaction_message(
                            self.server.external_ip,
                            self.server.external_port,
                            tx
                        )
                    )

    async def handle_block(self, msg: dict, _: StreamWriter):
        block = msg['payload']
        self.server.blockchain.valid_add_block(block)
        for peer in self.server.connection_pool.get_alive_peers(20):
            await self.send_message(
                peer,
                create_block_message(
                    self.server.external_ip,
                    self.server.external_port,
                    block
                )
            )

    async def handle_peers(self, msg: dict, w: StreamWriter):
        peers = msg['payload']
        ping_message = create_ping_message(
            self.server.external_ip,
            self.server.external_port,
            len(self.server.blockchain.chain),
            len(self.server.connection_pool.get_alive_peers(50)),
            False
        )
        for peer in peers:
            _, w = await asyncio.open_connection(peer.address, peer.port)
            self.server.connection_pool.add_peer(PeerWriter(w, peer['ip'], peer['port']))
            await self.send_message(w, ping_message)
