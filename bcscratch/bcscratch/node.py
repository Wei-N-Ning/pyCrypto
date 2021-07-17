import asyncio
import structlog


from bcscratch.blockchain import Blockchain
from bcscratch.connections import ConnectionPool
from bcscratch.server import Server
from bcscratch.protocol import P2PProtocol


logger = structlog.get_logger()


if __name__ == '__main__':
    blockchain = Blockchain()
    connection_pool = ConnectionPool()
    server = Server(blockchain, connection_pool, P2PProtocol)

    async def main():
        await server.listen()

    # how to do proper exception handling:
    # https://www.roguelynn.com/words/asyncio-exception-handling/
    asyncio.run(main())
