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
