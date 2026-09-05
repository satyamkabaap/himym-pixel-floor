# HERMES.md — context for the coding agent

Project: HIMYM Pixel Floor (v10 "The Coworker Release")
Stack: Python stdlib + requests backend (director.py), vanilla JS canvas frontend
       (dashboard.html + ui_plus.js + coworker.js), zero-build, ships as one exe.

Current architecture:
- director.py v10: task pipeline (queue→draft→review→approve→outputs/),
  episodes, guests, TF-IDF memory palace, relationships, achievements,
  /api/task /api/episode /api/speed /api/auto /api/control /api/health,
  atomic JSON writes, RLock thread safety, LLM circuit breaker.
- dashboard.html v7+: outlined pixel sprites, delta-time door pathing,
  day/night AI floors, weather, particles, envelopes.
- Modules: ui_plus.js (cold open, cinema, themes, kanban, drawer),
  coworker.js (live work screens, take-the-wheel, audit trail, portrait support with procedural fallback).

Rules:
- Keep zero external frontend deps and offline fallbacks sacred.
- Keys ONLY via env HIMYM_LLM_KEY or himym_data/llm_key.txt (never commit).
- All JSON writes must use atomic_json().
- UI changes derive from the cream-paper pixel design tokens.


## Agent protocol (v1)
- Specs arrive as specs/spec-NNN-*.md (or inbox drops). Implement exactly that scope.
- Commit message: `spec-NNN <short title>`. One spec = one commit.
- After committing, output: git show --stat + full diff (user forwards to reviewer).
- Never: add frontend deps, commit keys, break offline fallbacks, rewrite files
  you weren't asked to (dashboard.html stays modular: ui_plus.js / coworker.js).
