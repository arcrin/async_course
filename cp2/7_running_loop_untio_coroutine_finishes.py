# Solution 1
# import asyncio
#
#
# async def main():
#     pass
#
# asyncio.run(main())


# Solution 2
# import asyncio
#
#
# async def main():
#     pass
#
# loop = asyncio.get_event_loop()
#
# try:
#     loop.run_until_complete(main())
# finally:
#     try:
#         loop.run_until_complete(loop.shutdown_asyncgens())
#     finally:
#         loop.close()


# Solution 3
import asyncio
import sys


async def main():
    pass


loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

if sys.platform != "win32":
    watcher = asyncio.get_child_watcher()
    watcher.attach_loop(loop)

try:
    loop.run_forever()
finally:
    try:
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()