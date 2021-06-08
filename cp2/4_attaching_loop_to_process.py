from multiprocessing import Process
import asyncio
import os
import random
import typing


processes = []


def cleanup():
    global processes
    while processes:
        proc = processes.pop()
        try:
            proc.join()
        except KeyboardInterrupt:
            proc.terminate()


async def worker():
    random_delay = random.randint(0, 3)
    result = await asyncio.sleep(random_delay, result=f'Working in process: {os.getpid()}')
    print(result)


def process_main(coroutine_worker: typing.Callable, number_of_couroutines: int):
    loop = asyncio.new_event_loop()
    try:
        workers = [coroutine_worker() for _ in range(number_of_couroutines)]
        loop.run_until_complete(asyncio.gather(*workers, loop=loop))
    except KeyboardInterrupt:
        print(f'Stopping {os.getpid()}')
        loop.stop()
    finally:
        loop.close()


def main(processes, number_of_processes, number_of_coroutines, process_main):
    for _ in range(number_of_processes):
        process = Process(target=process_main, args=(worker, number_of_coroutines))
        processes.append(process)
        process.start()


if __name__ == '__main__':
    try:
        main(processes, 10, 2, process_main)
    except KeyboardInterrupt:
        print('CTRL+C was pressed, Stopping all')