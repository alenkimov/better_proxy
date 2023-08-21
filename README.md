# Better Proxy
[![Telegram channel](https://img.shields.io/endpoint?url=https://runkit.io/damiankrawczyk/telegram-badge/branches/master?url=https://t.me/cum_insider)](https://t.me/cum_insider)
[![PyPI version info](https://img.shields.io/pypi/v/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)
[![PyPI supported Python versions](https://img.shields.io/pypi/pyversions/better-proxy.svg)](https://pypi.python.org/pypi/better-proxy)


```bash
pip install better-proxy
```

```python
import aiohttp
from better_proxy import Proxy
from aiohttp_socks import ProxyConnector


async def fetch(url):
    proxy = Proxy('socks5://user:password@127.0.0.1:1080')
    connector = ProxyConnector.from_url(proxy.as_url)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        async with session.get(url) as response:
            return await response.text()
```