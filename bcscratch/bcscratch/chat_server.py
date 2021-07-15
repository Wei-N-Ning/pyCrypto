import asyncio
import textwrap
from typing import Set


class User:
    def __init__(self, name: str, w: asyncio.StreamWriter):
        self.w = w
        self.name = name


class ConnectionPool:
    def __init__(self):
        self.users: Set[User] = set()

    @staticmethod
    def send_welcome_message(u: User) -> None:
        u.w.write(textwrap.dedent(f'''
        welcome {u.name}
        help:
            /list: list all the active users
            /quit: screw you guys, I'm going home
        ''').encode())

    def broadcast(self, user: User, msg: str) -> None:
        for u in self.users:
            if u != user:
                u.w.write(f'[{user.name}] {msg}\n'.encode())

    def broadcast_user_join(self, user: User) -> None:
        for u in self.users:
            if u != user:
                u.w.write(f'<<<server>>> {user.name} has joined.\n'.encode())

    def broadcast_user_quit(self, user: User) -> None:
        for u in self.users:
            if u != user:
                u.w.write(f'<<<server>>> {user.name} has left.\n'.encode())

    def list_users(self, u: User) -> None:
        payload = '== active users ==\n' + \
                  '\n'.join(u.name for u in self.users) + \
                  '\n'
        u.w.write(payload.encode())

    def pool_new_user(self, u: User) -> None:
        self.users.add(u)
        self.send_welcome_message(u)
        self.broadcast_user_join(u)

    def remove_user(self, u: User) -> None:
        self.users.remove(u)
        self.broadcast_user_quit(u)


connection_pool = ConnectionPool()


# each user has an instance of this callback serving it
async def handle_connection(r: asyncio.StreamReader, w: asyncio.StreamWriter) -> None:
    w.write("> choose your name:\n".encode())
    resp = await r.readuntil(b'\n')
    u = User(resp.decode().strip(), w)
    connection_pool.pool_new_user(u)
    while True:
        try:
            data = await r.readuntil(b'\n')
        except asyncio.exceptions.IncompleteReadError:
            connection_pool.remove_user(u)
            break
        msg = data.decode().strip()
        if msg == '/quit':
            connection_pool.remove_user(u)
            break
        elif msg == '/list':
            connection_pool.list_users(u)
        else:
            connection_pool.broadcast(u, msg)

    await w.drain()
    w.close()
    await w.wait_closed()


async def main():
    server = await asyncio.start_server(handle_connection, '0.0.0.0', 8888)
    async with server:
        await server.serve_forever()


asyncio.run(main())
