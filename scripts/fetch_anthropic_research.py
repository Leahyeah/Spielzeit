#!/usr/bin/env python3
"""Archive Anthropic research pages from sitemap.xml as Markdown."""

from __future__ import annotations

import html
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path


BASE = "https://www.anthropic.com"
SITEMAP = f"{BASE}/sitemap.xml"
OUT_DIR = Path("anthropic/research")


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Spielzeit research archiver (+https://github.com/Leahyeah/Spielzeit)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    last_error: Exception | None = None
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as exc:  # transient TLS/network errors are common on large archive runs
            last_error = exc
            time.sleep(1 + attempt)
    raise last_error or RuntimeError(f"failed to fetch {url}")


def clean_text(value: str) -> str:
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def strip_tags(value: str) -> str:
    value = re.sub(r"<script\b.*?</script>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<style\b.*?</style>", " ", value, flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    return clean_text(value)


def slug_from_url(url: str) -> str:
    return url.rstrip("/").split("/")[-1]


def extract_between(source: str, tag: str) -> str:
    start = source.find(f"<{tag}")
    if start < 0:
        return ""
    depth = 0
    pos = start
    open_re = re.compile(rf"<{tag}\b[^>]*>|</{tag}>", re.I)
    for match in open_re.finditer(source, start):
        token = match.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return source[start : match.end()]
        else:
            depth += 1
        pos = match.end()
    return source[start:pos]


def first_match(pattern: str, source: str) -> str:
    match = re.search(pattern, source, flags=re.I | re.S)
    return clean_text(match.group(1)) if match else ""


def extract_meta(source: str, attr: str, value: str) -> str:
    patterns = [
        rf'<meta[^>]+{attr}=["\']{re.escape(value)}["\'][^>]+content=["\']([^"\']*)["\']',
        rf'<meta[^>]+content=["\']([^"\']*)["\'][^>]+{attr}=["\']{re.escape(value)}["\']',
    ]
    for pattern in patterns:
        found = first_match(pattern, source)
        if found:
            return found
    return ""


class MarkdownHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []
        self.href_stack: list[str | None] = []
        self.skip_depth = 0
        self.list_stack: list[str] = []
        self.in_heading: int | None = None

    def emit(self, text: str) -> None:
        if self.skip_depth:
            return
        self.parts.append(text)

    def newline(self, count: int = 1) -> None:
        self.emit("\n" * count)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        if tag in {"script", "style", "svg", "video", "picture", "noscript", "template", "button", "form"}:
            self.skip_depth += 1
            return
        if tag in {"h1", "h2", "h3", "h4"}:
            self.in_heading = int(tag[1])
            self.newline(2)
            self.emit("#" * self.in_heading + " ")
        elif tag == "p":
            self.newline(2)
        elif tag == "br":
            self.newline()
        elif tag in {"ul", "ol"}:
            self.list_stack.append(tag)
            self.newline()
        elif tag == "li":
            self.newline()
            marker = "1. " if self.list_stack and self.list_stack[-1] == "ol" else "- "
            self.emit(marker)
        elif tag == "blockquote":
            self.newline(2)
            self.emit("> ")
        elif tag == "pre":
            self.newline(2)
            self.emit("```\n")
        elif tag == "code":
            self.emit("`")
        elif tag == "a":
            if self.parts and not self.parts[-1].endswith(("\n", " ", "(", "[", "`", "*")):
                self.emit(" ")
            self.href_stack.append(attrs_dict.get("href"))
            self.emit("[")
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("*")

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "svg", "video", "picture", "noscript", "template", "button", "form"}:
            if self.skip_depth:
                self.skip_depth -= 1
            return
        if self.skip_depth:
            return
        if tag in {"h1", "h2", "h3", "h4"}:
            self.in_heading = None
            self.newline(2)
        elif tag in {"p", "blockquote"}:
            self.newline(2)
        elif tag in {"ul", "ol"}:
            if self.list_stack:
                self.list_stack.pop()
            self.newline()
        elif tag == "pre":
            self.emit("\n```")
            self.newline(2)
        elif tag == "code":
            self.emit("`")
        elif tag == "a":
            href = self.href_stack.pop() if self.href_stack else None
            if href:
                if href.startswith("/"):
                    href = BASE + href
                self.emit(f"]({href})")
            else:
                self.emit("]")
        elif tag in {"strong", "b"}:
            self.emit("**")
        elif tag in {"em", "i"}:
            self.emit("*")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        text = clean_text(data)
        if not text:
            return
        if self.parts and not self.parts[-1].endswith(("\n", " ", "[", "(", "`", "*")):
            self.emit(" ")
        self.emit(text)

    def markdown(self) -> str:
        text = "".join(self.parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"\[\s+", "[", text)
        text = re.sub(r"\s+\]", "]", text)
        return text.strip()


@dataclass
class Page:
    url: str
    slug: str
    title: str
    date: str
    category: str
    description: str
    external_links: list[str]
    markdown: str


def date_key(date: str) -> datetime:
    for fmt in ("%b %d, %Y", "%B %d, %Y"):
        try:
            return datetime.strptime(date, fmt)
        except ValueError:
            pass
    return datetime.min


def parse_page(url: str, source: str) -> Page:
    article = extract_between(source, "article") or extract_between(source, "main") or source
    title = strip_tags(first_match(r"<h1\b[^>]*>(.*?)</h1>", article))
    if not title:
        title = extract_meta(source, "property", "og:title") or first_match(r"<title[^>]*>(.*?)</title>", source)
    if title.endswith(" \\ Anthropic"):
        title = title[: -len(" \\ Anthropic")]
    description = extract_meta(source, "name", "description") or extract_meta(source, "property", "og:description")
    category = strip_tags(first_match(r'<div[^>]+subjects[^>]*>(.*?)</div>', article))
    date = strip_tags(first_match(r'<div[^>]+agate[^>]*>(.*?)</div>', article))
    if not date:
        date = strip_tags(first_match(r"<time\b[^>]*>(.*?)</time>", article))
    external_links = []
    for href in re.findall(r'<a\b[^>]+href=["\']([^"\']+)["\']', article, flags=re.I):
        if href.startswith("http") and "anthropic.com" not in href and href not in external_links:
            external_links.append(href)
    body = article
    body = re.sub(r"<header\b.*?</header>", "", body, flags=re.I | re.S)
    parser = MarkdownHTMLParser()
    parser.feed(body)
    markdown = parser.markdown()
    return Page(
        url=url,
        slug=slug_from_url(url),
        title=title or slug_from_url(url),
        date=date,
        category=category,
        description=description,
        external_links=external_links,
        markdown=markdown,
    )


def page_markdown(page: Page) -> str:
    lines = [
        "---",
        f'title: "{page.title.replace(chr(34), chr(39))}"',
        f"url: {page.url}",
    ]
    if page.date:
        lines.append(f'date: "{page.date}"')
    if page.category:
        lines.append(f'category: "{page.category.replace(chr(34), chr(39))}"')
    if page.description:
        lines.append(f'description: "{page.description.replace(chr(34), chr(39))}"')
    lines.extend(["source: Anthropic Research", "---", ""])
    lines.append(f"# {page.title}")
    lines.append("")
    if page.date or page.category:
        meta = " | ".join(x for x in [page.category, page.date] if x)
        lines.append(meta)
        lines.append("")
    if page.description:
        lines.append(f"> {page.description}")
        lines.append("")
    if page.external_links:
        lines.append("## External Links")
        lines.append("")
        for link in page.external_links:
            lines.append(f"- {link}")
        lines.append("")
    body = page.markdown
    body = re.sub(rf"^#\s+{re.escape(page.title)}\s*", "", body).strip()
    if body:
        lines.append("## Archived Content")
        lines.append("")
        lines.append(body)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sitemap = fetch(SITEMAP)
    urls = re.findall(r"<loc>(https://www\.anthropic\.com/research/[^<]+)</loc>", sitemap)
    urls = sorted(set(u for u in urls if "/research/team/" not in u))
    pages: list[Page] = []
    failures: list[tuple[str, str]] = []
    for index, url in enumerate(urls, 1):
        try:
            source = fetch(url)
            page = parse_page(url, source)
            pages.append(page)
            path = OUT_DIR / f"{page.slug}.md"
            path.write_text(page_markdown(page), encoding="utf-8")
            print(f"[{index:03d}/{len(urls)}] {page.slug}")
            time.sleep(0.15)
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            failures.append((url, str(exc)))
            print(f"[fail] {url}: {exc}", file=sys.stderr)
    index_lines = [
        "# Anthropic Research Archive",
        "",
        f"Source: {BASE}/research and {SITEMAP}",
        f"Last updated: {time.strftime('%Y-%m-%d')}",
        f"Archived pages: {len(pages)}",
        "",
        "This archive stores Anthropic public research pages as Markdown for reading and follow-up summaries.",
        "",
        "## Publications",
        "",
    ]
    for page in sorted(pages, key=lambda p: (date_key(p.date), p.title), reverse=True):
        meta = " | ".join(x for x in [page.category, page.date] if x)
        suffix = f" - {meta}" if meta else ""
        index_lines.append(f"- [{page.title}](research/{page.slug}.md){suffix}")
    if failures:
        index_lines.extend(["", "## Fetch Failures", ""])
        for url, error in failures:
            index_lines.append(f"- {url}: {error}")
    (OUT_DIR.parent / "README.md").write_text("\n".join(index_lines).rstrip() + "\n", encoding="utf-8")
    print(f"Archived {len(pages)} pages into {OUT_DIR}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
