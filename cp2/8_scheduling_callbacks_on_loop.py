# Solution 1
# import asyncio
#
# loop = asyncio.get_event_loop()
# loop.call_soon(print, 'I am scheduled on a loop!')
# loop.call_soon_threadsafe(print, 'I am scheduled on a loop but threadsafely!')
# loop.call_later(1, print, 'I am scheduled on a loop in one second')
# loop.call_at(loop.time() + 1, print, 'I am scheduled on a loop in one second too')
#
# try:
#     print('Stop the loop by hitting the CTRL+C keys')
#     loop.run_forever()
# except KeyboardInterrupt:
#     loop.stop()
# finally:
#     loop.close()

# Solution 2
import asyncio
from functools import partial as func


class SchedulerLoop(asyncio.SelectorEventLoop):
    def __init__(self):
        super(SchedulerLoop, self).__init__()
        self._scheduled_callback_futures = []

    @staticmethod
    def unwrapper(fut: asyncio.Future, function):
        """
        FUnction to get rid of the implicit fut parameter
        :param fut:
        :param function:
        :return:
        """
        return function()

    def _future(self, done_hook):
        """
        Create a future object that calls the done_hook when it is awaited
        :param done_hook:
        :return:
        """
        fut = self.create_future()
        fut.add_done_callback(func(self.unwrapper, function=done_hook))
        return fut

    def schedule_soon_threadsafe(self, callback, *args, context=None):
        fut = self._future(func(callback, *args))
        self._scheduled_callback_futures.append(fut)
        self.call_soon_threadsafe(fut.set_result, None, context=context)

    def schedule_soon(self, callback, *args, context=None):
        fut = self._future(func(callback, *args))
        self._scheduled_callback_futures.append(fut)
        self.call_soon(fut.set_result, None, context=context)

    def schedule_later(self, delay_in_seconds, callback, *args, context=None):
        fut = self._future(func(callback, *args))
        self._scheduled_callback_futures.append(fut)
        self.call_later(delay_in_seconds, fut.set_result, None, context=context)

    def schedule_at(self, delay_in_seconds, callback, *args, context=None):
        fut = self._future(func(callback, *args))
        self._scheduled_callback_futures.append(fut)
        self.call_at(delay_in_seconds, fut.set_result, None, context=context)

    async def await_callbacks(self):
        callback_futs = self._scheduled_callback_futures[:]
        self._scheduled_callback_futures[:] = []
        await asyncio.gather(*callback_futs)


async def main(loop):
    loop.schedule_soon_threadsafe(print, 'hallo')
    loop.schedule_soon(print, 'This will be printed when the loop starts running')

    def callback(value):
        print(value)

    loop.schedule_soon_threadsafe(func(callback, value='This will get printed when the loop starts running'))
    offset_in_seconds = 4
    loop.schedule_at(loop.time() + offset_in_seconds,
                     func(print, f'This will be printed after {offset_in_seconds} seconds'))
    loop.schedule_later(offset_in_seconds, func(print, f'This will be printed after {offset_in_seconds} seconds too'))
    await loop.await_callbacks()

loop = SchedulerLoop()
loop.run_until_complete(main(loop))
