---
type: timeline
title: "Crime Scene Timeline — Dirty Laundry"
audience: host
tags: [timeline, host-guide]
---

# Crime Scene Timeline

> Master reference for the host. Public-facing facts up top; the killer's actual movements are at the bottom (host-only spoiler — fold or scroll past if a player is over your shoulder).

---

## Pre-party (the days before)

| When | Event | Source |
|---|---|---|
| 2 days before | Paloma comes to confession with [[Jimmy]]. Distraught — "terrible things," "people who would kill her." | [[Jimmy]] |
| 2 days before | Paloma gives [[Sasha]] a sealed envelope: "If anything happens to me, give this to the authorities." | [[Sasha]] |
| 2 days before | Cleaning chemicals go missing from the maintenance closet. [[Pepe]] files report; nobody follows up. | [[Pepe]] |
| 1 day before | [[Val]] and Paloma in heated argument on the beach. Photographed. | [[Fiona]] |
| 1 day before | [[Val]] grabs Paloma's arm in the lobby; Paloma pulls away. | [[Sasha]] |
| 1 day before | Paloma makes a cruel comment about [[Pam]]; Pam tells multiple people she'll "make her pay." | [[Destiny]], multiple |
| Day-of, 5 AM | [[Jimmy]] sees [[Dex]] leaving [[Irina]]'s staff quarters with two coffees. | [[Jimmy]] |

---

## The night (chronological)

| Time | Event | Actor(s) | Location |
|---|---|---|---|
| 6:00 PM | Generator repair begins, off-property | [[Pepe]] | Far property |
| 6:00 PM | Service stairwell side exit propped open with doorstop | Unknown | Side exit |
| 7:00 PM | Sasha takes over front desk for the evening | [[Sasha]] | Front desk |
| 7:00 PM | Zoya settles at lobby bar (stays until midnight) | [[Zoya]] | Lobby bar |
| 7:00 PM | Garment bag delivered to Paloma's room via laundry | [[Irina]] | Laundry → Paloma's floor |
| 7:30 PM | Gloria visits chaplain — "I'd do anything to protect my children." | [[Gloria]] | Chapel |
| 8:00 PM | Gerald and Lorraine join Gloria in the conference room | [[Gerald]], [[Lorraine]], [[Gloria]] | Conference room |
| 8:00 PM | Dex and Doug in intense conversation at the bar — they "knew each other from before" | [[Dex]], [[Doug]] | Bar |
| 8:00 PM | Gloria on phone speaking rapid Spanish, serious tone | [[Gloria]] | Courtyard |
| 8:30 PM | Destiny begins continuous live-stream (until 11:45 PM) | [[Destiny]] | Main party |
| 9:00 PM | Paloma was scheduled to give a toast — no-show | — | — |
| 9:00 PM | Zane visibly panicking, stress-checking phone | [[Zane]] | Party area |
| 9:00 PM | Jimmy leads sunset meditation circle (8 witnesses, until 10:30 PM) | [[Jimmy]] | Meditation area |
| 9:00 PM | Rosa starts continuous corporate video call (until 11 PM) | [[Rosa]] | Manager's office |
| 9:15 PM | Val and Zane retreat to Val's private suite | [[Val]], [[Zane]] | Val's suite |
| 9:30 PM | Pam's memory cuts out (blackout begins) | [[Pam]] | Party area |
| 9:30 PM | Val's suite back staircase propped open | Unknown | Back staircase |
| 9:45 PM | Doug arrives via service entrance — contradicts his "in Pittsburgh" alibi | [[Doug]] | Service entrance |
| 10:00 PM | Marco takes a 15-min "bathroom break" from valet stand | [[Marco]] | Service area |
| 10:00 PM | Silhouette on Val's back staircase — identity unclear | Unknown | Back staircase |
| 10:05 PM | Owner override card swiped on Paloma's floor (only [[Val]] has it) | [[Val]] | Paloma's floor |
| 10:07 PM | Master key used at service area | Marco / Irina / maintenance | Service area |
| 10:15 PM | Dex takes a 20-min "break" from the bar | [[Dex]] | Staff area (with Irina) |
| 10:25 PM | Gloria steps out of conference room — "restroom" (~10 min absence) | [[Gloria]] | Conference room → ??? |
| 10:30 PM | Jimmy alone in chapel writing sermon (until midnight) | [[Jimmy]] | Chapel |
| 10:45 PM | Irina "discovers" the body and screams | [[Irina]] | Laundry room |
| 11:30 PM | Pam wakes near laundry with chemical residue on her hand — no memory | [[Pam]] | Near laundry |
| 12:00 AM | Doug's "official" arrival through the main entrance | [[Doug]] | Front desk |

---

## Forensic / key card log (Mentalist hands these out as evidence)

| Time | Item | Reading | Round to reveal |
|---|---|---|---|
| 6:00 PM | Side exit | Propped open with doorstop (fire code violation) | Round 2 |
| 7:00 PM | Laundry log | Garment bag routed to Paloma's room | Round 3 |
| 9:30 PM | Val's back staircase | Door wedged open | Round 2 |
| 9:45 PM | Service entrance | Doug enters (no log entry until midnight) | Round 2 |
| 10:05 PM | Owner override card | Swiped on Paloma's floor | Round 3 |
| 10:07 PM | Master key | Service area | Round 2 |
| 10:25 PM | Conference room exit | Gloria steps out | Round 3 |
| 10:45 PM | Body discovered | Irina, laundry room | Round 1 (end) |

---

## Quick filters

### Where everyone says they were

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  alibi_location AS "Location",
  alibi AS "Alibi"
FROM "dossiers"
WHERE alibi_location AND alibi_location != ""
SORT alibi_location ASC, character ASC
```

### Suspects with unaccounted-for time during the kill window (10:00–10:45 PM)

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Suspect",
  alibi_break AS "Gap"
FROM "dossiers"
WHERE role = "SUSPECT" AND alibi_break AND alibi_break != "None" AND alibi_break != ""
SORT character ASC
```

### Anyone who claims to be in the conference room

```dataview
LIST alibi
FROM "dossiers"
WHERE contains(lower(alibi_location), "conference")
```

---

## HOST EYES ONLY — Gloria's actual movements

> ⚠️ Spoiler. Hide this if a player is reading over your shoulder.

The shirt was the cartel plan. The injection was the mother.

| Time | What actually happened |
|---|---|
| Days before | Gloria gives [[Irina]] a slow-acting dermal toxin and orders her to lace Paloma's dress shirt |
| 7:00 PM | Irina prepares the shirt and routes it through laundry to Paloma's room |
| 7:30 PM | Gloria visits chaplain — laying the "protective mother" alibi groundwork |
| 8:00 PM onward | Gloria builds an ironclad alibi in the conference room with [[Gerald]] and [[Lorraine]] |
| ~10:00 PM | Gloria checks her watch repeatedly; the shirt should have killed Paloma by now |
| 10:25 PM | Steps out "to the restroom." Slips through the side exit to the service corridor. |
| 10:26 PM | Finds Paloma stumbling near laundry, weakened by the toxin. Injects her in the neck with insulin pen loaded with paralytic. ~90 seconds. |
| 10:27 PM | Places body in a laundry basket |
| 10:30 PM | Returns to conference room. Total absence: ~10 minutes. |
| 10:45 PM | [[Irina]] "discovers" the body on cue |

**The tell that breaks her alibi:** [[Marco]] saw her near the service stairwell at 10:25. He's been protecting her all night. When [[Zoya]] outs the Diego connection in Round 3, Marco can't hold it anymore. That's the unlock.

**Two methods, why:** The shirt was professional and deniable. The injection was personal — Gloria needed to look Paloma in the eye for what she did to Diego. A cartel operator would have let the poison finish the job. A mother couldn't.

See: [[00-Master-Storyline]] for the full backstory.
