import asyncio


async def handle_connection(r: asyncio.StreamReader, w: asyncio.StreamWriter) -> None:
    w.write("= ready\n".encode())
    data = await r.readuntil(b'\n')
    w.write('. received '.encode() + data + '\n'.encode())
    await w.drain()
    w.close()
    await w.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, '0.0.0.0', 8888)
    async with server:
        await server.serve_forever()


asyncio.run(main())
