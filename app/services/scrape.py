from __future__ import annotations

from html.parser import HTMLParser
import ipaddress
import socket
from typing import Optional
from urllib.parse import urlparse
from urllib.request import Request, urlopen


class JobPostingParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, str] = {}
        self.title: Optional[str] = None
        self.h1: Optional[str] = None
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "meta":
            attr_map = {key.lower(): value for key, value in attrs if key}
            content = attr_map.get("content")
            if not content:
                return
            name = attr_map.get("property") or attr_map.get("name")
            if name:
                self.meta[name.lower()] = content.strip()
        elif tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data: str) -> None:
        if self._in_title and not self.title:
            cleaned = data.strip()
            if cleaned:
                self.title = cleaned
        elif self._in_h1 and not self.h1:
            cleaned = data.strip()
            if cleaned:
                self.h1 = cleaned


def _split_title(title: str) -> tuple[Optional[str], Optional[str]]:
    separators = [" at ", " @ ", " - ", " | ", " – ", " — "]
    for sep in separators:
        if sep in title:
            left, right = [part.strip() for part in title.split(sep, 1)]
            if not left or not right:
                continue
            if sep in {" at ", " @ "}:
                return left, right
            return left, right
    return None, None


def _clean_company(company: str) -> str:
    suffixes = ["careers", "jobs", "job openings"]
    cleaned = company.strip()
    for suffix in suffixes:
        if cleaned.lower().endswith(suffix):
            cleaned = cleaned[: -len(suffix)].strip(" -|")
    return cleaned


def _host_is_public(hostname: str) -> bool:
    try:
        ip = ipaddress.ip_address(hostname)
    except ValueError:
        try:
            resolved = socket.getaddrinfo(hostname, None)
        except socket.gaierror as exc:
            raise ValueError("Unable to resolve host") from exc
        for _, _, _, _, sockaddr in resolved:
            addr = sockaddr[0]
            if not ipaddress.ip_address(addr).is_global:
                return False
        return True
    return ip.is_global


def scrape_job_posting(url: str) -> dict[str, Optional[str]]:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"}:
        raise ValueError("URL must start with http or https")
    if not parsed.hostname:
        raise ValueError("URL must include a hostname")
    if not _host_is_public(parsed.hostname):
        raise ValueError("URL must resolve to a public host")

    request = Request(url, headers={"User-Agent": "ApplicationTracker/1.0"})
    with urlopen(request, timeout=10) as response:  # noqa: S310
        charset = response.headers.get_content_charset() or "utf-8"
        content = response.read(2_000_000).decode(charset, errors="ignore")

    parser = JobPostingParser()
    parser.feed(content)

    meta = parser.meta
    title_candidate = (
        meta.get("og:title")
        or meta.get("twitter:title")
        or parser.title
        or parser.h1
    )
    company_candidate = (
        meta.get("og:site_name")
        or meta.get("twitter:site")
        or meta.get("application-name")
        or meta.get("og:app_name")
    )

    role_title = None
    company = None

    if title_candidate:
        role_title, company = _split_title(title_candidate)

    if company and not company_candidate:
        company_candidate = company

    if not role_title and parser.h1:
        role_title = parser.h1

    location = None
    for key, value in meta.items():
        if "location" in key:
            location = value
            break

    return {
        "company": _clean_company(company_candidate) if company_candidate else None,
        "role_title": role_title,
        "location": location,
        "source": url,
    }
