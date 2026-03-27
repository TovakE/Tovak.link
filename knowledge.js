async function loadJson(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load ${path}`);
  return res.json();
}

function renderItems(el, rows, render) {
  if (!rows.length) {
    el.innerHTML = '<p class="hint">No entries found.</p>';
    return;
  }
  el.innerHTML = rows.map(render).join('');
}

function esc(v = '') {
  return String(v)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;');
}

async function loadReview() {
  const el = document.querySelector('#review-content');
  try {
    const res = await fetch('knowledge_base/notes/summaries/latest-organization-review.md');
    el.textContent = await res.text();
  } catch {
    el.textContent = 'Review file unavailable. Run: python3 scripts/review_organization.py';
  }
}

async function init() {
  const docsEl = document.querySelector('#docs-list');
  const chatsEl = document.querySelector('#chats-list');
  const overlapEl = document.querySelector('#overlap-list');

  try {
    const [docs, chats, overlaps] = await Promise.all([
      loadJson('knowledge_base/index/manifest.json'),
      loadJson('knowledge_base/chats/index/chat_manifest.json'),
      loadJson('knowledge_base/index/overlaps.json').catch(() => ({ records: [] })),
    ]);

    renderItems(docsEl, docs.records || [], (d) => `
      <article class="item">
        <h3>${esc(d.title)}</h3>
        <div class="meta">${esc(d.id)} • topic: ${esc(d.topic)} • type: ${esc(d.file_type)}</div>
        <p>${esc(d.summary || '')}</p>
        <a href="knowledge_base/${esc(d.path)}" target="_blank" rel="noopener">Open note</a>
      </article>
    `);

    renderItems(chatsEl, chats.records || [], (c) => `
      <article class="item">
        <h3>${esc(c.title)}</h3>
        <div class="meta">${esc(c.id)} • topic: ${esc(c.topic)} • date: ${esc(c.date)}</div>
        <p>${esc(c.summary || '')}</p>
        <a href="knowledge_base/${esc(c.topic_path)}" target="_blank" rel="noopener">Open chat summary</a>
      </article>
    `);

    renderItems(overlapEl, (overlaps.records || []).slice(0, 25), (o) => `
      <article class="item">
        <h3>Score ${esc(o.score)}</h3>
        <div>${esc(o.left.id)} (${esc(o.left.topic)}) ↔ ${esc(o.right.id)} (${esc(o.right.topic)})</div>
        <div class="meta">Signals: ${esc((o.signals || []).join(', '))}</div>
      </article>
    `);
  } catch (err) {
    docsEl.innerHTML = `<p class="hint">Error: ${esc(err.message)}</p>`;
    chatsEl.innerHTML = '<p class="hint">Could not load chat records.</p>';
    overlapEl.innerHTML = '<p class="hint">Could not load overlap records.</p>';
  }

  loadReview();
}

init();
