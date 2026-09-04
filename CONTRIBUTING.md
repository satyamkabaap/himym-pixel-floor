# Contributing

Fork, branch, `pip install requests`, run `python director.py`, keep CI green.

## Before you start
- Cross-platform paths (`os.path`), no hardcoded C:\ anything.
- Provider-neutral: everything must work with the LLM **offline** (fallbacks are sacred).
- UI changes derive from `docs/DESIGN.md` tokens.

## Where the bar is
- PRs without a **Before** and **After** (screenshot or recording) don't merge.
  "No UI" just changes what evidence looks like (terminal output counts).
- New dialogue must be in-character and quotable.

Good first issues: fallback dialogue packs, floor props, new events (/slapbet
variants), README translations, kanban cards.
