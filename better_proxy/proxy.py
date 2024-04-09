import re
from pathlib import Path
from typing import Literal, TypedDict

from pydantic import BaseModel


Protocol = Literal["http", "https", "SOP2", "SOP3", "socks4", "socks5"]
PROXY_FORMATS_REGEXP = [
    re.compile(r'^(?:(?P<protocol>.+)://)?(?P<login>[^:]+):(?P<password>[^@|:]+)[@|:](?P<host>[^:]+):(?P<port>\d+)$'),
    re.compile(r'^(?:(?P<protocol>.+)://)?(?P<host>[^:]+):(?P<port>\d+)[@|:](?P<login>[^:]+):(?P<password>[^:]+)$'),
    re.compile(r'^(?:(?P<protocol>.+)://)?(?P<host>[^:]+):(?P<port>\d+)$'),
]


class ParsedProxy(TypedDict):
    host: str
    port: int
    protocol: Protocol | None
    login:    str | None
    password: str | None


def parse_proxy_str(proxy: str) -> ParsedProxy:
    for pattern in PROXY_FORMATS_REGEXP:
        match = pattern.match(proxy)
        if match:
            groups = match.groupdict()
            return {
                "host": groups["host"],
                "port": int(groups["port"]),
                "protocol": groups.get("protocol"),
                "login": groups.get("login"),
                "password": groups.get("password"),
            }

    raise ValueError(f'Unsupported proxy format: {proxy}')


def _load_lines(filepath: Path | str) -> list[str]:
    with open(filepath, "r") as file:
        return [line.strip() for line in file.readlines() if line != "\n"]


class PlaywrightProxySettings(TypedDict, total=False):
    server:   str
    bypass:   str | None
    username: str | None
    password: str | None


class Proxy(BaseModel):
    host: str
    port: int
    protocol: Protocol = "http"
    login:    str | None = None
    password: str | None = None
    refresh_url: str | None = None

    @classmethod
    def from_str(cls, proxy: str or "Proxy") -> "Proxy":
        if type(proxy) is cls or issubclass(type(proxy), cls):
            return proxy

        parsed_proxy = parse_proxy_str(proxy)
        parsed_proxy["protocol"] = parsed_proxy["protocol"] or "http"
        return cls(**parsed_proxy)

    @classmethod
    def from_file(cls, filepath: Path | str) -> list["Proxy"]:
        return [cls.from_str(proxy) for proxy in _load_lines(filepath)]

    @property
    def as_url(self) -> str:
        return (f"{self.protocol}://"
                + (f"{self.login}:{self.password}@" if self.login and self.password else "")
                + f"{self.host}:{self.port}")

    @property
    def server(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"

    @property
    def as_playwright_proxy(self) -> PlaywrightProxySettings:
        return PlaywrightProxySettings(
            server=self.server,
            password=self.password,
            username=self.login,
        )

    @property
    def fixed_length(self) -> str:
        return f"[{self.host:>15}:{str(self.port):<5}]".replace(" ", "_")

    def __repr__(self):
        return f"Proxy(host={self.host}, port={self.port})"

    def __str__(self) -> str:
        return self.as_url

    def __hash__(self):
        return hash((self.host, self.port, self.protocol, self.login, self.password))

    def __eq__(self, other):
        if isinstance(other, Proxy):
            return (
                self.host == other.host
                and self.port == other.port
                and self.protocol == other.protocol
                and self.login == other.login
                and self.password == other.password
            )
        return False
