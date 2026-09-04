# Architecture
Two planes, one renderer:
- **Event plane (director.py):** task pipeline (queued→drafting→reviewing→revising→done),
  inbox scanner, auto-task generator, LLM-with-fallback, memory + collab persistence.
- **Data plane (sim_data.json):** the contract the UI reads every 2s —
  {location, agents{status, sub_location, last_dialogue, memory}, tasks[], stats, collab, time_of_day}.
- **Renderer (dashboard.html):** canvas floor (AI art + procedural sprites),
  command center tabs, POST /api/task for intake.
Single-committer file writes; no locks; JSON atomic enough for a sim.
