#!/usr/bin/env python3
"""
Build per-character consolidated dossier packets for distribution.

Each output file in dossiers/ contains:
  1. Costume
  2. Props
  3. Character dossier
  4-7. Round cards 1-4 with "STOP HERE" gates between rounds

Pulls from the existing wiki files and assembles one markdown packet
per playable character.
"""

import re
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "dossiers"
OUT.mkdir(exist_ok=True)

# (output_basename, display_name, dossier_file, costume_anchor, props_anchor, round_keywords)
CHARACTERS = [
    ("01-Val-Montecito",       "Val Montecito",        "03-Val-Montecito.md",       "Val Montecito",         "Val Montecito",         ["VAL"]),
    ("02-Marco-Reyes",         "Marco Reyes",          "04-Marco-Reyes.md",         "Marco Reyes",           "Marco Reyes",           ["MARCO"]),
    ("03-Zane-Nakamura",       "Zane Nakamura",        "05-Zane-Nakamura.md",       "Zane Nakamura",         "Zane Nakamura",         ["ZANE"]),
    ("04-Dex-Calloway",        "Dex Calloway",         "06-Dex-Calloway.md",        "Dex Calloway",          "Dex Calloway",          ["DEX"]),
    ("05-Gloria-Reyes",        "Gloria Reyes",         "07-Gloria-Reyes.md",        "Gloria",                "Gloria Reyes",          ["GLORIA"]),
    ("06-Pam-Worthington",     "Pam Worthington",      "08-Pam-Worthington.md",     "Pam Worthington",       "Pam Worthington",       ["PAM"]),
    ("07-Doug-Kaminski",       "Doug Kaminski",        "09-Doug-Kaminski.md",       "Doug",                  "Doug Kaminski",         ["DOUG"]),
    ("08-Irina-Volkov",        "Irina Volkov",         "10-Irina-Volkov.md",        "Irina Volkov",          "Irina Volkov",          ["IRINA"]),
    ("09-Sunny-Patel",         "Sunny Patel",          "11-Sunny-Patel.md",         "Sunny Patel",           "Sunny Patel",           ["SUNNY"]),
    ("10-Diego-Reyes",         "Diego Reyes (Ghost)",  "12-Diego-Reyes.md",         "Diego Reyes",           "Diego",                 ["DIEGO"]),
    ("11-Fiona-Beaumont",      "Fiona Beaumont",       "13-Fiona-Beaumont.md",      "Fiona Beaumont",        "Fiona Beaumont",        ["FIONA"]),
    ("12-Destiny-Rivers",      "Destiny Rivers",       "14-Destiny-Rivers.md",      "Destiny Rivers",        "Destiny Rivers",        ["DESTINY"]),
    ("13-Zoya-Davenport",      "Zoya Davenport",       "15-Zoya-Davenport.md",      "Zoya Davenport",        "Zoya Davenport",        ["ZOYA"]),
    ("14-Rev-Jimmy-Whitfield", "Rev. Jimmy Whitfield", "16-Rev-Jimmy-Whitfield.md", "Rev. Jimmy Whitfield",  "Rev. Jimmy",            ["JIMMY"]),
    ("15-Rosa-Martinez",       "Rosa Martinez",        "17-Rosa-Martinez.md",       "Rosa Martinez",         "Rosa",                  ["ROSA"]),
    ("16-Lorraine-Chu",        "Lorraine Chu",         "18-Lorraine-Chu.md",        "Lorraine Chu",          "Lorraine Chu",          ["LORRAINE"]),
    ("17-Gerald-Finch",        "Gerald Finch",         "19-Gerald-Finch.md",        "Gerald Finch",          "Gerald Finch",          ["GERALD"]),
    ("18-Nadia-Osei",          "Nadia Osei",           "20-Nadia-Osei.md",          "Nadia Osei",            "Nadia Osei",            ["NADIA"]),
    ("19-Pepe-Stevens",        "Pepe Stevens",         "21-Pepe-Stevens.md",        "Pepe Stevens",          "Pepe Stevens",          ["PEPE"]),
    ("20-Sasha-Kimura",        "Sasha Kimura",         "22-Sasha-Kimura.md",        "Sasha Kimura",          "Sasha Kimura",          ["SASHA"]),
]

ROUND_FILES = {
    1: ("23-Round-Cards-R1.md", "Round 1 — \"The After-Party\"", "8:00 PM – 10:00 PM"),
    2: ("24-Round-Cards-R2.md", "Round 2 — \"Everyone's a Suspect\"", "10:00 PM – 11:00 PM"),
    3: ("25-Round-Cards-R3.md", "Round 3 — \"The Investigation\"",   "11:00 PM – Midnight"),
    4: ("26-Round-Cards-R4.md", "Round 4 — \"The Reveal\"",          "Midnight"),
}


def read(path):
    return (ROOT / path).read_text()


def strip_h1(text):
    """Drop the leading H1 line so it doesn't compete with our packet's H1."""
    lines = text.splitlines()
    out = []
    dropped_h1 = False
    for line in lines:
        if not dropped_h1 and line.startswith("# "):
            dropped_h1 = True
            continue
        out.append(line)
    return "\n".join(out).strip()


def extract_costume(anchor):
    """Pull the character's section from the costume guide."""
    text = read("29-Costume-Guide.md")
    # Find a ### header containing the anchor
    pattern = re.compile(r"^### .*$", re.MULTILINE)
    matches = list(pattern.finditer(text))
    for i, m in enumerate(matches):
        if anchor.lower() in m.group(0).lower():
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            # Stop at a horizontal rule (--- on its own line) before the next ###
            section = text[start:end]
            section = re.split(r"^---\s*$", section, maxsplit=1, flags=re.MULTILINE)[0]
            return section.strip()
    return f"_(Costume entry for {anchor} not found.)_"


def extract_props(anchor):
    """Pull the character's row from the props table."""
    text = read("28-Props-List.md")
    for line in text.splitlines():
        if line.startswith("|") and anchor.lower() in line.lower() and "Character" not in line and "---" not in line:
            # Strip the table pipes for cleaner display
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2:
                return cells[1]
    return f"_(Props row for {anchor} not found.)_"


def extract_round_sections(round_num, keywords):
    """Pull all H3 sections from a round card file whose header matches any keyword."""
    path, _, _ = ROUND_FILES[round_num]
    text = read(path)

    # Skip everything before the first ## MAJOR/MINOR heading so we don't grab the file header
    header_split = re.split(r"^## ", text, maxsplit=1, flags=re.MULTILINE)
    body = "## " + header_split[1] if len(header_split) > 1 else text

    # Find every ### block
    pattern = re.compile(r"^### (.+)$", re.MULTILINE)
    matches = list(pattern.finditer(body))
    chunks = []
    for i, m in enumerate(matches):
        header_line = m.group(1)
        if not any(kw in header_line.upper() for kw in keywords):
            continue
        start = m.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        # Stop at the next ## heading or --- divider
        section = body[start:end]
        section = re.split(r"^## ", section, maxsplit=1, flags=re.MULTILINE)[0]
        section = re.split(r"^---\s*$", section, maxsplit=1, flags=re.MULTILINE)[0]
        chunks.append(section.strip())
    if not chunks:
        return f"_(No specific cue this round — follow the host's lead and stay in character.)_"
    return "\n\n".join(chunks)


def gate(round_num, time_label):
    return f"---\n\n## ⛔ STOP — Wait for the host to call \"ROUND {round_num} — {time_label}\"\n\n---"


def build_packet(out_basename, display_name, dossier_file, costume_anchor, props_anchor, keywords):
    costume = extract_costume(costume_anchor)
    props = extract_props(props_anchor)
    dossier_body = strip_h1(read(dossier_file))

    parts = [
        f"# YOUR GAME PACKET — {display_name}",
        "## Dirty Laundry: Murder in the Caymans",
        "",
        "> **READ BEFORE THE PARTY:** Sections 1, 2, and 3.",
        "> **DO NOT READ AHEAD:** Sections 4–7 are your round cards. Wait for the host to call each round before reading.",
        "",
        "---",
        "",
        "## 1. Your Costume",
        "",
        costume,
        "",
        "---",
        "",
        "## 2. Your Props",
        "",
        props,
        "",
        "---",
        "",
        "## 3. Your Character",
        "",
        dossier_body,
        "",
    ]

    for rn in (1, 2, 3, 4):
        _, title, time_label = ROUND_FILES[rn]
        parts.append(gate(rn, ROUND_FILES[rn][2].split("–")[0].strip() if "–" in ROUND_FILES[rn][2] else ROUND_FILES[rn][2]))
        parts.append("")
        parts.append(f"## {3 + rn}. {title}")
        parts.append(f"*In-game time: {time_label}*")
        parts.append("")
        parts.append(extract_round_sections(rn, keywords))
        parts.append("")

    return "\n".join(parts).rstrip() + "\n"


def main():
    for c in CHARACTERS:
        packet = build_packet(*c)
        out_path = OUT / f"{c[0]}.md"
        out_path.write_text(packet)
        print(f"Wrote {out_path.relative_to(ROOT)} ({len(packet)} chars)")


if __name__ == "__main__":
    main()
