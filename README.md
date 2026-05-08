# Spielzeit

## Anthropic Research Archive

- Markdown archive index: [anthropic/README.md](anthropic/README.md)
- Update script: [scripts/fetch_anthropic_research.py](scripts/fetch_anthropic_research.py)

Run the script from the repository root to refresh Anthropic public research pages from the sitemap:

```bash
python3 scripts/fetch_anthropic_research.py
```

## Podcast Archive

- Podcast index: [podcasts/README.md](podcasts/README.md)
- Feed configuration: [podcasts/feeds.json](podcasts/feeds.json)
- Update script: [scripts/fetch_podcasts.py](scripts/fetch_podcasts.py)

Run the script from the repository root to refresh podcast RSS metadata and text fields. Audio files are linked but not stored:

```bash
python3 scripts/fetch_podcasts.py
```

To transcribe audio into episode Markdown for fuller text history, configure a transcription engine first, then run:

```bash
python3 scripts/transcribe_podcasts.py --since 2025-01-01 --limit 3
```

For Aliyun Tingwu transcription, install the optional SDK and provide credentials through local environment variables:

```bash
python3 -m pip install -r requirements-transcription.txt
```

Then create a local `.env` file from `.env.example` and fill in the real values. `.env` is ignored by git:

```bash
cp .env.example .env
```

Run a small test:

```bash
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --since 2025-01-01 --limit 3
```

For long episodes that exceed Tingwu's duration quota, install `ffmpeg`, configure OSS fields in `.env`, then run chunked transcription:

```bash
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --aliyun-split-minutes 45 --since 2025-01-01 --limit 1
```

Chunked mode downloads audio locally, splits it with `ffmpeg`, uploads temporary chunks to OSS, submits each signed URL to Tingwu, stitches the transcripts, then deletes the temporary OSS objects.

For feeds whose original audio URL is not readable by Tingwu, use OSS as a temporary URL bridge without splitting:

```bash
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --aliyun-use-oss-url --show sv101 --limit 1
```
