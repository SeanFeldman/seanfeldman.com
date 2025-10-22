from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List
import json
from slugify import slugify
import xml.etree.ElementTree as ET


@dataclass
class Post:
    title: str | None
    slug: str | None
    body_html: str | None
    created: datetime | str | None
    updated: datetime | str | None
    published: bool
    tags: List[str]
    categories: List[str]
    author: str | None
    id: str | None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "slug": self.slug,
            "body_html": self.body_html,
            "created": self.created,
            "updated": self.updated,
            "published": self.published,
            "tags": self.tags,
            "categories": self.categories,
            "author": self.author,
            "id": self.id,
        }


# Public API

def parse_export(path: Path, fmt: str = "auto") -> List[Dict[str, Any]]:
    """Parse an Orchard export file (XML or JSON) and return list of post dicts.

    Currently implements XML (Orchard 1.x). JSON is reserved for future extension.
    """
    if fmt not in {"auto", "xml", "json"}:
        raise ValueError("fmt must be 'auto', 'xml', or 'json'")

    if fmt == "json" or (fmt == "auto" and path.suffix.lower() == ".json"):
        # Placeholder for Orchard Core JSON parsing
        with path.open("r", encoding="utf-8") as f:
            _ = json.load(f)
        raise NotImplementedError("JSON export parsing is not implemented yet.")

    # Default to XML
    return _parse_xml(path)


# Helpers


def _text_or_none(node) -> str | None:
    if node is None:
        return None
    text = node.text or ""
    return text.strip() or None


def _bool_from_text(value: str | None) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"true", "1", "yes"}


def _find_first(elem, paths: Iterable[str]):
    for p in paths:
        found = elem.find(p)
        if found is not None:
            return found
    return None


def _parse_date(text: str | None) -> datetime | str | None:
    if not text:
        return None
    t = text.strip()
    # Attempt to parse common ISO forms; if fail, return original string
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            return datetime.strptime(t, fmt)
        except Exception:
            pass
    try:
        # fromisoformat needs offset; handle trailing Z
        return datetime.fromisoformat(t.replace("Z", "+00:00"))
    except Exception:
        return t


def _parse_xml(path: Path) -> List[Dict[str, Any]]:
    tree = ET.parse(str(path))
    root = tree.getroot()

    # Try a few likely containers for content items
    containers = []
    for tag in ("Data", "Orchard", "Root", "Export"):
        containers.extend(root.findall(f".//{tag}"))
    containers.append(root)

    items = []

    def looks_like_blogpost(elem) -> bool:
        # Heuristics for Orchard 1.x BlogPost
        content_type = _text_or_none(elem.find("ContentType")) or _text_or_none(elem.find("Type"))
        if content_type and content_type.lower() == "blogpost":
            return True
        # Fallback: has BodyPart/Text and a Title-ish field
        has_body = elem.find(".//BodyPart") is not None
        has_title = (
            elem.find(".//TitlePart") is not None or _text_or_none(elem.find("DisplayText")) is not None
        )
        return has_body and has_title

    # Collect candidate elements that look like a content item
    candidates = root.findall(".//ContentItem")
    if not candidates:
        # Some exports may nest BlogPost elements directly
        candidates = root.findall(".//BlogPost")

    # If still empty, scan broadly under containers
    if not candidates:
        for c in containers:
            candidates.extend(c.findall(".//*"))

    for elem in candidates:
        if not looks_like_blogpost(elem):
            continue

        title = _text_or_none(elem.find("DisplayText"))
        if title is None:
            tp = elem.find("TitlePart")
            if tp is not None:
                title = tp.get("Title") or _text_or_none(tp.find("Title")) or _text_or_none(tp.find("PartTitle"))

        # Slug/Path
        slug = None
        ar = elem.find("AutoroutePart")
        if ar is not None:
            slug = ar.get("Alias") or ar.get("Path") or ar.get("Slug")
            if not slug:
                slug = _text_or_none(ar.find("Path")) or _text_or_none(ar.find("Slug"))
        if not slug and title:
            slug = slugify(title)

        # Body HTML
        body_html = None
        bp = elem.find("BodyPart")
        if bp is not None:
            # Try attribute first (common in exports), then child element
            body_html = bp.get("Text") or bp.get("Html")
            if not body_html:
                body_html = _text_or_none(bp.find("Text")) or _text_or_none(bp.find("Html"))

        # Dates and flags
        created = None
        updated = None
        published = False
        cp = elem.find("CommonPart")
        if cp is not None:
            created = _parse_date(cp.get("CreatedUtc") or _text_or_none(cp.find("CreatedUtc")))
            updated = _parse_date(cp.get("ModifiedUtc") or cp.get("UpdatedUtc") or _text_or_none(cp.find("ModifiedUtc")) or _text_or_none(cp.find("UpdatedUtc")))
            # Post is published if it has a PublishedUtc date
            published_date_str = cp.get("PublishedUtc") or _text_or_none(cp.find("PublishedUtc"))
            published = bool(published_date_str)

        # Author
        author = None
        if cp is not None:
            author = cp.get("Owner") or cp.get("Author") or _text_or_none(cp.find("Owner")) or _text_or_none(cp.find("Author"))
            # Clean up author format from "/User.UserName=sfeldman" to "Sean Feldman"
            if author and author.startswith("/User.UserName="):
                username = author.replace("/User.UserName=", "")
                if username == "sfeldman":
                    author = "Sean Feldman"

        # Tags
        tags: List[str] = []
        tp = elem.find("TagsPart")
        if tp is not None:
            tags_attr = tp.get("Tags")
            if tags_attr:
                # Tags stored as comma-separated string in attribute
                tags = [t.strip() for t in tags_attr.split(",") if t.strip()]
            else:
                # Tags stored as child elements
                for t in tp.findall(".//Tag"):
                    tx = _text_or_none(t)
                    if tx:
                        tags.append(tx)

        # Categories (if present in some setups)
        categories: List[str] = []
        catp = elem.find("CategoriesPart")
        if catp is not None:
            for t in catp.findall(".//Category"):
                tx = _text_or_none(t)
                if tx:
                    categories.append(tx)

        # Id
        cid = elem.get("Id") or _text_or_none(elem.find("Id"))

        post = Post(
            title=title,
            slug=slug,
            body_html=body_html,
            created=created,
            updated=updated,
            published=published,
            tags=tags,
            categories=categories,
            author=author,
            id=cid,
        )
        items.append(post.as_dict())

    return items
