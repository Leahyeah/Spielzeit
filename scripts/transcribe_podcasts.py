#!/usr/bin/env python3
"""Download podcast audio temporarily and write transcripts into episode Markdown.

Audio files are cached under .cache/ and are not committed. Transcripts are
committed into the existing episode Markdown files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


CACHE = Path(".cache/podcast-audio")
TRANSCRIPT_MARKER = "## Transcript"
OPENAI_TRANSCRIPT_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini-transcribe"


@dataclass
class EpisodeFile:
    path: Path
    title: str
    show: str
    category: str
    published: datetime | None
    audio_url: str
    has_transcript: bool


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    return values


def parse_date(value: str) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def iter_episodes(root: Path, since: datetime | None) -> list[EpisodeFile]:
    episodes: list[EpisodeFile] = []
    for path in sorted((root / "podcasts").glob("*/*/episodes/*.md")):
        raw = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(path)
        published = parse_date(fm.get("published", ""))
        if since and (not published or published < since):
            continue
        audio_url = fm.get("audio_url", "")
        if not audio_url or audio_url == "-":
            continue
        episodes.append(
            EpisodeFile(
                path=path,
                title=fm.get("title", path.stem),
                show=fm.get("show", ""),
                category=fm.get("category", ""),
                published=published,
                audio_url=audio_url,
                has_transcript=TRANSCRIPT_MARKER in raw,
            )
        )
    return episodes


def safe_name(episode: EpisodeFile) -> str:
    base = re.sub(r"[^a-zA-Z0-9._-]+", "-", f"{episode.path.parent.parent.name}-{episode.path.stem}")
    return base[:160]


def download_audio(episode: EpisodeFile) -> Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    suffix = Path(episode.audio_url.split("?", 1)[0]).suffix or ".audio"
    dest = CACHE / f"{safe_name(episode)}{suffix}"
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    req = urllib.request.Request(episode.audio_url, headers={"User-Agent": "Spielzeit transcript fetcher"})
    with urllib.request.urlopen(req, timeout=120) as response:
        dest.write_bytes(response.read())
    return dest


def run_json(command: list[str]) -> dict:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def transcribe_with_openai(audio: Path, model: str, language: str) -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    command = [
        "curl",
        "-sS",
        OPENAI_TRANSCRIPT_URL,
        "-H",
        f"Authorization: Bearer {api_key}",
        "-H",
        "Content-Type: multipart/form-data",
        "-F",
        f"file=@{audio}",
        "-F",
        f"model={model}",
        "-F",
        "response_format=json",
    ]
    if language:
        command += ["-F", f"language={language}"]
    payload = run_json(command)
    if "text" not in payload:
        raise RuntimeError(f"OpenAI transcription response missing text: {payload}")
    return payload["text"].strip()


def transcribe_with_command(audio: Path, template: str) -> str:
    # The command must print transcript text to stdout. Use {audio} as placeholder.
    command = [part.format(audio=str(audio)) for part in template.split()]
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def insert_transcript(path: Path, transcript: str, engine: str) -> None:
    text = path.read_text(encoding="utf-8")
    if TRANSCRIPT_MARKER in text:
        return
    block = f"\n{TRANSCRIPT_MARKER}\n\n_Source: audio transcription via {engine}._\n\n{transcript.strip()}\n"
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="2025-01-01", help="Only transcribe episodes published on/after YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum episodes to transcribe in this run.")
    parser.add_argument("--show", help="Only transcribe one show slug.")
    parser.add_argument("--category", help="Only transcribe one category.")
    parser.add_argument("--include-existing", action="store_true", help="Reprocess files even if they already contain a transcript.")
    parser.add_argument("--engine", choices=["openai", "command"], default="openai")
    parser.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL)
    parser.add_argument("--language", default="zh")
    parser.add_argument("--command", help="Command template for --engine command; must print transcript to stdout and use {audio}.")
    args = parser.parse_args()

    since = datetime.fromisoformat(args.since).replace(tzinfo=timezone.utc) if args.since else None
    episodes = iter_episodes(Path.cwd(), since)
    if args.show:
        episodes = [e for e in episodes if e.path.parent.parent.name == args.show]
    if args.category:
        episodes = [e for e in episodes if e.category == args.category]
    if not args.include_existing:
        episodes = [e for e in episodes if not e.has_transcript]
    episodes.sort(key=lambda e: e.published or datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    if args.limit > 0:
        episodes = episodes[: args.limit]
    if not episodes:
        print("No matching episodes to transcribe.")
        return 0
    if args.engine == "command" and not args.command:
        raise SystemExit("--command is required when --engine command")

    for index, episode in enumerate(episodes, 1):
        print(f"[{index}/{len(episodes)}] {episode.category}/{episode.show}: {episode.title}", flush=True)
        audio = download_audio(episode)
        if args.engine == "openai":
            transcript = transcribe_with_openai(audio, args.openai_model, args.language)
            engine = f"OpenAI {args.openai_model}"
        else:
            transcript = transcribe_with_command(audio, args.command or "")
            engine = args.command or "command"
        insert_transcript(episode.path, transcript, engine)
        print(f"  wrote transcript to {episode.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
