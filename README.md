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
  cache/
    knowledge_cache.json               # single browser/reference cache file
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



### See exactly what is stored

Use this command to print an inventory of currently saved docs, chats, and overlap links from the unified cache:

```bash
python3 scripts/show_stored.py
```

### Browser access for accrued notes

Open `knowledge.html` in the browser to directly access notes from one reference file:

- `knowledge_base/cache/knowledge_cache.json` (includes docs, chats in date/id order, overlaps, and latest review text)

### Automatic organization re-check after each stored chat

`python3 scripts/store_chat.py ...` now triggers `scripts/review_organization.py` automatically, which refreshes:

- `knowledge_base/index/overlaps.json`
- `knowledge_base/notes/summaries/latest-organization-review.md`


### Unified cache workflow

Run this command to rebuild the single cache file manually:

```bash
python3 scripts/build_cache.py
```

`python3 scripts/store_chat.py ...` now refreshes overlap/review and then rebuilds `knowledge_base/cache/knowledge_cache.json`, so the browser can reference one file at all times.


## Site deployment

For step-by-step GitHub Pages + Cloudflare domain setup, see [`DEPLOYMENT.md`](DEPLOYMENT.md).
- Quick copy/paste for your domain: [`DEPLOY_CHECKLIST_TOVAK.md`](DEPLOY_CHECKLIST_TOVAK.md).
- Canonical domain behavior: `canonical.js` redirects legacy hosts (`tovak.link`, `www.tovak.link`, `www.tovak.net`) to `https://tovak.net`.
- Repo target for deployment: `https://github.com/TovakE/tovak.link/tree/main` (supports either GitHub Actions or branch deploy from `main` `/root`).

## Jekyll vs static pages

Use a **plain static page** setup for this repository (recommended).

- It is simpler for JSON-driven pages like `knowledge.html`.
- There is no Ruby/Jekyll build dependency to manage.
- GitHub Pages can deploy directly from the GitHub Actions workflow in this repo.

This repo includes `.nojekyll` to keep Pages in static mode.
