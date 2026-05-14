---
type: dashboard
title: "Dataview Queries — Dirty Laundry"
tags: [dashboard, queries]
---

# Dataview Queries — Dirty Laundry

Open this note in **Reading view** (or live preview) for the queries below to render. Make sure the **Dataview** plugin is installed and enabled.

> Tip: Most queries below scope to `"dossiers"` — that's the folder name. If you rename the folder, update the `FROM` clauses.

---

## Cast at a glance

### Full cast

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  player_name AS "Player",
  role AS "Role",
  age_range AS "Age",
  gender AS "Gender"
FROM "dossiers"
SORT role ASC, character ASC
```

### Suspects only

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Suspect",
  player_name AS "Player",
  alibi AS "Alibi",
  alibi_break AS "Unaccounted Time"
FROM "dossiers"
WHERE role = "SUSPECT"
SORT character ASC
```

### Witnesses & non-suspects

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  player_name AS "Player",
  alibi_location AS "Location",
  alibi AS "Alibi"
FROM "dossiers"
WHERE role != "SUSPECT"
SORT role ASC, character ASC
```

---

## The killer (host eyes only)

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Killer",
  alibi_break AS "Window of Opportunity",
  affiliations AS "Affiliations"
FROM "dossiers"
WHERE is_killer = true
```

---

## Casting

### Characters who still need a player assigned

```dataview
LIST
FROM "dossiers"
WHERE !player_name OR player_name = ""
SORT file.name ASC
```

### Players ↔ characters

```dataview
TABLE WITHOUT ID
  player_name AS "Player",
  link(file.link, character) AS "Character",
  role AS "Role"
FROM "dossiers"
WHERE player_name AND player_name != ""
SORT player_name ASC
```

---

## The connection web

### Everyone connected to Paloma (the victim)

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  role AS "Role",
  alibi_break AS "Unaccounted Time"
FROM "dossiers"
WHERE any(connections, (c) => contains(string(c), "Paloma"))
SORT role ASC, character ASC
```

### Gloria's network

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  affiliations AS "Affiliations"
FROM "dossiers"
WHERE any(connections, (c) => contains(string(c), "Gloria"))
SORT character ASC
```

### Connection counts (most central characters)

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  length(connections) AS "Connections"
FROM "dossiers"
WHERE connections
SORT length(connections) DESC
```

---

## Alibis & opportunity

### Suspects with unaccounted-for time

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Suspect",
  alibi_location AS "Where",
  alibi_break AS "Gap"
FROM "dossiers"
WHERE role = "SUSPECT" AND alibi_break AND alibi_break != "None" AND alibi_break != ""
SORT character ASC
```

### Who was in the conference room

```dataview
LIST alibi
FROM "dossiers"
WHERE contains(lower(alibi_location), "conference")
```

---

## Affiliations

### Hotel staff

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  role AS "Role"
FROM "dossiers"
WHERE contains(file.tags, "#hotel-staff")
SORT character ASC
```

### Cartel-adjacent (Gloria's operation)

```dataview
TABLE WITHOUT ID
  link(file.link, character) AS "Character",
  affiliations AS "Affiliations"
FROM "dossiers"
WHERE any(affiliations, (a) => contains(lower(a), "cartel") OR contains(lower(a), "launder") OR contains(lower(a), "operative") OR contains(lower(a), "trafficking"))
SORT character ASC
```

---

## Round cards

```dataview
TABLE WITHOUT ID
  round AS "Round",
  link(file.link, title) AS "Title",
  in_game_time AS "Time",
  scene AS "Scene"
FROM "round cards"
SORT round ASC
```

---

## Reference index

```dataview
LIST
FROM "Reference Material" OR "host guide"
SORT file.name ASC
```

---

## Building blocks (copy/paste these)

### Inline metadata

You can also use **inline fields** anywhere in note body — just write `key:: value`. Example inside a dossier:

```
Threat level:: high
Motive:: revenge
```

Then query with:

```dataview
TABLE motive, "threat level" AS "Threat"
FROM "dossiers"
WHERE motive
```

### `dataviewjs` (if you enabled JS queries)

````markdown
```dataviewjs
const suspects = dv.pages('"dossiers"').where(p => p.role === "SUSPECT");
dv.paragraph(`There are **${suspects.length}** suspects.`);
```
````
