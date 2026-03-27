#!/usr/bin/env python3
"""Show what is currently stored in the knowledge base."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
CACHE_PATH = KB / "cache" / "knowledge_cache.json"


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def main() -> None:
    data = read_json(CACHE_PATH)
    docs = data.get("docs", [])
    chats = data.get("chats", [])
    overlaps = data.get("overlaps", [])

    print(f"Cache file: {CACHE_PATH.relative_to(ROOT)}")
    print(f"Generated : {data.get('generated_at', 'unknown')}")
    print()

    print(f"Documents ({len(docs)}):")
    for row in docs:
        print(f"- {row.get('id', '?')} | {row.get('topic', '?')} | {row.get('title', 'untitled')}")

    print()
    print(f"Chats ({len(chats)}):")
    for row in chats:
        print(f"- {row.get('id', '?')} | {row.get('date', '?')} | {row.get('topic', '?')} | {row.get('title', 'untitled')}")

    print()
    print(f"Overlaps ({len(overlaps)}):")
    for row in overlaps[:20]:
        left = row.get("left", {}).get("id", "?")
        right = row.get("right", {}).get("id", "?")
        score = row.get("score", "?")
        print(f"- score={score} | {left} <-> {right}")


if __name__ == "__main__":
    main()
