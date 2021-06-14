# gather sample code
# from pprint import pprint
# import asyncio
# import random
#
#
# async def coro(tag):
#     print('>', tag)
#     random_sleep_time = random.uniform(1, 3)
#     await asyncio.sleep(random_sleep_time)
#     print('< {} slept for {}'.format(tag, random_sleep_time))
#     return tag
#
#
# loop = asyncio.get_event_loop()
#
# group1 = asyncio.gather(*[coro('group 1.{}'.format(i)) for i in range(1, 6)])
# group2 = asyncio.gather(*[coro('group 2.{}'.format(i)) for i in range(1, 4)])
# group3 = asyncio.gather(*[coro('group 3.{}'.format(i)) for i in range(1, 10)])
#
# all_groups = asyncio.gather(group1, group2, group3)
#
# results = loop.run_until_complete(all_groups)
#
# loop.close()
#
# pprint(results)


# wait sample code
import asyncio
import random


async def coro(tag):
    print('>', tag)
    random_sleep_time = random.uniform(0.5, 5)
    await asyncio.sleep(random_sleep_time)
    print('< {} slept for {}'.format(tag, random_sleep_time))
    return tag


loop = asyncio.get_event_loop()

tasks = [coro(i) for i in range(1, 11)]

print('Get first results:')
finished, unfinished = loop.run_until_complete(
    asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
)

for task in finished:
    print(task.result())

print("unfinished:", len(unfinished))

print("Get more results in 2 seconds:")
finished2, unfinished2 = loop.run_until_complete(
    asyncio.wait(unfinished, timeout=2)
)

for task in finished2:
    print(task.result())

print("unfinished2:", len(unfinished2))

print("Get all other results:")
finished3, unfinished3 = loop.run_until_complete(asyncio.wait(unfinished2))

for task in finished3:
    print(task.result())

loop.close()
