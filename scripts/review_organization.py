#!/usr/bin/env python3
"""Review knowledge_base organization and compute overlap between indexed ideas."""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
DOC_MANIFEST = KB / "index" / "manifest.json"
CHAT_MANIFEST = KB / "chats" / "index" / "chat_manifest.json"
OVERLAP_PATH = KB / "index" / "overlaps.json"
REVIEW_PATH = KB / "notes" / "summaries" / "latest-organization-review.md"


def read_json(path: Path) -> dict:
    if not path.exists():
        return {"records": []}
    return json.loads(path.read_text())


def score_overlap(a: dict, b: dict) -> tuple[int, list[str]]:
    features_a = set(a.get("keywords", [])) | set(a.get("tags", []))
    features_b = set(b.get("keywords", [])) | set(b.get("tags", []))
    shared = sorted(features_a & features_b)

    score = len(shared)
    if a.get("topic") == b.get("topic"):
        score += 1
        shared.append("same-topic")
    if b.get("id") in set(a.get("related_files", [])) or a.get("id") in set(b.get("related_files", [])):
        score += 2
        shared.append("related-file-link")

    return score, shared


def build_overlap_records(doc_records: list[dict], chat_records: list[dict]) -> list[dict]:
    unified: list[dict] = []

    for record in doc_records:
        unified.append(
            {
                "id": record.get("id"),
                "title": record.get("title"),
                "topic": record.get("topic"),
                "kind": "doc",
                "keywords": record.get("keywords", []),
                "tags": record.get("tags", []),
                "related_files": record.get("related_files", []),
                "path": record.get("path"),
            }
        )

    for record in chat_records:
        unified.append(
            {
                "id": record.get("id"),
                "title": record.get("title"),
                "topic": record.get("topic"),
                "kind": "chat",
                "keywords": record.get("keywords", []),
                "tags": [],
                "related_files": [],
                "path": record.get("topic_path"),
            }
        )

    overlaps = []
    for a, b in combinations(unified, 2):
        score, signals = score_overlap(a, b)
        if score <= 0:
            continue
        overlaps.append(
            {
                "score": score,
                "signals": signals,
                "left": {"id": a["id"], "title": a["title"], "kind": a["kind"], "topic": a["topic"], "path": a["path"]},
                "right": {"id": b["id"], "title": b["title"], "kind": b["kind"], "topic": b["topic"], "path": b["path"]},
            }
        )

    overlaps.sort(key=lambda item: item["score"], reverse=True)
    return overlaps


def find_organization_issues(doc_records: list[dict], chat_records: list[dict]) -> list[str]:
    issues: list[str] = []

    for record in doc_records:
        path = record.get("path", "")
        topic = record.get("topic", "")
        if topic and f"topic-{topic}" not in path:
            issues.append(f"Document {record.get('id')} topic '{topic}' may not match its folder: {path}")

    seen_titles: dict[str, int] = defaultdict(int)
    for record in chat_records:
        key = f"{record.get('date')}::{record.get('title', '').strip().lower()}"
        seen_titles[key] += 1
    for key, count in seen_titles.items():
        if count > 1:
            issues.append(f"Possible duplicate chat summaries for {key} ({count} entries)")

    return issues


def write_review(doc_records: list[dict], chat_records: list[dict], overlaps: list[dict], issues: list[str]) -> None:
    now = datetime.now(timezone.utc)
    topic_counts: dict[str, int] = defaultdict(int)
    for record in doc_records:
        topic_counts[record.get("topic", "unknown")] += 1

    lines = [
        "# Knowledge Base Organization Review",
        "",
        f"- Generated at (UTC): `{now.isoformat()}`",
        f"- Indexed documents: `{len(doc_records)}`",
        f"- Indexed chats: `{len(chat_records)}`",
        f"- Overlap links found: `{len(overlaps)}`",
        "",
        "## Documents by Topic",
    ]

    if topic_counts:
        for topic, count in sorted(topic_counts.items()):
            lines.append(f"- `{topic}`: {count}")
    else:
        lines.append("- none")

    lines.extend(["", "## Overlapping Ideas (Top 10)"])
    if overlaps:
        for item in overlaps[:10]:
            lines.append(
                f"- ({item['score']}) {item['left']['id']} ↔ {item['right']['id']} | signals: {', '.join(item['signals'])}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Organization Issues"])
    if issues:
        lines.extend([f"- {issue}" for issue in issues])
    else:
        lines.append("- none")

    lines.append("")
    REVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PATH.write_text("\n".join(lines))


def main() -> None:
    docs = read_json(DOC_MANIFEST).get("records", [])
    chats = read_json(CHAT_MANIFEST).get("records", [])

    overlaps = build_overlap_records(docs, chats)
    issues = find_organization_issues(docs, chats)

    OVERLAP_PATH.parent.mkdir(parents=True, exist_ok=True)
    OVERLAP_PATH.write_text(
        json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(), "records": overlaps}, indent=2) + "\n"
    )
    write_review(docs, chats, overlaps, issues)

    print(f"Wrote {OVERLAP_PATH.relative_to(ROOT)} and {REVIEW_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
