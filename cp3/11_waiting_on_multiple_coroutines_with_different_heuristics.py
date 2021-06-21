# we can use asyncio.wait to wait on multiple coroutines with different herustics

# Solution 1: we will wait for multiple coroutines using asyncio.wait and asyncio.ALL_COMPLETED
# import asyncio
#
#
# async def raiser():
#     raise Exception('An exception was raised')
#
#
# async def main():
#     raiser_future = asyncio.ensure_future(raiser())
#     hello_world_future = asyncio.create_task(asyncio.sleep(1.0, "I have returned!"))
#     coros = {raiser_future, hello_world_future}
#     finished, pending = await asyncio.wait(coros, return_when=asyncio.ALL_COMPLETED)
#     assert raiser_future in finished
#     assert raiser_future not in pending
#     assert hello_world_future in finished
#     assert hello_world_future not in pending
#     print(raiser_future.exception())
#     print(hello_world_future.result())
#
#
# asyncio.run(main())

# Solution 2: We will wait for multiple coroutines using asyncio.wait and asyncio.FIRST_EXCEPTION
# import asyncio
#
#
# async def raiser():
#     raise Exception('An exception was raised')
#
#
# async def main():
#     raiser_future = asyncio.ensure_future(raiser())
#     hello_world_future = asyncio.create_task(asyncio.sleep(1.0, "I have returned!"))
#     coros = {raiser_future, hello_world_future}
#     finished, pending = await asyncio.wait(coros, return_when=asyncio.FIRST_EXCEPTION)
#     assert raiser_future in finished
#     assert raiser_future not in pending
#     assert hello_world_future not in finished
#     assert hello_world_future in pending
#     print(raiser_future.exception())
#     try:
#         print(hello_world_future.result())
#     except asyncio.InvalidStateError as err:
#         err_was_thrown = err
#     assert err_was_thrown
#
#
# asyncio.run(main())


# Solution 3: We will wait for multiple coroutines using asyncio.wait and asyncio.FIRST_COMPLETED
import asyncio


async def raiser():
    raise Exception('An exception was raised')


async def main():
    raiser_future = asyncio.ensure_future(raiser())
    hello_world_future = asyncio.create_task(asyncio.sleep(1.0, "I have returned!"))
    coros = {raiser_future, hello_world_future}
    finished, pending = await asyncio.wait(coros, return_when=asyncio.FIRST_COMPLETED)
    assert raiser_future in finished
    assert raiser_future not in pending
    assert hello_world_future not in finished
    assert hello_world_future in pending
    print(raiser_future.exception())
    err_was_thrown = None
    try:
        print(hello_world_future.result())
    except asyncio.InvalidStateError as err:
        err_was_thrown = err
    assert err_was_thrown


asyncio.run(main())

# the different solutions of this section demonstrate how asyncio.wait behaves with different values of the return_when
# parameter.
# asynio.wait is more low level than asyncio.gather in the sense that it can be used for grouping coroutines as well,
# but not for cancellation purposes. It takes a keyword-only parameter called return_when with the wait trategy.
# It returns with two values - two sets either containing the finished and the pending tasks.
# The allowed values for the return_when parameter are as follows:
# 1. FIRST_COMPLETED: Returns when any future finishes or is cancelled.
# 2. FIRST_EXCEPTION: Returns when any future finishes by raising an exception. If no future raises an exception,
#    then this value is equivalent to ALL_COMPLETED
# 3. ALL_COMPLETED: Returns when all futures finish or are cancelled

# NOTE: just calling raiser_future_exception() is not a safe option, since it might raise a CancelledError
