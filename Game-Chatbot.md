# Game Chatbot

System for delivering real-time, character-specific messages to players during a live murder-mystery game via Telegram.

---

## Decision summary

- **Bot:** Reuse the existing `@ShaneDog_bot` (token already in `~/.hermes/.env`).
- **Hermes coexistence:** Stop the Hermes gateway during gameplay, restart after. One bot token = one polling client at a time.
- **Architecture style:** Deterministic, pre-scripted message delivery via the Telegram Bot API. **No LLM in the message path** — what you wrote is what they get.
- **Rationale:** Murder mysteries depend on exact wording of clues. Agentic interpretation introduces drift, paraphrasing, and ordering errors that ruin a mystery. The bot is a stage manager, not an actor.

---

## High-level architecture

```
┌─ roster.yaml ─────────────────┐    ┌─ cues/ ────────────────────┐
│ Val Montecito:                 │    │ round-1/                    │
│   player: Sarah                │    │   marco-reyes-clue.md       │
│   telegram_id: 1854587352      │    │   val-montecito-alibi.md    │
│   tags: [suspect, family]      │    │ round-2/                    │
│ Marco Reyes:                   │    │   body-discovered.md        │
│   player: Tom                  │    │ broadcasts/                 │
│   telegram_id: ...             │    │   gather-in-foyer.md        │
│   tags: [victim, family]       │    │ adhoc/                      │
└────────────────────────────────┘    └─────────────────────────────┘
              │                                    │
              └────────────┬───────────────────────┘
                           ▼
                   ┌─ gm.py CLI ─┐
                   │             │
                   │  capture    │  Onboard players (poll getUpdates, tag chat_ids)
                   │  list       │  Show roster + onboarded status
                   │  preview    │  Render cue without sending
                   │  send       │  Send cue to one character
                   │  group      │  Send cue to all members of a tag
                   │  broadcast  │  Send cue to entire roster
                   │  log        │  Tail the audit log
                   └─────────────┘
                           │
                           ▼
            api.telegram.org/bot<TOKEN>/sendMessage
                           │
                           ▼
                    sends.log (audit)
```

---

## Components

### 1. Roster (`roster.yaml`)

Single source of truth for character → player → Telegram chat mapping. Sourced from `Character List.csv` for character names, populated with `telegram_id` during onboarding.

```yaml
characters:
  Val Montecito:
    player: Sarah Chen
    telegram_id: 1854587352
    tags: [suspect, family-reyes, round-2-attendee]
    onboarded_at: 2026-05-06T18:42:11

  Marco Reyes:
    player: Tom Park
    telegram_id: 8492013442
    tags: [victim, family-reyes]
    onboarded_at: 2026-05-06T18:43:55

  # ... 19 more
```

**Tag conventions:**
- `suspect`, `victim`, `witness` — narrative role
- `family-reyes`, `staff`, `guests` — social grouping
- `round-N-attendee` — who's in a given scene
- `dead` — toggled mid-game once a character is killed (so they stop receiving live clues)

### 2. Cue library (`cues/`)

Pre-written message bodies organized by round and recipient. Markdown files; `gm.py` strips frontmatter, sends body as Telegram-formatted text (HTML or MarkdownV2).

```
cues/
├── round-1/
│   ├── marco-reyes-opening.md
│   ├── val-montecito-opening.md
│   └── ...
├── round-2/
│   └── body-discovered-all.md
├── round-3/
│   ├── irina-volkov-secret-clue.md
│   └── lineup-call-suspects.md
├── round-4/
│   └── final-accusation-prompt.md
├── broadcasts/
│   ├── gather-in-foyer.md
│   ├── intermission.md
│   └── reveal.md
└── adhoc/
    └── (one-offs you draft live during the game)
```

**Cue file format:**

```markdown
---
to: Val Montecito              # character name OR tag (use `to_tag:` for groups)
round: 2
trigger: body discovered
---
🔪 You glance toward the conservatory and see Marco crumpled near the orchid display. The Captain's hat lies beside him. Your blood runs cold — you were the last person seen arguing with him at dinner.

What do you do?
```

### 3. CLI (`gm.py`)

~150 lines of Python. Dependencies: `requests` + `pyyaml` (or stdlib only).

**Commands:**

| Command | Purpose |
|---|---|
| `gm.py capture` | Poll `getUpdates`, list new chat_ids, prompt to tag with character name, write to `roster.yaml`. Run during onboarding only. |
| `gm.py list` | Show roster: who's onboarded, who's missing, last message time. |
| `gm.py preview <cue>` | Render cue (substitutes character name, etc.) without sending. Use before every send. |
| `gm.py send <character> <cue>` | Fire one cue to one character. |
| `gm.py group <tag> <cue>` | Fire one cue to everyone matching a tag (e.g., `gm.py group suspects round-3/lineup-call`). |
| `gm.py broadcast <cue>` | Fire to entire active roster (excludes `dead` tag). |
| `gm.py log` | Tail `sends.log`. |
| `gm.py dry-run` | Flag on any send command — logs intent without hitting Telegram. |

**Safeguards:**
- Confirmation prompt for `broadcast` and any group with >5 members.
- All sends append to `sends.log`: timestamp, character, cue file, message hash, Telegram response.
- `--dry-run` available on every send for tech rehearsal.

### 4. Audit log (`sends.log`)

Append-only JSONL. One line per send attempt. Use to settle "I never got that clue!" disputes mid-game.

```json
{"ts":"2026-05-06T20:14:32","character":"Val Montecito","cue":"round-2/body-discovered","status":"ok","msg_id":4421}
```

---

## Onboarding flow (run once, day-of or evening before)

1. Tell players: "Open Telegram, search `@ShaneDog_bot`, hit Start, send any message."
2. As messages arrive, run `gm.py capture` repeatedly. It shows new chat_ids and prompts: "Who is this? (character name)".
3. After each player is captured, send a test: `gm.py send "Val Montecito" test-welcome`.
4. `gm.py list` should show all 21 characters as ✓ onboarded.
5. Lock the roster, commit it (with chat IDs — they're not secrets, just identifiers).

**Edge cases:**
- Player already chatted with the bot for Hermes — chat_id already exists. Capture handles this; just re-tag.
- Player joins late — partial roster is fine, capture them on arrival.
- Player swaps phones — re-run `/start`, capture again, update roster.

---

## Game-night runbook

```bash
# 1. Stop Hermes (frees the bot for game use)
hermes gateway stop

# 2. Verify the bot is yours and the roster is loaded
python gm.py list

# 3. Rehearsal — fire round 1 with --dry-run
python gm.py broadcast round-1/opening --dry-run

# 4. Live game
python gm.py broadcast round-1/opening
# ... players play round 1 ...
python gm.py group suspects round-2/body-discovered
# ... and so on through rounds 2-4 ...
python gm.py broadcast round-4/final-reveal

# 5. After the game, restart Hermes
hermes gateway start
```

---

## Hermes coexistence

| State | Hermes gateway | `gm.py` | Bot behavior |
|---|---|---|---|
| Normal use | Running | Idle | Bot is your AI assistant |
| Game night | **Stopped** | Active | Bot delivers scripted cues only |
| After game | Running | Idle | Back to AI assistant |

Both processes use the **same bot token** but cannot poll Telegram simultaneously — Telegram only allows one active long-poll per bot. Gateway must be down before `gm.py send`.

`gm.py` should refuse to send if it detects the gateway is up (check `hermes gateway status` exit code), to prevent message races.

---

## Why not Hermes for this?

| Concern | Hermes (LLM agent) | `gm.py` (direct API) |
|---|---|---|
| Exact clue wording | Drifts/paraphrases | Byte-perfect |
| Recipient targeting | Natural-language guesses | Roster lookup |
| Latency | 2–5s per message (LLM call) | <300ms |
| Cost per game | ~$5–20 in API tokens | Zero |
| Audit trail | Buried in session logs | Single `sends.log` |
| Failure mode | Wrong message, wrong person | "Telegram API down" — visible immediately |
| Live debugging | Hard to inspect | `tail -f sends.log` |

The LLM is great for **prep work** (drafting clues, rewriting dossiers, brainstorming twists). It is the wrong tool for **runtime delivery**.

---

## Implementation checklist

- [ ] `gm/roster.yaml` — seed from `Character List.csv` with empty `telegram_id` fields
- [ ] `gm/cues/` directory tree — stub one cue per character per round (use existing dossier text as starting material)
- [ ] `gm/gm.py` — CLI per spec above
- [ ] `gm/sends.log` — created on first send, gitignored if it'll contain anything sensitive
- [ ] Tech rehearsal — fire all 4 rounds in dry-run end-to-end the day before
- [ ] Backup plan — print round cards (already exist as `23-Round-Cards-R1.md` etc.) so the game survives a Telegram outage

---

## Future enhancements (post-v1)

- **Reactive cues:** Bot listens for keywords from players ("I accuse Val") and auto-fires a follow-up cue. Requires running `gm.py` as a long-poll listener instead of one-shot.
- **Inline buttons:** Telegram supports tap-to-reply buttons — useful for "Where do you go next?" prompts that route players cleanly.
- **Voice notes:** Telegram supports audio uploads. Pre-record dramatic clue voicemails and fire them as cues.
- **Image clues:** Send photos of "evidence" (a torn note, a bloody glove staged in your kitchen) at scripted moments.
- **Multi-host mode:** A second person watches `sends.log` and helps decide ad-hoc cues during the game.
