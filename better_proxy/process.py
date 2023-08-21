from collections import defaultdict
from typing import Iterable, Callable

import aiohttp
from aiohttp_socks import ProxyConnector

from .proxy import Proxy
from .utils.other import bounded_gather


async def _process_accounts_with_session(
        accounts: Iterable,
        fn: Callable,
        *,
        proxy: Proxy = None,
):
    connector = ProxyConnector.from_url(proxy.as_url) if proxy else aiohttp.TCPConnector()
    async with aiohttp.ClientSession(connector=connector) as session:
        for account in accounts:
            await fn(session, account)


async def process_accounts_with_session(
        accounts: Iterable,
        proxies: Iterable[Proxy],
        fn: Callable,
        max_tasks: int = None,
):
    proxy_to_accounts: defaultdict[Proxy: list[accounts]] = defaultdict(list)
    if proxies:
        proxies = tuple(proxies)
        for i, account in enumerate(accounts):
            proxy = proxies[i % len(proxies)]
            proxy_to_accounts[proxy].append(account)
    else:
        proxy_to_accounts[None] = list(accounts)
    tasks = [_process_accounts_with_session(accounts, fn, proxy=proxy) for proxy, accounts in proxy_to_accounts.items()]
    await bounded_gather(tasks, max_tasks)
