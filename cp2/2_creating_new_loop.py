from threading import Thread
import asyncio
import sys


# loop = asyncio.new_event_loop()
# asyncio.set_event_loop(loop)
#
# if sys.platform != 'win32':
#     watcher = asyncio.get_child_watcher()
#     watcher.attach_loop(loop)


# !!!Wrong way to create loop
class LoopShowerThread(Thread):
    def run(self):
        try:
            loop = asyncio.get_event_loop()
            print(loop)
        except RuntimeError:
            print('No event loop!')


loop = asyncio.get_event_loop()
print(loop)

thread = LoopShowerThread()
thread.start()
thread.join()



