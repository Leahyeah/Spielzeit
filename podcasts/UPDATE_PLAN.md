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

RSS text is only a lightweight baseline. For fuller historical text, transcribe audio for episodes published from 2025 onward and for new episodes.

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

Recommended tool setup:

- `ffmpeg` for audio conversion/chunking and local transcription tools.
- One transcription engine:
  - OpenAI audio transcription API with `OPENAI_API_KEY`, or
  - local `whisper.cpp` / `faster-whisper` / `mlx-whisper` that can print text from an audio path.
