# Deployment Guide (GitHub Pages + Cloudflare)

This repo is a static site (`index.html`, `knowledge.html`, css/js/json files), so GitHub Pages + Cloudflare is a good fit.

## 1) GitHub setup

Repo reference: `https://github.com/TovakE/tovak.link/tree/main`

Choose one Pages mode:

### Mode A (current repo default): GitHub Actions

1. Push this repo to GitHub.
2. In **Settings → Pages**:
   - **Build and deployment**: `GitHub Actions`.
3. Ensure your default branch is `main` (workflow deploys on pushes to `main`).
4. Keep `CNAME` in the repo root set to your domain (currently `tovak.net`).

Workflow file used:
- `.github/workflows/deploy-pages.yml`

### Mode B (branch deploy): Deploy from branch `main` `/ (root)`

If you switched Pages to branch deploy, use:

1. In **Settings → Pages**, set **Source** to `Deploy from a branch`.
2. Select branch `main` and folder `/ (root)`.
3. Save and wait for GitHub to publish.
4. Keep `CNAME` in the repo root set to `tovak.net`.

After first successful run, GitHub will publish at:
- `https://<username>.github.io/<repo>` (project URL)
- and custom domain once DNS is configured.

## 2) Cloudflare DNS setup

In Cloudflare DNS for your domain (`tovak.net`):

### Apex/root domain (`tovak.net`)
Use one of these methods:

- **Recommended:** CNAME flattening
  - Type: `CNAME`
  - Name: `@`
  - Target: `<username>.github.io`
  - Proxy status: start with **DNS only** (grey cloud)

### `www` subdomain (`www.tovak.net`)
- Type: `CNAME`
- Name: `www`
- Target: `<username>.github.io`
- Proxy status: **DNS only** first

## 3) GitHub custom domain settings

In **GitHub → Settings → Pages**:
1. Set **Custom domain** to `tovak.net`.
2. Save and wait for DNS check to pass.
3. Enable **Enforce HTTPS** after certificate provisioning completes.

## 4) Cloudflare SSL/TLS settings

In Cloudflare:
- SSL/TLS mode: **Full** (or **Full (strict)** once stable).
- Always Use HTTPS: enabled.
- If you see redirect loops, temporarily set DNS records to **DNS only** and retest.

## 5) Verification checklist

- `CNAME` file in repo root matches production domain.
- GitHub Actions workflow run succeeded.
- GitHub Pages custom domain shows “DNS check successful”.
- `https://tovak.net` loads site.
- `https://www.tovak.net` redirects (optional, configure in Cloudflare Rules).
- `https://tovak.link` redirects to `https://tovak.net` via `canonical.js`.

## 6) Common issues

- **404 on custom domain**: DNS not propagated or wrong target (`<username>.github.io` mismatch).
- **SSL pending too long**: wait for DNS propagation; keep records DNS-only first.
- **Old content**: Cloudflare cache; purge cache once after first deploy.

## 7) Updating content

1. Commit changes.
2. Push to `main`.
3. GitHub Pages workflow deploys automatically.
4. If needed: Purge Cloudflare cache.
