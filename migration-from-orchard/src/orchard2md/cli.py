from __future__ import annotations

import argparse
import sys
from pathlib import Path
from datetime import datetime

from .parser import parse_export
from .convert import convert_html_to_markdown
from .writer import write_post_file


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="orchard2md",
        description="Convert Orchard CMS export to Markdown files",
    )
    p.add_argument("--input", required=True, help="Path to Orchard export file (XML/JSON)")
    p.add_argument("--out-dir", default="out", help="Directory for generated Markdown files")
    p.add_argument(
        "--name-template",
        default="{date}-{slug}.md",
        help="File name template; available tokens: {date}, {slug}, {title}",
    )
    p.add_argument("--format", choices=["auto", "xml", "json"], default="auto")
    p.add_argument(
        "--drafts",
        action="store_true",
        help="Include drafts/unpublished posts",
    )
    p.add_argument(
        "--assets-dir",
        default=None,
        help="Optional assets directory (reserved; no copying yet)",
    )
    p.add_argument("--dry-run", action="store_true", help="Preview actions without writing files")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input file not found: {input_path}", file=sys.stderr)
        return 2

    posts = parse_export(input_path, fmt=args.format)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = 0
    skipped = 0

    for post in posts:
        # Filter drafts by default
        is_published = bool(post.get("published", False))
        if not args.drafts and not is_published:
            skipped += 1
            continue
        
        # Mark all posts as published (not draft)
        post["published"] = True

        html = post.get("body_html") or ""
        md = convert_html_to_markdown(html)

        # Determine date for naming
        created = post.get("created")
        if isinstance(created, str):
            # attempt ISO parse
            try:
                created_dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
            except Exception:
                created_dt = None
        else:
            created_dt = created

        date_for_name = (
            created_dt.strftime("%Y-%m-%d") if isinstance(created_dt, datetime) else "unknown-date"
        )

        file_name = args.name_template.format(
            date=date_for_name,
            slug=post.get("slug") or "no-slug",
            title=post.get("title") or "untitled",
            id=post.get("id") or "",
        )

        if args.dry_run:
            print(f"Would write: {file_name}")
            written += 1
            continue

        write_post_file(out_dir, file_name, post, md)
        written += 1

    if args.dry_run:
        print(f"[Dry-run] Posts considered: {len(posts)}, would write: {written}, skipped: {skipped}")
    else:
        print(f"Posts processed: {len(posts)}, written: {written}, skipped: {skipped}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
