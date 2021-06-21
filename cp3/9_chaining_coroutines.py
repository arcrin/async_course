# Problem: Using concurrency does not mean our code is free from assumptions about ordering and consequence.
# In fact, it is even more essential to have a way to express them in an easily understandable fashion

# Solution: For this purpose, we can deploy the await keyword,
# which can be used to block the execution of awaitables until the either return or are cancelled.
import asyncio


async def print_delayed(delay, text):
    print(await asyncio.sleep(delay, text))


async def main():
    await print_delayed(1, "Printing this after 1 second")
    await print_delayed(1, "Printing this after 2 seconds")
    await print_delayed(1, "Printing this after 3 seconds")


asyncio.run(main())

# Just one coroutine can run at the same time on a loop, since a coroutine also runs under the GIL.
# We use the await keyword to schedule an awaitable on the loop with the premise of returning from that call when
# the awaitable has finished executing or has been cancelled.
# Awaitables can be one of the following:
# 1. a native coroutine object returned from a native coroutine function
# 2. a generator-based coroutine object returned from a function decorated with @asyncio.coroutine()
# 3. an object with an __await__ method returning an iterator (futures fall in this category)
# You can check for an awiatable by means of inspect.isawatable

