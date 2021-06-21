# asyncio.gather method is a high-level tool that can be used to group coroutines while silencing the emitted exceptions
# and returning them as a result value. The exceptions are returned by using the keyword-only argument return_exceptions

# Using asyncio.gather, we can:
#   1. Schedule all the coroutines passed to it concurrently
#   2. Receive a GatheringFuture, which can be used to cancel all coroutines at the same time
# If waited successfully, asyncio.gather returns a list of all the results. asyncio.gather supports a keyword-only
# argument called return_exceptions, which can alter the result set on the GatheringFuture.
# If an exception occurs in one of the scheduled coroutines, it can either bubble up or be returned as an argument.
# Note: Irrespective of the return_exceptions argument being st to True or not, the cancellation of the GatheringFuture
# is always propagated (since 3.7). i.e. All coroutines will be cancelled even if there is an exception on one of them
import asyncio


async def cancellable(delay=10, *, loop):
    try:
        now = loop.time()
        print(f'Sleeping from {now} for {delay} seconds...')
        await asyncio.sleep(delay)
        print(f'Slept for {delay} seconds without disturbance...')
    except asyncio.CancelledError:
        print(f'Cancelled at {now} after {loop.time() - now}')


def canceller(task, fut):
    task.cancel()
    fut.set_result(None)


async def cancel_threadsafe(gathered_tasks, loop):
    fut = loop.create_future()
    loop.call_soon_threadsafe(canceller, gathered_tasks, fut)
    await fut


async def main():
    loop = asyncio.get_running_loop()
    coros = [cancellable(i, loop=loop) for i in range(10)]
    gathered_tasks = asyncio.gather(*coros)
    # Add a delay here, so we can see that the first three coroutines run uninterrupted
    await asyncio.sleep(2)
    await cancel_threadsafe(gathered_tasks, loop)
    try:
        await gathered_tasks
    except asyncio.CancelledError:
        print('Was cancelled')


asyncio.run(main())