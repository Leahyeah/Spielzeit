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
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


CACHE = Path(".cache/podcast-audio")
TRANSCRIPT_MARKER = "## Transcript"
OPENAI_TRANSCRIPT_URL = "https://api.openai.com/v1/audio/transcriptions"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini-transcribe"
DEFAULT_ALIYUN_REGION = "cn-beijing"
DEFAULT_ALIYUN_ENDPOINT = "tingwu.cn-beijing.aliyuncs.com"
DEFAULT_ALIYUN_OSS_ENDPOINT = "oss-cn-beijing.aliyuncs.com"


def load_dotenv(path: Path = Path(".env")) -> None:
    """Load simple KEY=VALUE lines without overriding existing env vars."""
    if not path.exists():
        return
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            raise RuntimeError(f"Invalid .env line {line_number}: expected KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if not key:
            raise RuntimeError(f"Invalid .env line {line_number}: empty key")
        os.environ.setdefault(key, value)


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


def aliyun_client():
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    if not access_key_id or not access_key_secret:
        raise RuntimeError("ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required")
    try:
        from alibabacloud_tea_openapi import models as open_api_models
        from alibabacloud_tingwu20230930.client import Client as TingwuClient
    except ImportError as exc:
        raise RuntimeError(
            "Aliyun Tingwu SDK is not installed. Run: python3 -m pip install -r requirements-transcription.txt"
        ) from exc

    config = open_api_models.Config(
        access_key_id=access_key_id,
        access_key_secret=access_key_secret,
        region_id=os.environ.get("ALIBABA_CLOUD_REGION_ID", DEFAULT_ALIYUN_REGION),
    )
    config.endpoint = os.environ.get("ALIYUN_TINGWU_ENDPOINT", DEFAULT_ALIYUN_ENDPOINT)
    return TingwuClient(config)


def response_body_to_map(response) -> dict:
    body = getattr(response, "body", response)
    if hasattr(body, "to_map"):
        return body.to_map()
    if isinstance(body, dict):
        return body
    raise RuntimeError(f"Unsupported Aliyun response type: {type(response)!r}")


def normalize_aliyun_code(value) -> str:
    return "" if value is None else str(value)


def start_aliyun_task(
    client,
    episode: EpisodeFile,
    source_language: str,
    app_key: str | None,
    file_url: str | None = None,
    task_key: str | None = None,
) -> str:
    from alibabacloud_tingwu20230930 import models as tingwu_models

    request = tingwu_models.CreateTaskRequest(
        type="offline",
        app_key=app_key or None,
        input=tingwu_models.CreateTaskRequestInput(
            source_language=source_language,
            file_url=file_url or episode.audio_url,
            task_key=task_key or safe_name(episode),
        ),
        parameters=tingwu_models.CreateTaskRequestParameters(
            transcription=tingwu_models.CreateTaskRequestParametersTranscription(
                diarization_enabled=True,
                output_level=2,
            ),
            auto_chapters_enabled=False,
            meeting_assistance_enabled=False,
            summarization_enabled=False,
            text_polish_enabled=False,
        ),
    )
    payload = response_body_to_map(client.create_task(request))
    if normalize_aliyun_code(payload.get("Code")) not in {"0", ""}:
        raise RuntimeError(f"Aliyun CreateTask failed: {payload}")
    task_id = (payload.get("Data") or {}).get("TaskId")
    if not task_id:
        raise RuntimeError(f"Aliyun CreateTask response missing TaskId: {payload}")
    return task_id


def wait_aliyun_task(client, task_id: str, poll_seconds: int, timeout_minutes: int) -> dict:
    deadline = time.time() + timeout_minutes * 60
    transient_errors = 0
    while True:
        try:
            payload = response_body_to_map(client.get_task_info(task_id))
            transient_errors = 0
        except Exception as exc:
            transient_errors += 1
            if transient_errors > 5 or time.time() >= deadline:
                raise
            print(f"  Aliyun task {task_id} poll error: {exc}; retrying in {poll_seconds}s", flush=True)
            time.sleep(poll_seconds)
            continue
        if normalize_aliyun_code(payload.get("Code")) not in {"0", ""}:
            raise RuntimeError(f"Aliyun GetTaskInfo failed: {payload}")
        data = payload.get("Data") or {}
        status = data.get("TaskStatus")
        if status == "COMPLETED":
            return data
        if status in {"FAILED", "INVALID"}:
            raise RuntimeError(f"Aliyun task {task_id} ended with {status}: {data}")
        if time.time() >= deadline:
            raise RuntimeError(f"Aliyun task {task_id} timed out after {timeout_minutes} minutes")
        print(f"  Aliyun task {task_id} status={status}; polling again in {poll_seconds}s", flush=True)
        time.sleep(poll_seconds)


def fetch_json_url(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "Spielzeit transcript fetcher"})
    with urllib.request.urlopen(req, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def transcript_from_aliyun_json(payload: dict) -> str:
    transcription = payload.get("Transcription") or payload.get("transcription") or payload
    paragraphs = transcription.get("Paragraphs") or transcription.get("paragraphs") or []
    lines: list[str] = []
    for paragraph in paragraphs:
        words = paragraph.get("Words") or paragraph.get("words") or []
        if not words:
            continue
        speaker = paragraph.get("SpeakerId") or paragraph.get("speakerId") or paragraph.get("Speaker")
        sentence_parts: list[str] = []
        current_sentence = object()
        for word in words:
            sentence_id = word.get("SentenceId") or word.get("sentenceId")
            if sentence_id != current_sentence and sentence_parts:
                prefix = f"Speaker {speaker}: " if speaker else ""
                lines.append(prefix + "".join(sentence_parts).strip())
                sentence_parts = []
            current_sentence = sentence_id
            sentence_parts.append(str(word.get("Text") or word.get("text") or ""))
        if sentence_parts:
            prefix = f"Speaker {speaker}: " if speaker else ""
            lines.append(prefix + "".join(sentence_parts).strip())
    text = "\n".join(line for line in lines if line)
    if text:
        return text
    return collect_text_fields(transcription).strip()


def collect_text_fields(value) -> str:
    if isinstance(value, dict):
        parts = []
        for key, child in value.items():
            if key.lower() in {"text", "content", "sentence"} and isinstance(child, str):
                parts.append(child)
            else:
                nested = collect_text_fields(child)
                if nested:
                    parts.append(nested)
        return "\n".join(parts)
    if isinstance(value, list):
        return "\n".join(part for item in value if (part := collect_text_fields(item)))
    return ""


def transcribe_with_aliyun_tingwu(
    episode: EpisodeFile,
    source_language: str,
    poll_seconds: int,
    timeout_minutes: int,
) -> str:
    client = aliyun_client()
    task_id = start_aliyun_task(client, episode, source_language, os.environ.get("ALIYUN_TINGWU_APP_KEY"))
    print(f"  Aliyun task id: {task_id}", flush=True)
    data = wait_aliyun_task(client, task_id, poll_seconds, timeout_minutes)
    result = data.get("Result") or {}
    transcription_url = result.get("Transcription")
    if not transcription_url:
        raise RuntimeError(f"Aliyun task {task_id} completed but has no transcription URL: {data}")
    transcript_payload = fetch_json_url(transcription_url)
    transcript = transcript_from_aliyun_json(transcript_payload)
    if not transcript:
        raise RuntimeError(f"Aliyun transcription URL returned no recognizable text for task {task_id}")
    return transcript


def split_audio_for_aliyun(audio: Path, episode: EpisodeFile, chunk_minutes: int) -> list[Path]:
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("ffmpeg is required for --aliyun-split-minutes but was not found in PATH")
    chunk_dir = CACHE / "chunks" / safe_name(episode)
    if chunk_dir.exists():
        for old in chunk_dir.glob("*"):
            old.unlink()
    chunk_dir.mkdir(parents=True, exist_ok=True)
    suffix = audio.suffix if audio.suffix else ".m4a"
    output_pattern = chunk_dir / f"chunk-%03d{suffix}"
    command = [
        ffmpeg,
        "-hide_banner",
        "-loglevel",
        "error",
        "-i",
        str(audio),
        "-f",
        "segment",
        "-segment_time",
        str(chunk_minutes * 60),
        "-reset_timestamps",
        "1",
        "-c",
        "copy",
        str(output_pattern),
    ]
    subprocess.run(command, check=True)
    chunks = sorted(chunk_dir.glob(f"chunk-*{suffix}"))
    if not chunks:
        raise RuntimeError("ffmpeg completed but produced no audio chunks")
    return chunks


def aliyun_oss_bucket():
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    bucket_name = os.environ.get("ALIYUN_OSS_BUCKET")
    if not access_key_id or not access_key_secret or not bucket_name:
        raise RuntimeError(
            "ALIYUN_OSS_BUCKET plus ALIBABA_CLOUD_ACCESS_KEY_ID/SECRET are required for chunked Aliyun transcription"
        )
    try:
        import oss2
    except ImportError as exc:
        raise RuntimeError("oss2 is not installed. Run: python3 -m pip install -r requirements-transcription.txt") from exc
    endpoint = os.environ.get("ALIYUN_OSS_ENDPOINT", DEFAULT_ALIYUN_OSS_ENDPOINT)
    auth = oss2.Auth(access_key_id, access_key_secret)
    return oss2.Bucket(auth, endpoint, bucket_name)


def upload_chunks_to_oss(chunks: list[Path], episode: EpisodeFile) -> list[tuple[str, str]]:
    bucket = aliyun_oss_bucket()
    prefix = os.environ.get("ALIYUN_OSS_PREFIX", "podcast-transcription-temp").strip("/")
    expires = int(os.environ.get("ALIYUN_OSS_SIGNED_URL_EXPIRES", "86400"))
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    uploaded: list[tuple[str, str]] = []
    for index, chunk in enumerate(chunks, 1):
        key = f"{prefix}/{safe_name(episode)}/{stamp}/chunk-{index:03d}{chunk.suffix}"
        bucket.put_object_from_file(key, str(chunk))
        signed_url = bucket.sign_url("GET", key, expires, slash_safe=True)
        uploaded.append((key, signed_url))
    return uploaded


def delete_oss_objects(keys: list[str]) -> None:
    if not keys:
        return
    try:
        bucket = aliyun_oss_bucket()
        for key in keys:
            bucket.delete_object(key)
    except Exception as exc:
        print(f"  warning: failed to delete temporary OSS chunks: {exc}", file=sys.stderr, flush=True)


def transcribe_with_aliyun_tingwu_chunks(
    episode: EpisodeFile,
    source_language: str,
    poll_seconds: int,
    timeout_minutes: int,
    chunk_minutes: int,
) -> str:
    audio = download_audio(episode)
    chunks = split_audio_for_aliyun(audio, episode, chunk_minutes)
    print(f"  split into {len(chunks)} chunks", flush=True)
    uploaded = upload_chunks_to_oss(chunks, episode)
    uploaded_keys = [key for key, _ in uploaded]
    client = aliyun_client()
    transcripts: list[str] = []
    try:
        for index, (_, signed_url) in enumerate(uploaded, 1):
            task_key = f"{safe_name(episode)}-chunk-{index:03d}"
            task_id = start_aliyun_task(
                client,
                episode,
                source_language,
                os.environ.get("ALIYUN_TINGWU_APP_KEY"),
                file_url=signed_url,
                task_key=task_key,
            )
            print(f"  Aliyun chunk {index}/{len(uploaded)} task id: {task_id}", flush=True)
            data = wait_aliyun_task(client, task_id, poll_seconds, timeout_minutes)
            result = data.get("Result") or {}
            transcription_url = result.get("Transcription")
            if not transcription_url:
                raise RuntimeError(f"Aliyun chunk task {task_id} completed but has no transcription URL: {data}")
            transcript = transcript_from_aliyun_json(fetch_json_url(transcription_url))
            if not transcript:
                raise RuntimeError(f"Aliyun chunk task {task_id} returned no recognizable text")
            transcripts.append(f"[Part {index}/{len(uploaded)}]\n{transcript}")
    finally:
        delete_oss_objects(uploaded_keys)
    return "\n\n".join(transcripts)


def transcribe_with_aliyun_tingwu_oss_url(
    episode: EpisodeFile,
    source_language: str,
    poll_seconds: int,
    timeout_minutes: int,
) -> str:
    audio = download_audio(episode)
    uploaded = upload_chunks_to_oss([audio], episode)
    uploaded_key, signed_url = uploaded[0]
    client = aliyun_client()
    try:
        task_id = start_aliyun_task(
            client,
            episode,
            source_language,
            os.environ.get("ALIYUN_TINGWU_APP_KEY"),
            file_url=signed_url,
            task_key=f"{safe_name(episode)}-oss",
        )
        print(f"  Aliyun OSS task id: {task_id}", flush=True)
        data = wait_aliyun_task(client, task_id, poll_seconds, timeout_minutes)
        result = data.get("Result") or {}
        transcription_url = result.get("Transcription")
        if not transcription_url:
            raise RuntimeError(f"Aliyun OSS task {task_id} completed but has no transcription URL: {data}")
        transcript = transcript_from_aliyun_json(fetch_json_url(transcription_url))
        if not transcript:
            raise RuntimeError(f"Aliyun OSS task {task_id} returned no recognizable text")
        return transcript
    finally:
        delete_oss_objects([uploaded_key])


def insert_transcript(path: Path, transcript: str, engine: str) -> None:
    text = path.read_text(encoding="utf-8")
    if TRANSCRIPT_MARKER in text:
        return
    block = f"\n{TRANSCRIPT_MARKER}\n\n_Source: audio transcription via {engine}._\n\n{transcript.strip()}\n"
    path.write_text(text.rstrip() + "\n" + block, encoding="utf-8")


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--since", default="2025-01-01", help="Only transcribe episodes published on/after YYYY-MM-DD.")
    parser.add_argument("--limit", type=int, default=3, help="Maximum episodes to transcribe in this run.")
    parser.add_argument("--show", help="Only transcribe one show slug.")
    parser.add_argument("--category", help="Only transcribe one category.")
    parser.add_argument("--include-existing", action="store_true", help="Reprocess files even if they already contain a transcript.")
    parser.add_argument("--engine", choices=["openai", "command", "aliyun-tingwu"], default="openai")
    parser.add_argument("--openai-model", default=DEFAULT_OPENAI_MODEL)
    parser.add_argument("--language", default="zh")
    parser.add_argument("--command", help="Command template for --engine command; must print transcript to stdout and use {audio}.")
    parser.add_argument("--aliyun-source-language", default="fspk", help="Aliyun Tingwu SourceLanguage: cn, en, fspk, ja, or yue.")
    parser.add_argument("--aliyun-poll-seconds", type=int, default=30)
    parser.add_argument("--aliyun-timeout-minutes", type=int, default=180)
    parser.add_argument("--aliyun-use-oss-url", action="store_true", help="Download audio, upload one temporary OSS object, and pass the signed URL to Tingwu.")
    parser.add_argument("--aliyun-split-minutes", type=int, default=0, help="Split long audio into N-minute chunks, upload chunks to OSS, then stitch transcripts.")
    parser.add_argument("--continue-on-error", action="store_true", help="Log failed episodes and keep processing the batch.")
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

    failures: list[tuple[EpisodeFile, str]] = []
    for index, episode in enumerate(episodes, 1):
        print(f"[{index}/{len(episodes)}] {episode.category}/{episode.show}: {episode.title}", flush=True)
        try:
            if args.engine == "openai":
                audio = download_audio(episode)
                transcript = transcribe_with_openai(audio, args.openai_model, args.language)
                engine = f"OpenAI {args.openai_model}"
            elif args.engine == "command":
                audio = download_audio(episode)
                transcript = transcribe_with_command(audio, args.command or "")
                engine = args.command or "command"
            else:
                if args.aliyun_split_minutes > 0:
                    transcript = transcribe_with_aliyun_tingwu_chunks(
                        episode,
                        args.aliyun_source_language,
                        args.aliyun_poll_seconds,
                        args.aliyun_timeout_minutes,
                        args.aliyun_split_minutes,
                    )
                    engine = f"Aliyun Tingwu chunked {args.aliyun_split_minutes}m ({args.aliyun_source_language})"
                elif args.aliyun_use_oss_url:
                    transcript = transcribe_with_aliyun_tingwu_oss_url(
                        episode,
                        args.aliyun_source_language,
                        args.aliyun_poll_seconds,
                        args.aliyun_timeout_minutes,
                    )
                    engine = f"Aliyun Tingwu OSS URL ({args.aliyun_source_language})"
                else:
                    transcript = transcribe_with_aliyun_tingwu(
                        episode,
                        args.aliyun_source_language,
                        args.aliyun_poll_seconds,
                        args.aliyun_timeout_minutes,
                    )
                    engine = f"Aliyun Tingwu ({args.aliyun_source_language})"
            insert_transcript(episode.path, transcript, engine)
            print(f"  wrote transcript to {episode.path}")
        except Exception as exc:
            if not args.continue_on_error:
                raise
            message = str(exc)
            failures.append((episode, message))
            print(f"  failed: {message}", file=sys.stderr, flush=True)
    if failures:
        print("\nFailed episodes:", file=sys.stderr)
        for episode, message in failures:
            print(f"- {episode.category}/{episode.show}: {episode.title} :: {message}", file=sys.stderr)
    return 0 if not failures or args.continue_on_error else 1


if __name__ == "__main__":
    raise SystemExit(main())
