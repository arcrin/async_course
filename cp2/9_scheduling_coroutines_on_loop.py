# Solution 1 - option 1
# import asyncio
# import random
#
#
# async def work(i):
#     print(await asyncio.sleep(random.randint(0, i), result=f'Concurrent work {i}'))
#
#
# async def main():
#     tasks = [asyncio.ensure_future(work(i)) for i in range(10)]
#     await asyncio.gather(*tasks)
#
# asyncio.run(main())


# Solution 1 - option 2
# import asyncio
# import random
# 
# 
# async def work(i):
#     print(await asyncio.sleep(random.randint(0, i), result=f'Concurrent work {i}'))
# 
# loop = asyncio.get_event_loop()
# tasks = [asyncio.ensure_future(work(i)) for i in range(10)]
# loop.run_until_complete(asyncio.gather(*tasks))


# Solution 2
import asyncio
from asyncio import AbstractEventLoop


async def work():
    print('Main was called')
    

class AsyncSchedulerLoop(asyncio.SelectorEventLoop):
    def __init__(self):
        super(AsyncSchedulerLoop, self).__init__()
        self.coros = asyncio.Queue(loop=self)

    def schedule(self, coro):
        task = self.create_task(coro)
        task.add_done_callback(lambda _: self.coros.task_done())
        self.coros.put_nowait(task)

    async def wait_for_all(self):
        await self.coros.join()


class AsyncSchedulerLoopPolicy(asyncio.DefaultEventLoopPolicy):
    def new_event_loop(self) -> AbstractEventLoop:
        return AsyncSchedulerLoop()


asyncio.set_event_loop_policy(AsyncSchedulerLoopPolicy())
loop = asyncio.get_event_loop()
for i in range(1000):
    loop.schedule(work())

loop.run_until_complete(loop.wait_for_all())