. o"""Batch-convert round card markdown files to .docx using pypandoc.

Usage:
    uv run make_round_card_docx.py
"""

from pathlib import Path

import pypandoc

PROJECT_ROOT = Path(__file__).parent
SOURCE_DIR = PROJECT_ROOT / "round cards"
OUTPUT_DIR = PROJECT_ROOT / "docx" / "round cards"


def main() -> None:
    md_files = sorted(SOURCE_DIR.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {SOURCE_DIR}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for md in md_files:
        out = OUTPUT_DIR / f"{md.stem}.docx"
        pypandoc.convert_file(
            str(md),
            to="docx",
            outputfile=str(out),
            extra_args=["--standalone"],
        )
        print(f"  {md.name}  →  {out.relative_to(PROJECT_ROOT)}")

    print(f"\nDone. {len(md_files)} file(s) written to {OUTPUT_DIR.relative_to(PROJECT_ROOT)}/")


if __name__ == "__main__":
    main()
