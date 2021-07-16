"""
A basic TCP server
"""
from asyncio import StreamWriter, StreamReader, start_server
from asyncio.exceptions import IncompleteReadError

import structlog
from marshmallow.exceptions import MarshmallowError

from bcscratch.messages import BaseSchema
from bcscratch.utils import get_external_ip

logger = structlog.get_logger()


class Server:
    def __init__(self, blockchain, connection_pool, protocol):
        self.blockchain = blockchain
        self.connection_pool = connection_pool
        self.protocol = protocol
        self.external_ip = None
        self.external_port = None

    def start(self):
        pass

    async def get_external_ip(self):
        """

        Returns:
            the external ip address so that we can advertise it
            to our peers
        """
        self.external_ip = await get_external_ip()

    @staticmethod
    def try_schema_load(payload: str) -> (object, bool):
        try:
            return BaseSchema().loads(payload), True
        except MarshmallowError:
            return None, False

    async def handle_connection(self, r: StreamReader, w: StreamWriter):
        """

        Args:
            r:
            w: represents the connecting peer

        Returns:

        """
        while True:
            try:
                data = await r.readuntil(b'\n')
                decoded_data = data.decode().strip()
                msg, ok = self.try_schema_load(decoded_data)
                if not ok:
                    logger.info(f'Received unreadable message from peer: {w}')
                    break
                w.address = msg['meta']['address']
                self.connection_pool.add_peer(w)
                await self.protocol.handle_message(msg, w)
                await w.drain()
                if w.is_closing():
                    break
            except (ConnectionError, IncompleteReadError):
                break
        w.close()
        await w.wait_closed()
        self.connection_pool.remove_peer(w)

    async def listen(self, hostname='0.0.0.0', port=8888):
        server = await start_server(self.handle_connection, host=hostname, port=port)
        logger.info(f'Server listening on {hostname}:{port}')
        async with server:
            await server.serve_forever()
