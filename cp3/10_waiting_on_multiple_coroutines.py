# We have two options to wait on multiple coroutines:
# 1. asyncio.gather
# 2. asyncio.wait
# Both have their use cases. The asyncio.gather function provides a way to group and wait/cancel multiple
# coroutines at a time.
# If your only use case is to schedule multiple coroutines at the same time, you can safely assume that
# asyncio.gather is sufficient to do the job.
import asyncio


async def print_delayed(delay, text, result):
    print(await asyncio.sleep(delay, text))
    return result


async def main():
    workload = [
        print_delayed(1, 'Printing this after 1 seconds', 1),
        print_delayed(2, 'Printing this after 2 seconds', 2),
        print_delayed(3, 'Printing this after 3 seconds', 3),
    ]
    results = await asyncio.gather(*workload)
    print(results)


asyncio.run(main())

# asyncio.gather schedules and executes multiple coroutines or futures using asyncio.ensure_future.
# It uses asyncio.get_event_loop for querying the current event loop in the case of coroutines or
# asyncio.Future.get_loop in the case of futures before passing both of them to asyncio.ensure_future
# for scheduling.

