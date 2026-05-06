#!/usr/bin/env python3
"""Revise dossiers to match the new template.

Strips round cards (sections 4-7) and the duplicate Props block,
reformats the header, and merges the role line into Who You Are.
"""
import re
import sys
from pathlib import Path

DOSSIERS_DIR = Path(__file__).parent / "dossiers"


def transform(content: str) -> str:
    lines = content.split("\n")

    # Find the cutoff for round cards / duplicate Props.
    # Cut at the first of:
    #   - duplicate "## Your Props" (second occurrence)
    #   - "## ⛔ STOP" line
    #   - "## 4. Round 1" (or any "## N. Round")
    cut_idx = None
    seen_props = False
    for i, line in enumerate(lines):
        if line.startswith("## Your Props"):
            if seen_props:
                cut_idx = i
                break
            seen_props = True
            continue
        if line.startswith("## ⛔") or re.match(r"^## \d+\. Round", line):
            cut_idx = i
            break

    if cut_idx is not None:
        # Back up over preceding --- and blank lines so we don't leave a dangling rule.
        while cut_idx > 0 and lines[cut_idx - 1].strip() in ("", "---"):
            cut_idx -= 1
        lines = lines[:cut_idx]

    content = "\n".join(lines).rstrip() + "\n"

    # Header: "# YOUR GAME PACKET — Name" + "## Dirty Laundry..." -> "# Name Game Packet"
    content = re.sub(
        r"^# YOUR GAME PACKET — (.+?)\n## Dirty Laundry: Murder in the Caymans\n",
        r"# \1 Game Packet\n",
        content,
    )

    # Callout: drop "DO NOT READ AHEAD" line, simplify "READ BEFORE THE PARTY"
    content = re.sub(
        r"> \*\*READ BEFORE THE PARTY:\*\*[^\n]*\n> \*\*DO NOT READ AHEAD:\*\*[^\n]*\n",
        r"> **READ BEFORE THE PARTY**\n",
        content,
    )

    # Section 3: merge role line + "## Who You Are" header into "**Who You Are:** ROLE"
    content = re.sub(
        r"(## 3\. Your Character\n\n)\*\*([^*]+)\*\*\n\n---\n\n## Who You Are\n",
        r"\1**Who You Are:** \2\n",
        content,
    )
    # Fallback: dossiers without a "## Who You Are" header (e.g., the Ghost) still
    # have the bolded role line + a trailing "---". Convert that to the same format.
    content = re.sub(
        r"(## 3\. Your Character\n\n)\*\*([^*]+)\*\*\n\n---\n",
        r"\1**Who You Are:** \2\n",
        content,
    )

    # Drop the trailing duplicate "## Your Props" block (redundant with section 2).
    # Must run BEFORE the h2->h3 demotion so the literal "## Your Props" still matches.
    new_lines = content.split("\n")
    for i in range(len(new_lines) - 1, -1, -1):
        if new_lines[i].strip() == "## Your Props":
            new_lines = new_lines[:i]
            while new_lines and new_lines[-1].strip() in ("", "---"):
                new_lines.pop()
            break
    content = "\n".join(new_lines).rstrip() + "\n"

    # Demote every h2 that appears AFTER "## 3. Your Character" to h3 — those
    # are subsections of section 3 (varies by character: Suspects have Secrets/
    # Alibi/Connections; minor chars have What You Know / Questions / etc.).
    parts = content.split("## 3. Your Character", 1)
    if len(parts) == 2:
        head, tail = parts
        tail = re.sub(r"^## (?!\d+\. )", "### ", tail, flags=re.MULTILINE)
        content = head + "## 3. Your Character" + tail

    return content


def main() -> int:
    targets = sorted(DOSSIERS_DIR.glob("*.md"))
    if not targets:
        print(f"No dossiers found in {DOSSIERS_DIR}", file=sys.stderr)
        return 1
    for f in targets:
        new = transform(f.read_text())
        f.write_text(new)
        print(f"Revised: {f.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
