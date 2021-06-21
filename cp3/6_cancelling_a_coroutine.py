# Solution 1:
# This solution is most obvious. A task is the instance of a future subclass and hence has a cancel method,
# which can be invoked to unschedule the corresponding coroutine from the event loop and abort it
# This happens irrespective of what the current thread is. You can do this if you know that your application is
# single-threaded or you are absolutely sure that the loop you are handling is in fact on the same thread
# import asyncio
#
#
# async def cancellable(delay=10):
#     loop = asyncio.get_running_loop()
#     try:
#         now = loop.time()
#         print(f'Sleeping from {now} for {delay} seconds...')
#         await asyncio.sleep(delay, loop=loop)
#         print(f'Slept {delay} seconds...')
#     except asyncio.CancelledError:
#         print(f'Cancelled at {now} after {loop.time() - now} seconds')
#
#
# async def main():
#     coro = cancellable()
#     task = asyncio.create_task(coro)
#     await asyncio.sleep(3)
#     task.cancel()
#
#
# asyncio.run(main())

# Solution 2: If you are on another thread, you can't safely schedule a callback with loop.call_soon or loop.call_at
# You need to use the loop.call_threadsafe method for that, which happens to be scheduled asynchronously as well.
# To be able to tell when the scheduled coroutine has finished,
# you can pass a future object and call it at the right time and then await it on the outside.
import asyncio


async def cancellable(delay=10):
    loop = asyncio.get_running_loop()
    try:
        now = loop.time()
        print(f'Sleeping from {now} for {delay} seconds...')
        await asyncio.sleep(delay)
        print(f'Slept for {delay} seconds without disturbance...')
    except asyncio.CancelledError:
        print(f'Cancelled at {now} after {loop.time() - now} seconds')


async def main():
    coro = cancellable()
    task = asyncio.create_task(coro)
    await asyncio.sleep(3)

    def canceller(task, fut):
        task.cancel()
        fut.set_result(None)
    loop = asyncio.get_running_loop()
    fut = loop.create_future()
    loop.call_soon_threadsafe(canceller, task, fut)
    await fut


asyncio.run(main())