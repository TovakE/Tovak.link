# Canonical domain redirect to tovak.net

- Chat ID: `chat_000007`
- Date (UTC): `2026-03-27`
- Topic: `operations`
- Keywords: `domain, redirect, tovak.net, cloudflare, pages`

## Summary
Added canonical host redirect logic so legacy tovak.link hosts route to https://tovak.net and updated deployment docs/checklist.

## Source Files
- `canonical.js`
- `index.html`
- `knowledge.html`
- `README.md`
- `DEPLOYMENT.md`
- `DEPLOY_CHECKLIST_TOVAK.md`

## Next Actions
- Redeploy GitHub Pages from main
- Verify curl -I https://tovak.link returns redirect to https://tovak.net
