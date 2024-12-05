# Better Proxy
[![Telegram channel](https://img.shields.io/endpoint?color=neon&url=https://tg.sumanjay.workers.dev/cum_insider)](https://t.me/cum_insider)
[![PyPI version info](https://img.shields.io/pypi/v/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)
[![PyPI downloads per month](https://img.shields.io/pypi/dm/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)

Proxy as a class

- The `Proxy.from_str()` method supports most proxy formats (with and without protocol):
    ```
    host:port:login:password
    host:port@login:password
    login:password@host:port
    login:password:host:port
    host:port
    ```
- The `Proxy.from_file()` method returns the list of proxies from the file at the specified path


```bash
pip install better-proxy
```

## aiohttp
```python
import aiohttp
from better_proxy import Proxy
from aiohttp_socks import ProxyConnector

proxy = Proxy.from_str("socks5://user:password@127.0.0.1:1080")

async def fetch(url):
    connector = ProxyConnector.from_url(proxy.as_url)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            return await response.text()
```

## requests
```python
import requests
from better_proxy import Proxy

proxy = Proxy.from_str("http://user:password@host:port")    

def fetch(url):
    response = requests.get(url, proxies=proxy.as_proxies_dict)    
    return response.text
```

## playwright
[Playwright: http proxy](https://playwright.dev/python/docs/network#http-proxy)

```python
from playwright.async_api import async_playwright, Playwright
from better_proxy import Proxy

proxy = Proxy.from_str("http://user:password@host:port")

async def fetch(playwright: Playwright, url):
    chromium = playwright.chromium
    browser = await chromium.launch(proxy=proxy.as_playwright_proxy)
    ...
```

## httpx
```python
import httpx
from better_proxy import Proxy

proxy = Proxy.from_str("login:password@210.173.88.77:3001")

async def fetch(url):
    async with httpx.AsyncClient(proxy=proxy.as_url) as client:
        response = await client.get(url)
        return response.text
```

## httpx-socks
```python
import httpx
from httpx_socks import AsyncProxyTransport
from better_proxy import Proxy

proxy = Proxy.from_str("socks5://login:password@210.173.88.77:3001")

async def fetch(url):
    transport = AsyncProxyTransport.from_url(proxy.as_url)
    async with httpx.AsyncClient(transport=transport) as client:
        response = await client.get(url)
        return response.text
```
