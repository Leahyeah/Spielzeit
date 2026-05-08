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
