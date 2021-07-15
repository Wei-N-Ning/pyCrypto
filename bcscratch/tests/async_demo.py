import asyncio
import time


async def greet(name: str, delay: float) -> None:
    await asyncio.sleep(delay)
    print(f'>>> ping {name} after {delay} seconds')


async def main():
    # task is of type await-able

    task_1 = asyncio.create_task(greet('doom', 0.2))
    task_2 = asyncio.create_task(greet('duke', 0.1))
    task_3 = asyncio.create_task(greet('dune', 0.3))
    start = time.time()
    await task_1
    await task_2
    await task_3
    print(time.time() - start)


asyncio.run(main())
