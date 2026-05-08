# Podcast Weekly Update Plan

## Cadence

- Frequency: weekly.
- Storage: RSS metadata and available text fields only; audio files are linked but not stored.
- Anthropic research updates are maintained separately under `anthropic/`.

## User Focus

### AI

- Technology and model development trends.
- Human-AI interaction patterns.
- Hard technical knowledge worth extracting and retaining.

### Web3

- Track theme development rather than every market movement.
- Current known themes: real-world asset tokenization, MicroStrategy / DAT style treasury vehicles, chain-level technology development.
- Add new themes when they recur across episodes.

### 创业

- Interviewee and founder clues.
- Company, product, and go-to-market patterns.
- Market trends surfaced through founder/investor interviews.

### 市场投资

- Macro and market regime changes.
- Asset class signals and risk events.
- Industry-level capital flow and sentiment changes.

## Weekly Output Shape

For each category:

1. New episodes this week.
2. Why they matter for the user's focus.
3. Emerging themes and whether they are new, continuing, or fading.
4. People / companies / concepts to track.
5. Suggested follow-up reading or archive links.

## Maintenance

Run from the repository root:

```bash
python3 scripts/fetch_podcasts.py --weekly-days 8
```

Review `podcasts/weekly/<date>.md`, then send a concise category-based update in Slock.

## Audio Transcription

RSS text is only a lightweight baseline. For fuller text, transcribe selected priority episodes and new weekly episodes. The 2025+ bulk backfill is intentionally capped: do not keep chasing the remaining long-history backlog unless the user explicitly reopens it.

Audio policy:

- Audio is downloaded only into `.cache/podcast-audio/`.
- `.cache/` is ignored by git.
- Only transcript text is written into episode Markdown under `## Transcript`.
- Do not commit audio files.

Script:

```bash
python3 scripts/transcribe_podcasts.py --since 2025-01-01 --limit 3
```

Default engine is OpenAI transcription API and requires `OPENAI_API_KEY` in the local environment. Do not paste API keys into Slock. A local engine can be used instead:

```bash
python3 scripts/transcribe_podcasts.py --engine command --command "your-transcriber {audio}" --since 2025-01-01
```

Aliyun Tingwu is also supported. It creates an offline Tingwu task from each episode's public audio URL, polls task status, fetches the returned `Transcription` JSON, and writes the assembled transcript text into the episode Markdown. Current account/service limits may reject long episodes with `PRE.AudioDurationQuotaLimit`; treat those as skipped rather than blocking the weekly archive.

```bash
python3 -m pip install -r requirements-transcription.txt
cp .env.example .env
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --since 2025-01-01 --limit 3
```

Fill the local `.env` with real credentials before running. `.env` is ignored by git.

Use `--aliyun-source-language fspk` for mixed Chinese/English podcasts, or `cn`, `en`, `ja`, `yue` for single-language shows. Do not paste AccessKey values into Slock.

Batch rule:

- Historical cap: attempted AI recent 20 + Web3 recent 20 in May 2026; do not bulk-backfill the rest.
- Ongoing: transcribe new AI/Web3 priority episodes when they fit the service limit.
- If a priority episode fails with `PRE.AudioDurationQuotaLimit`, keep RSS text/description and mention the skip in the weekly update, or use chunked mode for selected important episodes.

Chunked mode for long episodes:

```bash
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --aliyun-split-minutes 45 --category AI --limit 1
```

Requirements:

- `ffmpeg` available in `PATH`.
- OSS settings in local `.env`: `ALIYUN_OSS_BUCKET`, `ALIYUN_OSS_ENDPOINT`, `ALIYUN_OSS_PREFIX`, `ALIYUN_OSS_SIGNED_URL_EXPIRES`.
- The script uploads temporary chunks, uses signed URLs as Tingwu `FileUrl` inputs, stitches `[Part N/M]` transcripts, and deletes temporary OSS objects.

For feeds whose original audio URL is not readable by Tingwu, use OSS as a temporary URL bridge without splitting:

```bash
python3 scripts/transcribe_podcasts.py --engine aliyun-tingwu --aliyun-use-oss-url --show sv101 --limit 1
```

Recommended tool setup:

- `ffmpeg` for audio conversion/chunking and local transcription tools.
- One transcription engine:
  - OpenAI audio transcription API with `OPENAI_API_KEY`, or
  - Aliyun Tingwu OpenAPI with local `ALIBABA_CLOUD_ACCESS_KEY_ID`, `ALIBABA_CLOUD_ACCESS_KEY_SECRET`, and `ALIYUN_TINGWU_APP_KEY`, or
  - local `whisper.cpp` / `faster-whisper` / `mlx-whisper` that can print text from an audio path.
