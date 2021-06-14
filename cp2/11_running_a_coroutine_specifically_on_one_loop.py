# Solution 1
# import asyncio
#
#
# async def main(loop):
#     print(loop == asyncio.get_running_loop())
#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(main(loop))

# Solution 2
import asyncio


async def main():
    print("main task")
    await asyncio.sleep(2)

loop = asyncio.get_event_loop()
task = loop.create_task(main())
task.add_done_callback(lambda fut: loop.stop())
# Or more generic if you don't have loop in scope:
# task.add_done_callback(lambda fut: asyncio.get_running_loop().stop())

loop.run_forever()
