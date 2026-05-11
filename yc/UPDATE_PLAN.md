# YC Library Weekly Update Plan

## Scope

Source: <https://www.ycombinator.com/library>

Track only these YC Library series for now:

- Lightcone Podcast
- How To Build The Future
- Hard Tech

Archive Markdown files under `yc/library/<series>/`. Keep transcripts when YC provides them in the Library page payload.

## Cadence

- Frequency: weekly.
- Default run day: Monday.
- Historical baseline: items since 2024-05-11.
- Ongoing behavior: rerun `scripts/fetch_yc_library.py`; new matching YC Library entries are added to the archive and index.

## User Focus

- Lightcone Podcast: AI startup direction, founder workflows, agent products, model/application shifts, market timing.
- How To Build The Future: top founder/operator judgment, company-building patterns, strategy, product taste, enduring lessons.
- Hard Tech: hard-tech startup wedge, milestone sequencing, capital intensity, regulatory/customer path, AI/robotics/science infrastructure overlap.

## Update Command

Run from the repository root:

```bash
python3 scripts/fetch_yc_library.py --since 2024-05-11
```

Then review `yc/library/README.md` and summarize:

1. New YC Library entries by series.
2. Why each matters for AI / Web3 / startup / market-investing reading focus.
3. People, companies, or concepts worth tracking.
4. Whether any transcript suggests a deeper follow-up memo.
