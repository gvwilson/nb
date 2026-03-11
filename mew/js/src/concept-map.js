import styles from './styles.css';

function mk(tag, cls, txt) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (txt !== undefined) el.textContent = txt;
  return el;
}

const NS = 'http://www.w3.org/2000/svg';
function mks(tag, attrs) {
  const el = document.createElementNS(NS, tag);
  if (attrs) for (const [k, v] of Object.entries(attrs)) el.setAttribute(k, v);
  return el;
}

let uid = 0;

function render({ model, el }) {
  const id = ++uid;
  const s = mk('style'); s.textContent = styles; el.appendChild(s);
  const container = mk('div', 'mew');
  container.appendChild(mk('div', 'mew-question', model.get('question')));
  container.appendChild(mk('div', 'mew-instructions', 'Select a relationship term, then click two concepts to connect them. Drag concepts to rearrange.'));

  const concepts = model.get('concepts');
  const terms = model.get('terms');
  const positions = {};
  const edges = [];
  let selectedTerm = null, pendingFrom = null, submitted = false;

  // Workspace
  const WW = 560, WH = 360;
  const workspace = mk('div', 'mew-cm-workspace');

  // SVG for drawing edges
  const svg = mks('svg'); svg.classList.add('mew-cm-svg');
  const defs = mks('defs');
  const mkMarker = (mid, color) => {
    const m = mks('marker', { id: mid, viewBox: '0 0 10 10', refX: '9', refY: '5', markerWidth: '6', markerHeight: '6', orient: 'auto' });
    const p = mks('path', { d: 'M0,0 L10,5 L0,10 z' }); p.style.fill = color; m.appendChild(p); return m;
  };
  defs.appendChild(mkMarker(`cm-n-${id}`, '#94a3b8'));
  defs.appendChild(mkMarker(`cm-ok-${id}`, '#28a745'));
  defs.appendChild(mkMarker(`cm-err-${id}`, '#dc3545'));
  svg.appendChild(defs);
  workspace.appendChild(svg);

  // Place concepts in a circle
  concepts.forEach((name, i) => {
    const a = (i / concepts.length) * 2 * Math.PI - Math.PI / 2;
    positions[name] = { x: WW / 2 + WW * 0.36 * Math.cos(a), y: WH / 2 + WH * 0.38 * Math.sin(a) };
  });

  // Create draggable concept nodes
  const nodeEls = {};
  concepts.forEach(name => {
    const node = mk('div', 'mew-cm-node', name);
    nodeEls[name] = node;
    node.style.left = positions[name].x + 'px';
    node.style.top  = positions[name].y + 'px';
    workspace.appendChild(node);

    let dragging = false, moved = false, ox = 0, oy = 0, wr;
    node.addEventListener('mousedown', e => {
      if (submitted) return;
      dragging = true; moved = false;
      wr = workspace.getBoundingClientRect();
      ox = e.clientX - wr.left - positions[name].x;
      oy = e.clientY - wr.top  - positions[name].y;
      node.style.zIndex = 10;
      e.preventDefault(); e.stopPropagation();
    });
    document.addEventListener('mousemove', e => {
      if (!dragging) return;
      const nx = e.clientX - wr.left - ox, ny = e.clientY - wr.top - oy;
      if (Math.abs(nx - positions[name].x) > 3 || Math.abs(ny - positions[name].y) > 3) moved = true;
      positions[name].x = Math.max(0, Math.min(WW, nx));
      positions[name].y = Math.max(0, Math.min(WH, ny));
      node.style.left = positions[name].x + 'px';
      node.style.top  = positions[name].y + 'px';
      renderEdges();
    });
    document.addEventListener('mouseup', () => { if (dragging) { dragging = false; node.style.zIndex = ''; } });

    node.addEventListener('click', e => {
      e.stopPropagation();
      if (submitted || moved || !selectedTerm) return;
      if (!pendingFrom) {
        pendingFrom = name; node.classList.add('mew-cm-pending');
      } else if (pendingFrom === name) {
        nodeEls[pendingFrom].classList.remove('mew-cm-pending'); pendingFrom = null;
      } else {
        const dup = edges.some(e => e.from === pendingFrom && e.to === name && e.label === selectedTerm);
        if (!dup) { edges.push({ from: pendingFrom, to: name, label: selectedTerm }); renderEdges(); renderEdgeList(); sync(); }
        nodeEls[pendingFrom].classList.remove('mew-cm-pending'); pendingFrom = null;
      }
    });
  });

  // Click on empty workspace to cancel pending
  workspace.addEventListener('click', () => {
    if (pendingFrom && !submitted) { nodeEls[pendingFrom].classList.remove('mew-cm-pending'); pendingFrom = null; }
  });

  container.appendChild(workspace);

  // Relationship term buttons
  const termsRow = mk('div', 'mew-cm-terms');
  const termBtns = {};
  terms.forEach(term => {
    const btn = mk('button', 'mew-cm-term', term);
    btn.addEventListener('click', () => {
      if (submitted) return;
      if (selectedTerm === term) { selectedTerm = null; btn.classList.remove('mew-cm-term-selected'); }
      else { Object.values(termBtns).forEach(b => b.classList.remove('mew-cm-term-selected')); selectedTerm = term; btn.classList.add('mew-cm-term-selected'); }
      if (pendingFrom) { nodeEls[pendingFrom].classList.remove('mew-cm-pending'); pendingFrom = null; }
    });
    termBtns[term] = btn;
    termsRow.appendChild(btn);
  });
  container.appendChild(termsRow);

  // List of placed edges with remove buttons
  const edgeList = mk('div', 'mew-cm-edge-list');
  container.appendChild(edgeList);

  function renderEdgeList() {
    edgeList.innerHTML = '';
    edges.forEach((edge, i) => {
      const row = mk('div', 'mew-cm-edge-row');
      row.appendChild(mk('span', null, edge.from + ' '));
      row.appendChild(mk('span', 'mew-cm-edge-label', edge.label));
      row.appendChild(mk('span', null, ' ' + edge.to));
      if (!submitted) {
        const x = mk('button', 'mew-cm-edge-remove', '✕');
        x.addEventListener('click', () => { edges.splice(i, 1); renderEdges(); renderEdgeList(); sync(); });
        row.appendChild(x);
      } else {
        row.appendChild(mk('span', edge.correct ? 'mew-correct' : 'mew-incorrect', edge.correct ? ' ✓' : ' ✗'));
      }
      edgeList.appendChild(row);
    });
  }

  // Check / Clear buttons
  const btnRow = mk('div'); btnRow.style.marginTop = '12px';
  const checkBtn = mk('button', 'mew-btn mew-btn-primary', 'Check Map'); checkBtn.style.marginRight = '12px';
  const clearBtn = mk('button', 'mew-btn mew-btn-secondary', 'Clear All');

  checkBtn.addEventListener('click', () => {
    if (submitted || !edges.length) return;
    submitted = true; checkBtn.disabled = true; clearBtn.style.display = 'none';
    Object.values(termBtns).forEach(b => { b.disabled = true; });
    const ce = model.get('correct_edges') || [];
    let score = 0;
    edges.forEach(e => { e.correct = ce.some(c => c.from === e.from && c.to === e.to && c.label === e.label); if (e.correct) score++; });
    renderEdges(); renderEdgeList();
    const allRight = score === ce.length && edges.length === ce.length;
    container.appendChild(mk('div', `mew-feedback ${allRight ? 'mew-correct' : 'mew-incorrect'}`, `${score}/${ce.length} correct connections`));
    model.set('value', { edges, score, total: ce.length, correct: allRight });
    model.save_changes();
  });

  clearBtn.addEventListener('click', () => { edges.length = 0; renderEdges(); renderEdgeList(); sync(); });

  btnRow.append(checkBtn, clearBtn);
  container.appendChild(btnRow);

  // Draw edges in SVG
  function renderEdges() {
    while (svg.childNodes.length > 1) svg.removeChild(svg.lastChild);
    edges.forEach(edge => {
      const fp = positions[edge.from], tp = positions[edge.to];
      if (!fp || !tp) return;
      const dx = tp.x - fp.x, dy = tp.y - fp.y;
      const dist = Math.sqrt(dx * dx + dy * dy) || 1;
      const ux = dx / dist, uy = dy / dist;
      const rFrom = Math.max(nodeEls[edge.from].offsetWidth, nodeEls[edge.from].offsetHeight) / 2 + 4;
      const rTo   = Math.max(nodeEls[edge.to].offsetWidth,   nodeEls[edge.to].offsetHeight)   / 2 + 12;
      const x1 = fp.x + ux * rFrom, y1 = fp.y + uy * rFrom;
      const x2 = tp.x - ux * rTo,   y2 = tp.y - uy * rTo;

      const color  = edge.correct === true ? '#28a745' : edge.correct === false ? '#dc3545' : '#94a3b8';
      const mId    = edge.correct === true ? `cm-ok-${id}` : edge.correct === false ? `cm-err-${id}` : `cm-n-${id}`;

      const line = mks('line', { x1, y1, x2, y2, 'stroke-width': 2 });
      line.style.stroke = color;
      line.setAttribute('marker-end', `url(#${mId})`);

      const mx = (fp.x + tp.x) / 2, my = (fp.y + tp.y) / 2;
      const txt = mks('text', { x: mx, y: my - 8, 'text-anchor': 'middle', 'font-size': 12 });
      txt.style.fill = color;
      txt.style.fontFamily = 'inherit';
      txt.style.stroke = 'var(--background)';
      txt.style.strokeWidth = '4';
      txt.style.paintOrder = 'stroke fill';
      txt.textContent = edge.label;

      svg.append(line, txt);
    });
  }

  function sync() {
    model.set('value', { edges, score: 0, total: (model.get('correct_edges') || []).length, correct: false });
    model.save_changes();
  }

  renderEdges();
  el.appendChild(container);
}

export default { render };
