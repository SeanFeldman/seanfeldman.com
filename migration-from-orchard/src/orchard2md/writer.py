from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List
import yaml


def _serialize_date(value: Any) -> str | None:
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, str):
        # Assume ISO-ish already
        return value
    return None


def render_front_matter(post: Dict[str, Any]) -> str:
    front: Dict[str, Any] = {
        "title": post.get("title"),
        "slug": post.get("slug"),
        "date": _serialize_date(post.get("created")),
        "updated": _serialize_date(post.get("updated")),
        "draft": not bool(post.get("published", False)),
    }

    tags = post.get("tags") or []
    categories = post.get("categories") or []
    author = post.get("author")

    if tags:
        front["tags"] = list(tags)
    if categories:
        front["categories"] = list(categories)
    if author:
        front["author"] = author

    # Remove None values
    front = {k: v for k, v in front.items() if v is not None}

    yaml_text = yaml.safe_dump(front, sort_keys=False, allow_unicode=True).strip()
    # Do not include a trailing newline after the closing delimiter; writer adds spacing
    return f"---\n{yaml_text}\n---"


def write_post_file(out_dir: Path, file_name: str, post: Dict[str, Any], body_md: str) -> Path:
    out_path = out_dir / file_name
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Ensure uniqueness if a file with the same name already exists
    if out_path.exists():
        stem = out_path.stem
        suffix = out_path.suffix or ".md"
        i = 1
        candidate = out_path
        while candidate.exists():
            candidate = out_path.with_name(f"{stem}-{i}{suffix}")
            i += 1
        out_path = candidate

    fm = render_front_matter(post)

    with out_path.open("w", encoding="utf-8") as f:
        f.write(fm)
        f.write("\n")
        f.write(body_md or "")
        f.write("\n")

    return out_path
