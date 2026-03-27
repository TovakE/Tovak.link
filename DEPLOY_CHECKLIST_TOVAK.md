# Copy/Paste Checklist for `tovak.net` (GitHub Pages + Cloudflare)

Use this exactly, top to bottom.

## 0) Set your variables

```bash
export GH_USER="TovakE"
export GH_REPO="tovak.link"
export DOMAIN="tovak.net"
export WWW_DOMAIN="www.tovak.net"
```

## 1) Push site to GitHub and trigger deploy

```bash
git checkout main
git pull
git add .
git commit -m "Deploy site updates" || true
git push origin main
```

> The repo already contains a Pages workflow at `.github/workflows/deploy-pages.yml`.

## 1b) If you deploy from branch `main` instead of Actions

In GitHub Pages settings (`https://github.com/$GH_USER/$GH_REPO/settings/pages`):

1. Source: **Deploy from a branch**
2. Branch: `main`
3. Folder: `/ (root)`
4. Save and wait for publish

## 2) Enable GitHub Pages (UI)

1. Open: `https://github.com/$GH_USER/$GH_REPO/settings/pages`
2. Under **Build and deployment** choose **GitHub Actions**.
3. Wait for workflow run to finish in **Actions** tab.

## 3) Confirm CNAME in repo root

```bash
cat CNAME
```

Expected output:

```text
tovak.net
```

## 4) Add DNS records in Cloudflare (UI quick path)

In Cloudflare DNS for `tovak.net`, add:

1. `CNAME` record
   - Name: `@`
   - Target: `${GH_USER}.github.io`
   - Proxy: **DNS only** (grey cloud)

2. `CNAME` record
   - Name: `www`
   - Target: `${GH_USER}.github.io`
   - Proxy: **DNS only**

## 5) Set custom domain in GitHub Pages

1. Open: `https://github.com/$GH_USER/$GH_REPO/settings/pages`
2. In **Custom domain**, enter: `tovak.net`
3. Save.
4. Wait for **DNS check successful**.
5. Turn on **Enforce HTTPS**.

## 6) Cloudflare SSL settings

In Cloudflare:

- SSL/TLS mode: `Full` (or `Full (strict)` once stable)
- Always Use HTTPS: `On`

## 7) Verify live site

```bash
curl -I https://tovak.net
curl -I https://www.tovak.net
curl -I https://tovak.link
```

You should see `HTTP/2 200` (or `301/308` redirect to the canonical URL).

## 8) Optional: Cloudflare API (advanced, fully scriptable)

Only run if you prefer API over UI.

```bash
export CF_API_TOKEN="<cloudflare_api_token>"
export CF_ZONE_ID="<zone_id_for_tovak.net>"

curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"CNAME\",\"name\":\"@\",\"content\":\"${GH_USER}.github.io\",\"proxied\":false}" \
  | jq .

curl -sS -X POST "https://api.cloudflare.com/client/v4/zones/$CF_ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CF_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"CNAME\",\"name\":\"www\",\"content\":\"${GH_USER}.github.io\",\"proxied\":false}" \
  | jq .
```

## 9) If something fails

- If SSL is pending, wait 5–30 minutes and retest.
- If custom domain fails validation, re-check DNS target is exactly `${GH_USER}.github.io`.
- If site looks stale, purge Cloudflare cache once.
- If `tovak.link` still resolves, it is redirected to `https://tovak.net` by `canonical.js`.

## Static mode check (recommended)

```bash
ls -la .nojekyll
```

If `.nojekyll` exists, GitHub Pages will skip Jekyll processing and serve static files directly.
