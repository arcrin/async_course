# after shielding your task, you can safely call cancel on the shielded task without fearing that the coroutine/task
# that's shielded will also be cancelled.
# NOTE: that you cannot safeguard a coroutine form being cancelled from within itself with asyncio.shield.
# Given how asyncio.shield is implemented (in python 3.7), it will add another task to the global task list.
# Hence, if you have shutdown logic that works along the lines of gather(*all_tasks()).cancel(),
# you might cancel the inner task of the shield operation.
import asyncio


async def cancellable(delay=10):
    now = asyncio.get_running_loop().time()
    try:
        print(f'Sleeping from {now} for {delay} seconds...')
        await asyncio.sleep(delay)
        print(f'Slept for {delay} seconds without disturbance...')
    except asyncio.CancelledError:
        print('I was disturbed in my sleep!')


def canceller(task, fut):
    task.cancel()
    fut.set_result(None)


async def cancel_threadsafe(task, *, delay=3, loop):
    await asyncio.sleep(delay)
    fut = loop.create_future()
    loop.call_soon_threadsafe(canceller, task, fut)
    await fut


async def main():
    complete_time = 10
    cancel_after = 3
    loop = asyncio.get_running_loop()
    coro = cancellable(delay=complete_time)
    shielded_task = asyncio.shield(coro)
    asyncio.create_task(cancel_threadsafe(shielded_task, delay=cancel_after, loop=loop))
    try:
        await shielded_task
    except asyncio.CancelledError:
        await asyncio.sleep(complete_time - cancel_after)


asyncio.run(main())
