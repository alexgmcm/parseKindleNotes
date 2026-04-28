# Kindle Clippings Exporter

Export selected Kindle highlights and notes from `My Clippings.txt` into LLM-friendly formats:

* `.jsonl`
* `.csv`
* `.md`
* `.txt`

The script filters clippings by matching one or more strings in the book title.

---

## Getting `My Clippings.txt` from your Kindle

1. Connect your Kindle to your computer using USB.

2. Open the Kindle as an external drive.

3. Go to:

   ```text
   documents/My Clippings.txt
   ```

4. Copy `My Clippings.txt` to your computer.

### Example paths

**macOS:**

```text
/Volumes/Kindle/documents/My Clippings.txt
```

**Windows:**

```text
D:\documents\My Clippings.txt
```

---

## What this file contains

`My Clippings.txt` contains highlights, notes, and bookmarks saved on your Kindle device.

Each entry usually includes:

* book title
* author
* clipping type (highlight, note, bookmark)
* page and/or location
* date added
* clipping text

---

## Installation

This script uses only Python’s standard library.

You need **Python 3.8+**.

Check your version:

```bash
python --version
```

or:

```bash
python3 --version
```

---

## Usage

### Basic example

```bash
python kindle_clippings_export.py \
  --input "My Clippings.txt" \
  --match "Atomic Habits" "Deep Work" \
  --out-prefix reading_notes
```

This will:

* filter clippings from books matching the given strings
* create the following files:

```text
reading_notes.jsonl
reading_notes.csv
reading_notes.md
reading_notes.txt
```

---

## Example using Kindle directly

### macOS

```bash
python kindle_clippings_export.py \
  --input "/Volumes/Kindle/documents/My Clippings.txt" \
  --match "Dune" \
  --out-prefix dune_clippings
```

### Windows (PowerShell)

```powershell
python kindle_clippings_export.py `
  --input "D:\documents\My Clippings.txt" `
  --match "Dune" `
  --out-prefix dune_clippings
```

---

## Output formats

### JSONL (recommended for LLMs)

Each line is a structured JSON object:

```json
{"title":"Atomic Habits","author":"James Clear","kind":"highlight","page":"","location":"1234","added":"Monday, January 1, 2024","text":"You do not rise to the level of your goals..."}
```

Best for:

* embeddings
* pipelines
* structured processing

---

### CSV

Tabular format:

```text
title, author, kind, page, location, added, text
```

Best for:

* Excel / Google Sheets
* manual inspection

---

### Markdown

Grouped by book:

```markdown
# Atomic Habits

## Clipping 1
*highlight | Location 1234*
You do not rise to the level of your goals...
```

Best for:

* reading
* note-taking tools

---

### TXT (LLM-friendly raw text)

One clipping per line, text only:

```text
You do not rise to the level of your goals...
Habits are the compound interest of self-improvement.
Focus is a skill that can be trained.
```

Formatting notes:

* metadata removed
* multiline highlights flattened into a single line

Best for:

* embeddings
* simple prompting
* corpus building

---

## Command-line options

### `--input` (required)

Path to `My Clippings.txt`:

```bash
--input "My Clippings.txt"
```

---

### `--match` (required)

One or more substrings to match in book titles:

```bash
--match "Atomic Habits" "Deep Work"
```

Matching is **case-insensitive by default**.

---

### `--out-prefix` (optional)

Output file prefix.

Default:

```text
kindle_clippings_export
```

Example:

```bash
--out-prefix my_notes
```

Creates:

```text
my_notes.jsonl
my_notes.csv
my_notes.md
my_notes.txt
```

---

### `--case-sensitive` (optional)

Enable case-sensitive title matching:

```bash
--case-sensitive
```

---

### `--include-bookmarks` (optional)

Include bookmarks (normally skipped because they lack text):

```bash
--include-bookmarks
```

---

## Recommended workflow for LLM use

### Best option (structured):

Use `.jsonl`

```text
reading_notes.jsonl
```

### Simplest option (raw text):

Use `.txt`

```text
reading_notes.txt
```

---

## Typical workflow

1. Connect Kindle and copy `My Clippings.txt`
2. Run the script with desired filters
3. Use output in your LLM pipeline

Example:

```bash
python kindle_clippings_export.py \
  --input "My Clippings.txt" \
  --match "The Beginning of Infinity" \
  --out-prefix boi_notes
```

---

## Notes and limitations

* Only includes clippings stored on the Kindle device
* Kindle app highlights may require syncing to device
* Format may vary slightly across Kindle versions
* Duplicate highlights can occur
* Some books may restrict highlight export (publisher limits)

---

## Tips

* Use short, distinctive substrings in `--match` for better filtering
* Combine multiple books in one run
* Prefer `.jsonl` for anything beyond simple text use
* Clean or deduplicate data before embedding if needed

---

## License

Use freely for personal workflows.
