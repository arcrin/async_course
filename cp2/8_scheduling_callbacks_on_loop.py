# Solution 1
import asyncio

loop = asyncio.get_event_loop()
loop.call_soon(print, 'I am scheduled on a loop!')
loop.call_soon_threadsafe(print, 'I am scheduled on a loop but threadsafely!')
loop.call_later(1, print, 'I am scheduled on a loop in one seconds')
loop.call_at(loop.time() + 1, print, 'I am scheduled on a loop in one seconds too')

try:
    print('Stop the loop try by hitting the CTRL+C keys')
    # To see the callbacks running you need to start the running loop
    loop.run_forever()
except KeyboardInterrupt:
    loop.stop()
finally:
    loop.close()