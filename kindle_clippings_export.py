#!/usr/bin/env python3
"""
Parse Kindle My Clippings.txt, filter by title substrings, and export LLM-friendly files.

Example:
  python kindle_clippings_export.py \
    --input "My Clippings.txt" \
    --match "Atomic Habits" "Deep Work" \
    --out-prefix kindle_export
"""

import argparse
import csv
import json
import re
from pathlib import Path


ENTRY_SEPARATOR = "=========="

META_RE = re.compile(
    r"- Your (?P<kind>Highlight|Note|Bookmark)"
    r"(?: on page (?P<page>\d+))?"
    r"(?: \| Location (?P<location>[\d,-]+))?"
    r".*?\| Added on (?P<added>.+)$",
    re.IGNORECASE,
)


def parse_title_author(line: str):
    """
    Parses lines like:
      Book Title (Author Name)
    Returns:
      (title, author)
    """
    line = line.strip()
    match = re.match(r"^(?P<title>.+?)\s+\((?P<author>[^()]*)\)$", line)
    if match:
        return match.group("title").strip(), match.group("author").strip()
    return line, ""


def parse_entry(raw_entry: str):
    lines = [line.rstrip("\ufeff\r") for line in raw_entry.strip().splitlines()]

    if len(lines) < 2:
        return None

    title, author = parse_title_author(lines[0])
    meta_line = lines[1].strip()

    meta_match = META_RE.match(meta_line)

    kind = ""
    page = ""
    location = ""
    added = ""

    if meta_match:
        kind = meta_match.group("kind").lower()
        page = meta_match.group("page") or ""
        location = meta_match.group("location") or ""
        added = meta_match.group("added") or ""

    text = "\n".join(lines[2:]).strip()

    # Bookmarks often have no body text; skip them by default later.
    return {
        "title": title,
        "author": author,
        "kind": kind,
        "page": page,
        "location": location,
        "added": added,
        "text": text,
        "raw": raw_entry.strip(),
    }


def parse_clippings(path: Path):
    content = path.read_text(encoding="utf-8-sig", errors="replace")
    raw_entries = content.split(ENTRY_SEPARATOR)

    entries = []
    for raw in raw_entries:
        parsed = parse_entry(raw)
        if parsed:
            entries.append(parsed)

    return entries


def title_matches(title: str, match_strings, case_sensitive=False):
    haystack = title if case_sensitive else title.lower()

    for s in match_strings:
        needle = s if case_sensitive else s.lower()
        if needle in haystack:
            return True

    return False


def export_jsonl(entries, path: Path):
    with path.open("w", encoding="utf-8") as f:
        for entry in entries:
            clean_entry = {k: v for k, v in entry.items() if k != "raw"}
            f.write(json.dumps(clean_entry, ensure_ascii=False) + "\n")


def export_csv(entries, path: Path):
    fieldnames = [
        "title",
        "author",
        "kind",
        "page",
        "location",
        "added",
        "text",
    ]

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for entry in entries:
            writer.writerow({field: entry.get(field, "") for field in fieldnames})


def export_txt(entries, path: Path):
    """
    Export only the 'text' field, one entry per line.
    Newlines inside entries are replaced with spaces.
    """
    with path.open("w", encoding="utf-8") as f:
        for entry in entries:
            text = entry.get("text", "").strip()

            if not text:
                continue

            # Flatten multiline highlights into one line
            text = re.sub(r"\s+", " ", text)

            f.write(text + "\n")

def export_markdown(entries, path: Path):
    grouped = {}

    for entry in entries:
        key = (entry["title"], entry["author"])
        grouped.setdefault(key, []).append(entry)

    with path.open("w", encoding="utf-8") as f:
        for (title, author), book_entries in grouped.items():
            f.write(f"# {title}\n\n")
            if author:
                f.write(f"**Author:** {author}\n\n")

            for i, entry in enumerate(book_entries, start=1):
                loc = f"Location {entry['location']}" if entry["location"] else ""
                page = f"Page {entry['page']}" if entry["page"] else ""
                metadata = " | ".join(x for x in [entry["kind"], page, loc, entry["added"]] if x)

                f.write(f"## Clipping {i}\n\n")
                if metadata:
                    f.write(f"*{metadata}*\n\n")

                f.write(entry["text"].strip() + "\n\n")


def main():
    parser = argparse.ArgumentParser(
        description="Filter Kindle clippings by title substring and export JSONL/CSV/Markdown."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Path to Kindle My Clippings.txt",
    )

    parser.add_argument(
        "--match",
        nargs="+",
        required=True,
        help="One or more substrings to match in book titles.",
    )

    parser.add_argument(
        "--out-prefix",
        default="kindle_clippings_export",
        help="Output filename prefix.",
    )

    parser.add_argument(
        "--case-sensitive",
        action="store_true",
        help="Use case-sensitive title matching.",
    )

    parser.add_argument(
        "--include-bookmarks",
        action="store_true",
        help="Include bookmarks. By default, bookmarks are skipped.",
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    entries = parse_clippings(input_path)

    filtered = [
        entry
        for entry in entries
        if title_matches(entry["title"], args.match, args.case_sensitive)
    ]

    if not args.include_bookmarks:
        filtered = [
            entry
            for entry in filtered
            if entry["kind"] != "bookmark" and entry["text"].strip()
        ]

    out_prefix = Path(args.out_prefix)

    export_jsonl(filtered, out_prefix.with_suffix(".jsonl"))
    export_csv(filtered, out_prefix.with_suffix(".csv"))
    export_markdown(filtered, out_prefix.with_suffix(".md"))
    export_txt(filtered, out_prefix.with_suffix(".txt"))

    print(f"Parsed entries: {len(entries)}")
    print(f"Matched entries: {len(filtered)}")
    print(f"Wrote:")
    print(f"  {out_prefix.with_suffix('.jsonl')}")
    print(f"  {out_prefix.with_suffix('.csv')}")
    print(f"  {out_prefix.with_suffix('.md')}")
    print(f"  {out_prefix.with_suffix('.txt')}")

if __name__ == "__main__":
    main()