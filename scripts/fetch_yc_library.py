#!/usr/bin/env python3
"""Archive selected YC Library series as Markdown.

The YC Library page embeds article metadata, descriptions, and transcripts in
an Inertia data-page payload. The payload is large, so this script only needs
the first several MB, which contains the latest articles sorted newest first.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import socket
import ssl
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE = "https://www.ycombinator.com"
LIBRARY_URL = f"{BASE}/library"
OUT_DIR = Path("yc/library")
SERIES_ALIASES = {
    "Lightcone Podcast": {"lightcone", "lightcone podcast"},
    "How To Build The Future": {"how to build the future"},
    "Hard Tech": {"hard tech"},
}


@dataclass
class Article:
    title: str
    slug: str
    created_at: str
    series_name: str
    author: str
    url: str
    video_url: str
    description: str
    content: str
    transcript: str
    video_chapters: list[Any]


def fetch_prefix(url: str, max_bytes: int = 6_000_000, timeout_seconds: int = 90) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Spielzeit YC Library archiver (+https://github.com/Leahyeah/Spielzeit)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        },
    )
    deadline = time.time() + timeout_seconds
    chunks: list[bytes] = []
    total = 0
    with urllib.request.urlopen(req, timeout=20) as response:
        while total < max_bytes and time.time() < deadline:
            try:
                chunk = response.read(min(65536, max_bytes - total))
            except (TimeoutError, socket.timeout, ssl.SSLError, OSError):
                break
            if not chunk:
                break
            chunks.append(chunk)
            total += len(chunk)
    return b"".join(chunks).decode("utf-8", errors="replace")


def extract_data_page(html_text: str) -> str:
    start_marker = '<div data-page="'
    start = html_text.find(start_marker)
    if start < 0:
        raise RuntimeError("could not find YC data-page payload")
    start += len(start_marker)
    payload = html.unescape(html_text[start:])
    articles_idx = payload.find('"articles":[')
    if articles_idx < 0:
        raise RuntimeError("could not find YC articles payload")
    return payload[articles_idx + len('"articles":[') :]


def parse_articles(payload_tail: str) -> list[dict[str, Any]]:
    # The HTML attribute may include literal control characters inside JSON
    # string values. Escape them before incremental JSON decoding.
    text = payload_tail.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
    decoder = json.JSONDecoder()
    items: list[dict[str, Any]] = []
    pos = 0
    while pos < len(text):
        while pos < len(text) and text[pos] in " \n\r\t,":
            pos += 1
        if pos >= len(text) or text[pos] != "{":
            break
        try:
            obj, end = decoder.raw_decode(text, pos)
        except json.JSONDecodeError:
            break
        items.append(obj)
        pos = end
    return items


def created_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value[:100] or "article"


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    value = html.unescape(value)
    value = value.replace("\\n", "\n")
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def canonical_topic(series_name: str, title: str = "") -> str | None:
    normalized = (series_name or "").strip().lower()
    for topic, aliases in SERIES_ALIASES.items():
        if normalized in aliases:
            return topic
    title_normalized = (title or "").strip().lower()
    if "how to build the future" in title_normalized:
        return "How To Build The Future"
    if "hard tech" in title_normalized:
        return "Hard Tech"
    return None


def article_from_raw(raw: dict[str, Any]) -> Article | None:
    series = raw.get("series_name") or ""
    title = raw.get("title") or ""
    topic = canonical_topic(series, title)
    if not topic:
        return None
    slug = raw.get("slug") or slugify(raw.get("title") or "article")
    url = f"{BASE}/library/{slug}"
    return Article(
        title=raw.get("title") or slug,
        slug=slug,
        created_at=raw.get("created_at") or "",
        series_name=topic,
        author=raw.get("author") or "Y Combinator",
        url=url,
        video_url=raw.get("link") or "",
        description=clean_text(raw.get("description")),
        content=clean_text(raw.get("content")),
        transcript=clean_text(raw.get("transcript")),
        video_chapters=raw.get("video_chapters") or [],
    )


def markdown(article: Article) -> str:
    lines = [
        "---",
        f'title: "{article.title.replace(chr(34), chr(39))}"',
        f"series: {article.series_name}",
        f"created_at: {article.created_at}",
        f"author: {article.author}",
        f"url: {article.url}",
        f"video_url: {article.video_url or '-'}",
        "---",
        "",
        f"# {article.title}",
        "",
        f"- Series: {article.series_name}",
        f"- Created: {article.created_at}",
        f"- Author: {article.author}",
        f"- URL: {article.url}",
    ]
    if article.video_url:
        lines.append(f"- Video: {article.video_url}")
    if article.description:
        lines += ["", "## Description", "", article.description]
    if article.content and article.content != article.description:
        lines += ["", "## Content", "", article.content]
    if article.video_chapters:
        lines += ["", "## Chapters", ""]
        for chapter in article.video_chapters:
            if isinstance(chapter, list) and len(chapter) >= 2:
                lines.append(f"- {chapter[0]}: {chapter[1]}")
    if article.transcript:
        lines += ["", "## Transcript", "", article.transcript]
    return "\n".join(lines).rstrip() + "\n"


def write_index(articles: list[Article], since: datetime) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    by_series: dict[str, list[Article]] = {topic: [] for topic in SERIES_ALIASES}
    for article in articles:
        by_series[article.series_name].append(article)
    lines = [
        "# YC Library Archive",
        "",
        f"Source: {LIBRARY_URL}",
        f"Scope: selected YC Library series since {since.date().isoformat()}",
        "",
    ]
    for topic, items in by_series.items():
        lines += [f"## {topic}", ""]
        if not items:
            lines.append("- No matching items archived.")
        for article in sorted(items, key=lambda item: item.created_at, reverse=True):
            path = f"{slugify(topic)}/{article.created_at[:10]}-{slugify(article.title)}.md"
            lines.append(f"- {article.created_at[:10]} [{article.title}]({path})")
        lines.append("")
    (OUT_DIR / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="2024-05-11", help="Archive items created on/after YYYY-MM-DD.")
    args = parser.parse_args()

    since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc)
    html_text = fetch_prefix(LIBRARY_URL)
    raw_articles = parse_articles(extract_data_page(html_text))
    articles: list[Article] = []
    for raw in raw_articles:
        article = article_from_raw(raw)
        if not article or not article.created_at:
            continue
        if created_datetime(article.created_at) < since:
            continue
        articles.append(article)

    for topic in SERIES_ALIASES:
        (OUT_DIR / slugify(topic)).mkdir(parents=True, exist_ok=True)

    for article in articles:
        filename = f"{article.created_at[:10]}-{slugify(article.title)}.md"
        path = OUT_DIR / slugify(article.series_name) / filename
        path.write_text(markdown(article), encoding="utf-8")
    write_index(articles, since)

    print(f"Archived {len(articles)} YC Library items into {OUT_DIR}")
    for topic in SERIES_ALIASES:
        print(f"{topic}: {sum(1 for item in articles if item.series_name == topic)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
