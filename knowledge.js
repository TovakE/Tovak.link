async function loadCache() {
  const path = 'knowledge_base/cache/knowledge_cache.json';
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

async function init() {
  const docsEl = document.querySelector('#docs-list');
  const chatsEl = document.querySelector('#chats-list');
  const overlapEl = document.querySelector('#overlap-list');
  const reviewEl = document.querySelector('#review-content');

  try {
    const cache = await loadCache();

    renderItems(docsEl, cache.docs || [], (d) => `
      <article class="item">
        <h3>${esc(d.title)}</h3>
        <div class="meta">${esc(d.id)} • topic: ${esc(d.topic)} • type: ${esc(d.file_type)}</div>
        <p>${esc(d.summary || '')}</p>
        <a href="knowledge_base/${esc(d.path)}" target="_blank" rel="noopener">Open note</a>
      </article>
    `);

    renderItems(chatsEl, cache.chats || [], (c) => `
      <article class="item">
        <h3>${esc(c.title)}</h3>
        <div class="meta">${esc(c.id)} • topic: ${esc(c.topic)} • date: ${esc(c.date)}</div>
        <p>${esc(c.summary || '')}</p>
        <a href="knowledge_base/${esc(c.topic_path)}" target="_blank" rel="noopener">Open chat summary</a>
      </article>
    `);

    renderItems(overlapEl, (cache.overlaps || []).slice(0, 25), (o) => `
      <article class="item">
        <h3>Score ${esc(o.score)}</h3>
        <div>${esc(o.left.id)} (${esc(o.left.topic)}) ↔ ${esc(o.right.id)} (${esc(o.right.topic)})</div>
        <div class="meta">Signals: ${esc((o.signals || []).join(', '))}</div>
      </article>
    `);

    reviewEl.textContent = cache.review_text || 'No review text found in cache.';
  } catch (err) {
    docsEl.innerHTML = `<p class="hint">Error: ${esc(err.message)}</p>`;
    chatsEl.innerHTML = '<p class="hint">Could not load chat records.</p>';
    overlapEl.innerHTML = '<p class="hint">Could not load overlap records.</p>';
    reviewEl.textContent = 'Cache unavailable. Run: python3 scripts/build_cache.py';
  }
}

init();
