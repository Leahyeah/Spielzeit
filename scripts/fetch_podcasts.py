#!/usr/bin/env python3
"""Archive configured podcast RSS metadata and text fields as Markdown."""

from __future__ import annotations

import argparse
import gzip
import hashlib
import html
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


ROOT = Path("podcasts")
CONFIG = ROOT / "feeds.json"
USER_AGENT = "Spielzeit podcast archiver (+https://github.com/Leahyeah/Spielzeit)"


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


def clean_text(value: str | None) -> str:
    if not value:
        return ""
    parser = TextExtractor()
    parser.feed(html.unescape(value))
    return re.sub(r"\s+", " ", "".join(parser.parts)).strip()


def slugify(value: str, fallback: str = "episode") -> str:
    value = value.strip().lower()
    value = re.sub(r"https?://", "", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value[:90] or fallback


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=45) as response:
        data = response.read()
    if data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
    return data


def discover_feed(url: str, data: bytes) -> tuple[str, bytes]:
    head = data[:300].lower()
    if b"<rss" in head or b"<feed" in head or b"<?xml" in head:
        return url, data
    text = data.decode("utf-8", errors="replace")
    candidates = re.findall(
        r'<link[^>]+(?:type=["\']application/(?:rss|atom)\+xml["\'][^>]+href=["\']([^"\']+)["\']|href=["\']([^"\']+)["\'][^>]+type=["\']application/(?:rss|atom)\+xml["\'])',
        text,
        flags=re.I,
    )
    hrefs = [a or b for a, b in candidates]
    if not hrefs:
        for guess in (url.rstrip("/") + "/rss", url.rstrip("/") + ".rss"):
            try:
                guessed = fetch(guess)
                return guess, guessed
            except Exception:
                pass
        raise ValueError(f"could not discover RSS feed from {url}")
    href = hrefs[0]
    if href.startswith("/"):
        base = re.match(r"^(https?://[^/]+)", url)
        href = (base.group(1) if base else "") + href
    elif not href.startswith("http"):
        href = url.rstrip("/") + "/" + href
    return href, fetch(href)


def child(element: ET.Element, local_name: str) -> ET.Element | None:
    for candidate in list(element):
        if candidate.tag.split("}")[-1] == local_name:
            return candidate
    return None


def child_text(element: ET.Element, local_name: str) -> str:
    item = child(element, local_name)
    return "".join(item.itertext()).strip() if item is not None else ""


def attr_child(element: ET.Element, local_name: str, attr: str) -> str:
    item = child(element, local_name)
    return item.attrib.get(attr, "") if item is not None else ""


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except Exception:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iso_date(dt: datetime | None) -> str:
    return dt.date().isoformat() if dt else "unknown-date"


@dataclass
class Episode:
    title: str
    published: datetime | None
    link: str
    guid: str
    description: str
    duration: str
    audio_url: str


@dataclass
class Show:
    title: str
    description: str
    feed_url: str
    resolved_feed_url: str
    site_url: str
    episodes: list[Episode]


def parse_feed(url: str, data: bytes) -> Show:
    root = ET.fromstring(data)
    channel = root.find("channel") if root.tag.endswith("rss") else root
    if channel is None:
        channel = root
    title = clean_text(child_text(channel, "title"))
    description = clean_text(child_text(channel, "description") or child_text(channel, "subtitle"))
    site_url = child_text(channel, "link")
    items = channel.findall("item") or root.findall(".//{*}entry")
    episodes: list[Episode] = []
    for item in items:
        item_title = clean_text(child_text(item, "title")) or "Untitled"
        published = parse_date(child_text(item, "pubDate") or child_text(item, "published") or child_text(item, "updated"))
        link = child_text(item, "link")
        if not link:
            link_node = child(item, "link")
            if link_node is not None:
                link = link_node.attrib.get("href", "")
        guid = child_text(item, "guid") or link or item_title
        desc = clean_text(child_text(item, "description") or child_text(item, "summary") or child_text(item, "encoded"))
        enclosure = child(item, "enclosure")
        audio_url = enclosure.attrib.get("url", "") if enclosure is not None else ""
        duration = child_text(item, "duration")
        episodes.append(Episode(item_title, published, link, guid, desc, duration, audio_url))
    episodes.sort(key=lambda item: item.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return Show(title=title, description=description, feed_url=url, resolved_feed_url=url, site_url=site_url, episodes=episodes)


def episode_filename(episode: Episode) -> str:
    date = iso_date(episode.published)
    digest = hashlib.sha1((episode.guid or episode.link or episode.title).encode("utf-8")).hexdigest()[:8]
    return f"{date}-{slugify(episode.title)}-{digest}.md"


def md_escape(value: str) -> str:
    return value.replace('"', "'")


def write_show(entry: dict[str, Any], show: Show) -> list[Path]:
    category = entry["category"]
    slug = entry["slug"]
    show_dir = ROOT / category / slug
    episode_dir = show_dir / "episodes"
    episode_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    readme_lines = [
        "---",
        f'title: "{md_escape(show.title)}"',
        f"category: {category}",
        f"feed: {entry['url']}",
        f"resolved_feed: {show.resolved_feed_url}",
        f'tags: "{", ".join(entry.get("tags", []))}"',
        "---",
        "",
        f"# {show.title}",
        "",
        f"- Category: {category}",
        f"- Tags: {', '.join(entry.get('tags', [])) or '-'}",
        f"- Feed: {entry['url']}",
        f"- Resolved feed: {show.resolved_feed_url}",
        f"- Episodes archived: {len(show.episodes)}",
        "",
        show.description,
        "",
        "## Latest Episodes",
        "",
    ]
    for episode in show.episodes[:20]:
        path = Path("episodes") / episode_filename(episode)
        readme_lines.append(f"- {iso_date(episode.published)} [{episode.title}]({path.as_posix()})")
    show_readme = show_dir / "README.md"
    show_readme.write_text("\n".join(readme_lines).rstrip() + "\n", encoding="utf-8")
    written.append(show_readme)
    for episode in show.episodes:
        path = episode_dir / episode_filename(episode)
        if path.exists():
            # Preserve richer episode files, especially audio transcripts added
            # after the RSS-only archive was created.
            written.append(path)
            continue
        lines = [
            "---",
            f'title: "{md_escape(episode.title)}"',
            f"show: \"{md_escape(show.title)}\"",
            f"category: {category}",
            f"published: {episode.published.isoformat() if episode.published else ''}",
            f"link: {episode.link}",
            f"audio_url: {episode.audio_url}",
            f"guid: \"{md_escape(episode.guid)}\"",
            "---",
            "",
            f"# {episode.title}",
            "",
            f"- Show: {show.title}",
            f"- Category: {category}",
            f"- Published: {episode.published.isoformat() if episode.published else 'unknown'}",
            f"- Link: {episode.link or '-'}",
            f"- Audio: {episode.audio_url or '-'}",
            f"- Duration: {episode.duration or '-'}",
            "",
            "## Text",
            "",
            episode.description or "(No description text in feed.)",
            "",
        ]
        path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
        written.append(path)
    return written


def write_indexes(config: dict[str, Any], shows: list[tuple[dict[str, Any], Show]]) -> None:
    latest_by_category: dict[str, list[tuple[dict[str, Any], Show, Episode]]] = defaultdict(list)
    for entry, show in shows:
        for episode in show.episodes:
            latest_by_category[entry["category"]].append((entry, show, episode))
    for items in latest_by_category.values():
        items.sort(key=lambda row: row[2].published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    lines = [
        "# Podcast Archive",
        "",
        f"Last updated: {datetime.now(timezone.utc).date().isoformat()}",
        "",
        "This archive stores podcast RSS metadata and text fields only. Audio files are linked but not stored.",
        "",
        "## Categories",
        "",
    ]
    for category in config["categories"]:
        lines.append(f"### {category}")
        lines.append("")
        for entry, show in sorted((row for row in shows if row[0]["category"] == category), key=lambda row: row[1].title):
            lines.append(f"- [{show.title}]({category}/{entry['slug']}/README.md): {entry.get('notes', '')}")
        lines.append("")
    lines.append("## Latest Episodes By Category")
    lines.append("")
    for category in config["categories"]:
        lines.append(f"### {category}")
        lines.append("")
        for entry, show, episode in latest_by_category.get(category, [])[:10]:
            rel = Path(category) / entry["slug"] / "episodes" / episode_filename(episode)
            lines.append(f"- {iso_date(episode.published)} [{show.title}]({rel.as_posix()}): [{episode.title}]({rel.as_posix()})")
        lines.append("")
    (ROOT / "README.md").write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_weekly(config: dict[str, Any], shows: list[tuple[dict[str, Any], Show]], days: int) -> Path:
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    weekly_dir = ROOT / "weekly"
    weekly_dir.mkdir(parents=True, exist_ok=True)
    path = weekly_dir / f"{datetime.now(timezone.utc).date().isoformat()}.md"
    by_category: dict[str, list[tuple[dict[str, Any], Show, Episode]]] = defaultdict(list)
    for entry, show in shows:
        for episode in show.episodes:
            if episode.published and episode.published >= cutoff:
                by_category[entry["category"]].append((entry, show, episode))
    for rows in by_category.values():
        rows.sort(key=lambda row: row[2].published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    lines = [
        f"# Podcast Weekly Update - {datetime.now(timezone.utc).date().isoformat()}",
        "",
        f"Window: last {days} days",
        "",
        "Anthropic research updates are maintained separately under `anthropic/`.",
        "",
    ]
    for category in config["categories"]:
        lines.append(f"## {category}")
        lines.append("")
        rows = by_category.get(category, [])
        if not rows:
            lines.append("- No new episodes in this window.")
            lines.append("")
            continue
        for entry, show, episode in rows:
            rel = Path("..") / category / entry["slug"] / "episodes" / episode_filename(episode)
            summary = episode.description[:180] + ("..." if len(episode.description) > 180 else "")
            lines.append(f"- {iso_date(episode.published)} [{show.title}]({rel.as_posix()}): [{episode.title}]({rel.as_posix()})")
            if summary:
                lines.append(f"  - {summary}")
        lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--weekly-days", type=int, default=14, help="Window for generated weekly update.")
    args = parser.parse_args()
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    shows: list[tuple[dict[str, Any], Show]] = []
    failures: list[str] = []
    for entry in config["feeds"]:
        try:
            initial = fetch(entry["url"])
            resolved_url, data = discover_feed(entry["url"], initial)
            show = parse_feed(resolved_url, data)
            show.resolved_feed_url = resolved_url
            shows.append((entry, show))
            write_show(entry, show)
            print(f"{entry['slug']}: {show.title} ({len(show.episodes)} episodes)")
        except (ET.ParseError, urllib.error.URLError, OSError, ValueError) as exc:
            failures.append(f"{entry['url']}: {exc}")
            print(f"FAIL {entry['url']}: {exc}", file=sys.stderr)
    write_indexes(config, shows)
    weekly = write_weekly(config, shows, args.weekly_days)
    print(f"Generated {ROOT / 'README.md'} and {weekly}")
    if failures:
        print("Failures:", file=sys.stderr)
        for failure in failures:
            print(f"- {failure}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
