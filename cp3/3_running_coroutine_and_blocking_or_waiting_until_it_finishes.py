# Problem: A syntactic mechanism is needed to pinpoint the moment when a coroutine finishes.
# This mechanism must also be suspendable and resumable
import asyncio


async def coroutine(*args, **kwargs):
    print("Waiting for the next coroutine...")
    await another_coroutine(*args, **kwargs)
    print("This will follow 'Done'")


async def another_coroutine(*args, **kwargs):
    await asyncio.sleep(3)
    print("Done")


# asyncio.run(coroutine())
loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine())