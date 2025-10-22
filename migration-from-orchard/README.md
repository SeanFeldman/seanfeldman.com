# orchard2md

Convert Orchard CMS exported data to Markdown, one file per BlogPost, with YAML front matter.

## Features
- Parses Orchard CMS 1.x XML export (auto-detect format). JSON support planned.
- Extracts title, slug, content (HTML→Markdown), created/updated, published, tags/categories, author.
- Writes one Markdown file per post using a configurable name template (default `{date}-{slug}.md`).
- YAML front matter for static site generators (Jekyll/Hugo/etc.).

## Requirements
- Python 3.9+
- Windows PowerShell (commands below are for PowerShell)

## Quick start (PowerShell)
```powershell
# Create and activate a virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Run against your Orchard export
python -m orchard2md --input path\to\export.xml --out-dir .\out

# Options
python -m orchard2md --help
```

## CLI options
- `--input` Path to Orchard export file (XML). Required.
- `--out-dir` Output directory for Markdown files. Defaults to `./out`.
- `--name-template` File name template, defaults to `{date}-{slug}.md`.
- `--format` Force format: `xml` or `json` (default: auto).
- `--drafts` Include unpublished/draft posts (default: false).
- `--assets-dir` Optional path for assets (reserved; no copying yet).
- `--dry-run` Preview what would be generated without writing files.

## Example fixture
A tiny sample XML is provided at `examples/fixtures/sample_orchard.xml`.

## Notes
- The XML schema can vary by Orchard version and modules. The parser aims to be tolerant; if your export varies, open an issue or share a sample.
- JSON (Orchard Core) support can be added later.

## Tests
```powershell
# From project root
.\.venv\Scripts\Activate.ps1
pytest
```

## License
MIT
