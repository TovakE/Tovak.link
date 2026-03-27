# Tovak Webpage

## Knowledge Base Filesystem

A structured filesystem is available at `knowledge_base/` to organize uploaded documents, code, and chat knowledge for topic-based retrieval.

### Directory layout

```text
knowledge_base/
  inbox/                               # raw uploads before processing
  docs/
    topic-ai/
    topic-finance/
    topic-legal/
  code/
    python/
    javascript/
    infra/
  notes/
    summaries/
    qa/
  chats/
    by-topic/<topic>/                  # chat summaries grouped by topic
    by-date/YYYY/MM/                   # same chat summaries grouped by time
    index/chat_manifest.json           # chat registry for retrieval
    templates/
      chat_entry.template.md
      chat_record.template.json
  index/
    manifest.json                      # document/code registry
    tags.json                          # topic/tag dictionary
    record.template.json               # metadata schema example
    embeddings/                        # vector index artifacts (optional)
  archive/
    YYYY/                              # old versions or retired files
```

### Naming convention

Use this standard for docs, notes, and chat summaries:

`YYYY-MM-DD__topic__short-title__vN.ext`

Example:

`2026-03-27__ai__rag-design-notes__v1.md`

### Ingestion workflow for uploaded files

1. Add raw uploads to `knowledge_base/inbox/`.
2. Classify each file by content (`docs/` or `code/`) and subject.
3. Move file into target folder using the naming convention.
4. Add/update a record in `knowledge_base/index/manifest.json`.
5. Update `knowledge_base/index/tags.json` for new topics/tags.
6. Move older versions to `knowledge_base/archive/<year>/` when superseded.

### Chat knowledge workflow

Store each meaningful chat in the `knowledge_base/chats/` structure so future answers can be retrieved by topic or date.

Use the helper script:

```bash
python3 scripts/store_chat.py \
  --topic operations \
  --title "Knowledge base chat storage request" \
  --summary "User requested chat-aware storage and retrieval structure." \
  --keywords filesystem chats retrieval \
  --source-files README.md knowledge_base/index/manifest.json \
  --next-actions "Store each future chat summary via script"
```

The script will:

- create a Markdown summary in `chats/by-topic/<topic>/`
- mirror it to `chats/by-date/YYYY/MM/`
- append a structured record to `chats/index/chat_manifest.json`

### Response convention

For repo work, prefer knowledge retrieval in this order:

1. `knowledge_base/chats/index/chat_manifest.json` (past chat context)
2. `knowledge_base/index/manifest.json` (uploaded file registry)
3. `knowledge_base/docs/` and `knowledge_base/code/` topic folders

Use ad-hoc paths only when information is not yet ingested.


### Browser access for accrued notes

Open `knowledge.html` in the browser to directly access:

- indexed documents from `knowledge_base/index/manifest.json`
- indexed chat summaries from `knowledge_base/chats/index/chat_manifest.json`
- overlap signals from `knowledge_base/index/overlaps.json`
- latest organization review from `knowledge_base/notes/summaries/latest-organization-review.md`

### Automatic organization re-check after each stored chat

`python3 scripts/store_chat.py ...` now triggers `scripts/review_organization.py` automatically, which refreshes:

- `knowledge_base/index/overlaps.json`
- `knowledge_base/notes/summaries/latest-organization-review.md`
