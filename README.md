<div align="center">

# 🎬 HIMYM PIXEL FLOOR

**The world's most legendary agents. The world's most sitcom workplace.**

*A multi-agent harness that runs the HIMYM gang as your autonomous studio —*
*they draft, review and ship **real deliverables** to your disk on a living*
*pixel-art floor, while Future Ted narrates it all.*

![Apartment & MacLaren's — day](floor_day.png)
![Apartment & MacLaren's — night](floor_night.png)

[![Release](https://img.shields.io/github/v/release/satyamkabaap/himym-pixel-floor?style=for-the-badge&color=b07f22)](https://github.com/satyamkabaap/himym-pixel-floor/releases)
[![License](https://img.shields.io/github/license/satyamkabaap/himym-pixel-floor?style=for-the-badge&color=5da668)](LICENSE)
[![Stars](https://img.shields.io/github/stars/satyamkabaap/himym-pixel-floor?style=for-the-badge&color=e0a43c)](https://github.com/satyamkabaap/himym-pixel-floor/stargazers)
[![Last commit](https://img.shields.io/github/last-commit/satyamkabaap/himym-pixel-floor?style=for-the-badge&color=5b8db8)](https://github.com/satyamkabaap/himym-pixel-floor/commits)
[![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)

**⬇ [Download for Windows](../../releases)** · no Python needed · **zero telemetry, forever**

</div>

---

## 🤔 Wait, what is this?

HIMYM Pixel Floor wraps five LLM personas in a **hive**: shared memory, a task
pipeline, and a GOD orchestrator (Future Ted). Every agent is an avatar on a
hand-painted day/night floor — they walk between the apartment and MacLaren's,
chat, drink scotch, and **actually work**: every approved task becomes a
markdown deliverable in `himym_data/outputs/`.

- **Every persona is an agent.** In-character writer, hype-man, legal, creative and research — with your LLM *or* fully offline fallbacks.
- **Every agent is an avatar.** Outlined pixel sprites on AI-painted floors that shift with sim time, weather and the weekly schedule.
- **The hive coordinates them.** Queue → draft → review → revise → approve, with a collab graph that thickens as pairs ship work together.
- **Real work ships.** No theater. Approved tasks are saved as files you can open.

## ✨ Features

| | |
| --- | --- |
|  **One narrator, not five** | Future Ted (GOD) assigns, routes and narrates. You brief the floor, not individuals. |
| 🤖 **Full automation** | Auto-tasks when idle, `.txt` drops into `inbox/`, or the UI queue (`POST /api/task`). |
| 🔁 **Draft → Review → Approve** | Marshall reviews contracts, Lily signs off on design, Barney makes it legendary. |
| 🎬 **Scripted episodes** | *Slapsgiving*, *The Blue French Horn*, *The Legendary Party*, *The Playbook* — spotlight, SFX, weather & recap cards. |
| 🌟 **Guest stars** | Drop a JSON in `himym_data/guests/` → Carl or Tracy join the cast. Community-extensible. |
| 🧠 **Memory palace** | TF-IDF semantic recall + searchable UI. The gang remembers what matters. |
| 🎮 **Take the wheel** | Pause-free human takeover: drive any character, assign work, hand back — audited. |
| 💻 **Coworker screens** | Click a character → watch their draft/review type out live. |
| 🌗 **Day/night + weather** | Rain, snow, lamp glow, TV static, steam — the floor is alive. |
| 🎨 **Themes & cinema mode** | Cream / midnight / blue-horn themes; letterboxed cinema mode with grain. |
| 🔊 **Voice in & out** | Mic queues tasks by speech; Future Ted reads recaps aloud. |
| 📸 **Polaroid album** | Auto-shots at episode wraps & group photos, saved locally. |
| 🪟 **One-click installer** | Inno Setup wizard, per-user install, uninstaller. |
| 🔒 **Zero telemetry** | Everything runs on your machine. Nothing phones home. Ever. |

## 🎭 The Cast

| Agent | Role in the hive | Signature move |
| --- | --- | --- |
| **Ted** | writer / architect | Blue french horn energy |
| **Barney** | pitch / hype | *"Suit up."* |
| **Marshall** | legal review | Slap-bet enforcement |
| **Lily** | creative director | Matchmaking + wine |
| **Robin** | research / facts | *Scotch. Neat. Now.* |
| **Future Ted** | GOD / narrator | *"Kids…"* |
| **carl · tracy** | guest stars | drop-in JSON hires |

## 🚀 Quick start

**Option A — Installer (Windows):** grab `HIMYM_PixelFloor_Setup_*.exe` from
[Releases](../../releases), run it, done.

**Option B — From source:**

```bash
git clone https://github.com/satyamkabaap/himym-pixel-floor.git
cd himym-pixel-floor
pip install -r requirements.txt
python director.py        # serves + auto-opens the dashboard
```

**Option C — Build everything yourself:** `build_installer.bat`

Flags: `--seed 42` (reproducible demo) · `--port 9000` · `--no-browser` · `--version`

## ⚙️ How it works

```
        you ── queue / inbox / auto ──► ┌──────────────┐
                                        │  FUTURE TED  │  GOD · narrator
                                        └──────┬───────┘
                          assign · review · approve · narrate
        ┌──────────┬──────────┬──────────┼──────────┬──────────┐
        ▼          ▼          ▼          ▼          ▼          ▼
      Ted       Barney     Marshall    Lily       Robin
     writer      hype       legal    creative   research
        └────────── shared hive: memory · tasks · outputs ──────┘
```

A shipped deliverable:

```markdown
# Task 007: Draft the official slap bet contract

## Draft by marshall
- Clause 1: be excellent to each other
- Clause 2: sandwiches mandatory

## Review by lily
APPROVE: chef's kiss.
```

## 🔌 HTTP API

| Endpoint | Purpose |
| --- | --- |
| `POST /api/task` | queue work (`{"text":"...","worker":"marshall"}`) |
| `POST /api/episode` | start an episode (`{"id":"slapsgiving"}`) |
| `POST /api/control` | take the wheel / hand back / override |
| `POST /api/speed` · `POST /api/auto` | pause + speed · auto-toggle |
| `GET /api/health` | version, uptime, cast, breaker state |

**Shortcuts:** `Space` pause/speed · `C` cinema · `S` polaroid · `F` fullscreen

## 🗺️ Roadmap

- [x] Scripted episodes *(v5)* · Voice narration *(v9)* · Guest stars *(v6)* · Governance & coworker screens *(v10)*
- [ ] Slack / Telegram intake · [ ] Parallel workers + kanban v2

## 🤝 Contributing

See [`CONTRIBUTING.md`](CONTRIBUTING.md) — **every PR must show a before and an after.**
Policies: [`SECURITY.md`](SECURITY.md) · [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) · [`CHANGELOG.md`](CHANGELOG.md)

## 💛 License & love

Code **MIT** · Floor art AI-generated · Fonts Pixelify Sans & VT323 (SIL OFL) ·
Inspired by [`munder-difflin`](https://github.com/chaitanyagiri/munder-difflin) &
CopilotKit *OpenBot* (MIT) · Built by a human + two AI coworkers.

_An affectionate fan parody. Not affiliated with CBS, 20th Television, or the
creators of How I Met Your Mother._

---

<div align="center">**It's going to be legendary. Wait for it…** 🎩</div>
