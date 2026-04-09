(() => {
  const ENDPOINT = window.SBZ_HIT_ENDPOINT || 'https://5pakmkcroalpibvk2y7did66pu0extmx.lambda-url.us-east-1.on.aws/';
  if (!ENDPOINT) return;

  const page = window.location.pathname || '/';

  function render(data) {
    let el = document.getElementById('sbz-hit-counter');
    if (!el) {
      el = document.createElement('div');
      el.id = 'sbz-hit-counter';
      el.style.cssText = [
        'position:fixed',
        'right:12px',
        'bottom:12px',
        'z-index:9999',
        'font:600 12px/1.2 Inter,system-ui,sans-serif',
        'color:#dfefff',
        'background:rgba(9,18,38,.88)',
        'border:1px solid #345d96',
        'border-radius:10px',
        'padding:7px 9px',
        'backdrop-filter:blur(4px)',
        'box-shadow:0 8px 20px rgba(0,0,0,.35)'
      ].join(';');
      document.body.appendChild(el);
    }
    const total = Number(data.total_hits || 0).toLocaleString();
    const today = Number(data.today_hits || 0).toLocaleString();
    el.textContent = `Views ${total} · Today ${today}`;
    el.title = `Unique today: ${Number(data.today_unique || 0).toLocaleString()}`;
  }

  fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ page })
  })
    .then((r) => r.ok ? r.json() : Promise.reject(new Error('counter request failed')))
    .then(render)
    .catch(() => {});
})();
