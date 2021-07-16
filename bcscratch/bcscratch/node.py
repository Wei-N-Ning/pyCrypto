import asyncio

from bcscratch.blockchain import Blockchain
from bcscratch.connections import ConnectionPool
from bcscratch.server import Server
from bcscratch.peers import P2PProtocol


if __name__ == '__main__':
    blockchain = Blockchain()
    connection_pool = ConnectionPool()
    server = Server(blockchain, connection_pool, P2PProtocol)

    async def main():
        await server.listen()

    asyncio.run(main())
