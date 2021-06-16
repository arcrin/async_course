# Problem: We have learned how to block until a coroutine has finished executing.
# But we want to defer the waiting to a certain place to decouple scheduling the coroutine.
# We also want to be able to pinpoint when it is finished and to schedule callbacks at that time.
import asyncio


async def coroutine_to_run():
    print(await asyncio.sleep(1, result="I have finished!"))


async def main():
    task = asyncio.create_task(coroutine_to_run())
    await task  # what is the benefit of this?
    # await coroutine_to_run()


asyncio.run(main())