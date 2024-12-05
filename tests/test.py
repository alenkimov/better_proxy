"""
https://github.com/BotsForge/proxystr/blob/main/tests/test_proxy.py
"""

import unittest


from better_proxy import Proxy
from better_proxy.proxy import PlaywrightProxySettings


class TestProxy(unittest.TestCase):
    def test_input_formats(self):
        default = Proxy.from_str('login:password@210.173.88.77:3001')
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001'), default)
        self.assertEqual(Proxy.from_str('login:password:210.173.88.77:3001'), default)
        self.assertEqual(Proxy.from_str('210.173.88.77:3001:login:password'), default)
        self.assertEqual(Proxy.from_str('http://login:password@210.173.88.77:3001'), default)

        default = Proxy.from_str('socks5://login:password@210.173.88.77:3001')
        self.assertEqual(Proxy.from_str('socks5://login:password@210.173.88.77:3001'), default)
        self.assertEqual(Proxy.from_str('socks5://login:password@210.173.88.77:3001'), default)

    def test_wrong_input_formats(self):
        with self.assertRaises(ValueError):
            Proxy.from_str('login:pass@word@210.173.88.77:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@210.173.88.77:300111')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@210.173.88.77.23:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@210.173.88:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@proxy. com:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@210.173.88.999:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('socks99://login:password@210.173.88.88:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('http:/login:password@210.173.88.999:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('socks://login:password@210.173.88.999:3001')
        with self.assertRaises(ValueError):
            Proxy.from_str('login:password@210.173.88.77:3001[https://proxy. com?refresh=123]')

    def test_host(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001').host, '210.173.88.77')

    def test_port(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001').port, 3001)

    def test_refresh_url(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001[https://myproxy.com?refresh=123]').refresh_url,
                         'https://myproxy.com?refresh=123')

    def test_login(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001').login, 'login')

    def test_password(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001').password, 'password')
        self.assertEqual(Proxy.from_str('login:pass:word@210.173.88.77:3001').password, 'pass:word')

    def test_protocol(self):
        self.assertEqual(Proxy.from_str('login:password@210.173.88.77:3001').protocol, 'http')
        self.assertEqual(Proxy.from_str('socks5://login:password@210.173.88.77:3001').protocol, 'socks5')

    def test_url(self):
        self.assertEqual(Proxy.from_str('210.173.88.77:3001:login:password').as_url,
                         'http://login:password@210.173.88.77:3001')
        self.assertEqual(Proxy.from_str('socks5://210.173.88.77:3001:login:password').as_url,
                         'socks5://login:password@210.173.88.77:3001')

    def test_dict(self):
        d1 = {
            'http': 'http://login:password@210.173.88.77:3001',
            'https': 'http://login:password@210.173.88.77:3001',
        }
        d2 = {'socks5': 'socks5://login:password@210.173.88.77:3001'}
        self.assertEqual(Proxy.from_str('210.173.88.77:3001:login:password').as_proxies_dict, d1)
        self.assertEqual(Proxy.from_str('socks5://210.173.88.77:3001:login:password').as_proxies_dict, d2)

    def test_server(self):
        self.assertEqual(Proxy.from_str('socks5://210.173.88.77:3001:login:password').server, 'socks5://210.173.88.77:3001')
        self.assertEqual(Proxy.from_str('210.173.88.77:3001:login:password').server, 'http://210.173.88.77:3001')

    def test_playwright(self):
        r1 = PlaywrightProxySettings(
            server='http://210.173.88.77:3001',
            password='password',
            username='login',
        )
        r2 = PlaywrightProxySettings(
            server='http://210.173.88.77:3001',
            password=None,
            username=None,
        )
        self.assertEqual(Proxy.from_str('210.173.88.77:3001:login:password').as_playwright_proxy, r1)
        self.assertEqual(Proxy.from_str('210.173.88.77:3001').as_playwright_proxy, r2)


if __name__ == '__main__':
    unittest.main()
