#!/usr/bin/env python3
"""Store a chat summary in the knowledge_base filesystem.

Usage:
  python scripts/store_chat.py \
    --topic ai \
    --title "RAG planning" \
    --summary "Defined chunking and retrieval plan" \
    --keywords rag retrieval embeddings
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / "knowledge_base"
CHAT_INDEX_PATH = KB / "chats" / "index" / "chat_manifest.json"


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "chat"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Store chat data in knowledge_base/chats")
    parser.add_argument("--topic", required=True, help="Primary chat topic (e.g. ai, finance, legal)")
    parser.add_argument("--title", required=True, help="Short chat title")
    parser.add_argument("--summary", required=True, help="1-3 sentence chat summary")
    parser.add_argument("--keywords", nargs="*", default=[], help="Optional keyword list")
    parser.add_argument("--source-files", nargs="*", default=[], help="Optional related file paths")
    parser.add_argument("--next-actions", nargs="*", default=[], help="Optional next action list")
    return parser


def ensure_index() -> dict:
    if CHAT_INDEX_PATH.exists():
        return json.loads(CHAT_INDEX_PATH.read_text())

    data = {"version": 1, "generated_at": "", "records": []}
    CHAT_INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    CHAT_INDEX_PATH.write_text(json.dumps(data, indent=2) + "\n")
    return data


def next_chat_id(records: list[dict]) -> str:
    if not records:
        return "chat_000001"
    last_num = max(int(record["id"].split("_")[1]) for record in records)
    return f"chat_{last_num + 1:06d}"


def store_chat(args: argparse.Namespace) -> tuple[Path, dict]:
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    year = now.strftime("%Y")
    month = now.strftime("%m")

    index = ensure_index()
    records = index["records"]
    chat_id = next_chat_id(records)

    slug = slugify(args.title)
    filename = f"{date_str}__{args.topic}__{slug}__v1.md"

    topic_dir = KB / "chats" / "by-topic" / args.topic
    date_dir = KB / "chats" / "by-date" / year / month
    topic_dir.mkdir(parents=True, exist_ok=True)
    date_dir.mkdir(parents=True, exist_ok=True)

    topic_path = topic_dir / filename
    date_path = date_dir / filename

    body = [
        f"# {args.title}",
        "",
        f"- Chat ID: `{chat_id}`",
        f"- Date (UTC): `{date_str}`",
        f"- Topic: `{args.topic}`",
        f"- Keywords: `{', '.join(args.keywords) if args.keywords else 'none'}`",
        "",
        "## Summary",
        args.summary,
        "",
        "## Source Files",
    ]

    if args.source_files:
        body.extend([f"- `{path}`" for path in args.source_files])
    else:
        body.append("- none")

    body.append("")
    body.append("## Next Actions")

    if args.next_actions:
        body.extend([f"- {action}" for action in args.next_actions])
    else:
        body.append("- none")

    body.append("")

    content = "\n".join(body)
    topic_path.write_text(content)
    date_path.write_text(content)

    record = {
        "id": chat_id,
        "title": args.title,
        "topic": args.topic,
        "date": date_str,
        "keywords": args.keywords,
        "summary": args.summary,
        "topic_path": str(topic_path.relative_to(KB)),
        "date_path": str(date_path.relative_to(KB)),
        "source_files": args.source_files,
    }

    records.append(record)
    index["generated_at"] = now.isoformat()
    CHAT_INDEX_PATH.write_text(json.dumps(index, indent=2) + "\n")

    return topic_path, record


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    path, record = store_chat(args)
    print(f"Stored {record['id']} at {path.relative_to(ROOT)}")

    review_script = ROOT / "scripts" / "review_organization.py"
    if review_script.exists():
        subprocess.run(["python3", str(review_script)], check=False)


if __name__ == "__main__":
    main()
