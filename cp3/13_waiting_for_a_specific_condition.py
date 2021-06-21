# Problem: We want to create a simple API that allows us to wait for a coroutine if a condition of choice is invalid.
# Ideally, the API will allow us to pass our condition as a predicate function.

# Solution: asyncio provides an implementation of condition variables, a synchronization primitive.
# They enable coroutines to wait until a condition occurs.
import asyncio


async def execute_on(condition, coro, predicate):
    async with condition:
        await condition.wait_for(predicate)
        await coro


async def print_coro(text):
    print(text)


async def worker(numbers):
    while numbers:
        print("Numbers:", numbers)
        numbers.pop()
        await asyncio.sleep(0.25)


async def main():
    numbers = list(range(10))
    condition = asyncio.Condition()
    is_empty = lambda: not numbers
    await worker(numbers)
    await execute_on(condition, print_coro("Finished!"), is_empty)


asyncio.run(main())


# We can use a condition variable to monitor the completion of our worker coroutine, which pops the numbers inside the
# numbers list one after another.
# Condition variables provide us with implicit and explicit notifying. Either they monitor a predicate that's called
# Repeatedly until it becomes true or the waiters are notified by calling condition_variable.notify or
# condition_variable.notify_all.
# The example uses implicit notifying. Hence, our predicate function, which is is_empty = lambda: not numbers,
# must return True for the condition variable's lock to be freed.
# We define the helper coroutine function execute_on, which sets the lock inside the condition variable correctly.
# This happens before we use the wait_for coroutine method to wait until the predicate holds true and dispatch the
# passed coroutine.

# NOTE: if you use the condition variable in more than one coroutine, you need to pass your own asyncio.Lock instance!
