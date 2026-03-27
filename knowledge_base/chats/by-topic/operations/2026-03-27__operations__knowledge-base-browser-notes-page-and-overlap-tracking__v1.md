# Knowledge base browser notes page and overlap tracking

- Chat ID: `chat_000003`
- Date (UTC): `2026-03-27`
- Topic: `operations`
- Keywords: `browser, notes, overlap, organization, review`

## Summary
Added a browser-accessible knowledge page that lists documents/chats and overlap signals, plus automatic organization review updates after chat storage.

## Source Files
- `knowledge.html`
- `knowledge.js`
- `knowledge.css`
- `scripts/review_organization.py`
- `scripts/store_chat.py`
- `knowledge_base/index/manifest.json`
- `knowledge_base/chats/index/chat_manifest.json`

## Next Actions
- Use knowledge.html to open indexed notes from a browser
- Run store_chat.py after meaningful chats to refresh organization review
