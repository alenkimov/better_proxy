# Better Proxy
[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/cum_insider)](https://t.me/cum_insider)
[![PyPI version info](https://img.shields.io/pypi/v/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)
[![PyPI downloads per month](https://img.shields.io/pypi/dm/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)



Представление такой сущности, как proxy в виде класса.
- Метод `Proxy.from_str()` поддерживает большинство форматом прокси (с протоколом и без):
    ```
    host:port:login:password
    host:port@login:password
    host:port|login:password
    login:password@host:port
    login:password:host:port
    host:port
    ```
- Реализованы методы `__hash__` и `__eq__`, что позволяет засовывть прокси в set()
- Метод `Proxy.from_file()` возвращает список прокси из файла по указанному пути


```bash
pip install better-proxy
```

More libraries of the family:
- [tweepy-self](https://github.com/alenkimov/tweepy-self)
- [better-web3](https://github.com/alenkimov/better_web3)

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