# Problem: Given a coroutine that needs to be scheduled and a timeout in seconds, how do we cancel a scheduled toutine
# if it doesn't complete in that timeframe?
import asyncio


async def delayed_print(text, delay):
    print(await asyncio.sleep(delay, text))


async def main():
    delay = 3
    on_time_coro = delayed_print(f'I will print after {delay} seconds', delay)
    await asyncio.wait_for(on_time_coro, delay + 1)

    try:
        delayed_coro = delayed_print(f'I will print after {delay + 1} seconds', delay + 1)
        await asyncio.wait_for(delayed_coro, delay)
    except asyncio.TimeoutError:
        print(f'I timed out after {delay} seconds')

asyncio.run(main())
