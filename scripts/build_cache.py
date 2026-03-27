#!/usr/bin/env python3
"""Build one ordered cache file for all saved knowledge base data."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
CACHE_DIR = KB / "cache"
CACHE_PATH = CACHE_DIR / "knowledge_cache.json"

DOC_MANIFEST = KB / "index" / "manifest.json"
CHAT_MANIFEST = KB / "chats" / "index" / "chat_manifest.json"
OVERLAPS_PATH = KB / "index" / "overlaps.json"
REVIEW_PATH = KB / "notes" / "summaries" / "latest-organization-review.md"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def main() -> None:
    docs_data = read_json(DOC_MANIFEST)
    chats_data = read_json(CHAT_MANIFEST)
    overlaps_data = read_json(OVERLAPS_PATH)
    review_text = REVIEW_PATH.read_text() if REVIEW_PATH.exists() else ""

    chats = chats_data.get("records", [])
    chats_sorted = sorted(chats, key=lambda row: (row.get("date", ""), row.get("id", "")))

    payload = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "reference": {
            "cache_file": str(CACHE_PATH.relative_to(ROOT)),
            "note": "Use this file as the primary browser reference for saved knowledge data.",
        },
        "docs": docs_data.get("records", []),
        "chats": chats_sorted,
        "overlaps": overlaps_data.get("records", []),
        "review_text": review_text,
    }

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(payload, indent=2) + "\n")
    print(f"Wrote {CACHE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
