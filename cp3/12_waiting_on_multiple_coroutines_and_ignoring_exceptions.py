# wait on multiple coroutines and ignore exceptions using asyncio.gather and asyncio.shield:
import asyncio
import sys


async def print_delayed(delay, text, ):
    print(await asyncio.sleep(delay, text))


async def raise_delayed(delay, text, ):
    raise Exception(await asyncio.sleep(delay, text))


async def main():
    workload = [
        print_delayed(5, 'Printing this after 5 seconds'),
        raise_delayed(5, "Raising this after 5 seconds"),
        print_delayed(5, "Printing this after 5 seconds"),
    ]
    res = None
    try:
        gathered = asyncio.gather(*workload, return_exceptions=True)
        res = await gathered
    except asyncio.CancelledError:
        print("The gathered task was cancelled", file=sys.stderr)
    finally:
        print("Result:", res)


asyncio.run(main())


# We schedule our workload using asyncio.gather function; note that we also schedule a coroutine that will raise an
# exception.
# To shield against premature cancellation of our GatheringFuture, we wrap everything into a try except block since
# asyncio.shield has no effect.
# Note that the try except block just stops the CancelledError from bubbling up and the coroutines behind the
# GatheringFuture get cancelled nonetheless.
# Setting return_exceptions to True, however, turns all exceptions (also CancelledErrors) into return values.
# You can find them in the corresponding position of the returned list.
