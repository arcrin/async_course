from concurrent.futures.thread import ThreadPoolExecutor
import asyncio
import certifi
import urllib3


HTTP_POOL_MANAGER = urllib3.PoolManager(ca_certs=certifi.where())
EXECUTOR = ThreadPoolExecutor(10)
URL = 'https://apress.com'


async def block_request(http, url, n, *, executor=None, loop: asyncio.AbstractEventLoop):
    return await loop.run_in_executor(executor, http.request, 'GET', url)


def multi_block_requests(http, url, n, *, executor=None)