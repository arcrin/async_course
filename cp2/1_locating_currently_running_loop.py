# Locating currently running loop
# option 1
import asyncio

loop = asyncio.get_event_loop()

# option 2
# try:
#     loop = asyncio.get_running_loop()
# except RuntimeError:
#     print('No loop running')
