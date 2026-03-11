import styles from './styles.css';

function mk(tag, cls, txt) {
  const el = document.createElement(tag);
  if (cls) el.className = cls;
  if (txt !== undefined) el.textContent = txt;
  return el;
}

function render({ model, el }) {
  const s = mk('style'); s.textContent = styles; el.appendChild(s);
  const container = mk('div', 'mew');
  container.appendChild(mk('div', 'mew-question', model.get('question')));
  container.appendChild(mk('div', 'mew-instructions', 'Drag label numbers to text lines. Drag outside to remove.'));

  const labels = model.get('labels'), textLines = model.get('text_lines'), correctLabels = model.get('correct_labels');
  const placed = {};
  let submitted = false;

  const area = mk('div', 'mew-labeling-area');
  const labelsCol = mk('div', 'mew-labeling-labels'), textCol = mk('div', 'mew-labeling-text');
  labelsCol.appendChild(mk('div', 'mew-labeling-title', 'Available Labels:'));
  textCol.appendChild(mk('div', 'mew-labeling-title', 'Text:'));

  labels.forEach((text, i) => {
    const item = mk('div', 'mew-label-item');
    const num = mk('span', 'mew-label-num', i + 1); num.draggable = true;
    num.addEventListener('dragstart', e => { if (submitted) return; e.dataTransfer.effectAllowed = 'copy'; e.dataTransfer.setData('text/plain', i); num.classList.add('mew-dragging'); });
    num.addEventListener('dragend', () => num.classList.remove('mew-dragging'));
    item.append(num, mk('span', 'mew-label-text', text));
    labelsCol.appendChild(item);
  });

  const linesEl = mk('div', 'mew-text-lines');

  function renderBadges(zone, lineIdx) {
    zone.innerHTML = '';
    (placed[lineIdx] || []).forEach(li => {
      const b = mk('span', 'mew-label-badge', li + 1); b.draggable = !submitted; b.dataset.labelIndex = li;
      if (!submitted) {
        b.addEventListener('dragstart', e => { e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', JSON.stringify({ li, from: lineIdx })); b.classList.add('mew-dragging'); });
        b.addEventListener('dragend', e => {
          b.classList.remove('mew-dragging');
          if (e.clientX < textCol.getBoundingClientRect().left) {
            placed[lineIdx] = placed[lineIdx].filter(x => x !== li);
            if (!placed[lineIdx].length) delete placed[lineIdx];
            renderBadges(zone, lineIdx); sync();
          }
        });
      }
      zone.appendChild(b);
    });
  }

  textLines.forEach((text, lineIdx) => {
    const line = mk('div', 'mew-text-line');
    const zone = mk('div', 'mew-label-drop-zone');
    zone.addEventListener('dragover', e => { if (submitted) return; e.preventDefault(); zone.classList.add('mew-drop-target'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('mew-drop-target'));
    zone.addEventListener('drop', e => {
      if (submitted) return;
      e.preventDefault(); zone.classList.remove('mew-drop-target');
      let li, from = null;
      try { const d = JSON.parse(e.dataTransfer.getData('text/plain')); li = d.li; from = d.from; } catch { li = parseInt(e.dataTransfer.getData('text/plain')); }
      if (from !== null && from !== lineIdx) {
        placed[from] = placed[from].filter(x => x !== li);
        if (!placed[from].length) delete placed[from];
        renderBadges(linesEl.children[from].querySelector('.mew-label-drop-zone'), from);
      }
      if (!placed[lineIdx]) placed[lineIdx] = [];
      placed[lineIdx].push(li); renderBadges(zone, lineIdx); sync();
    });
    line.append(zone, mk('div', 'mew-text-content', text));
    linesEl.appendChild(line);
  });

  textCol.appendChild(linesEl);
  area.append(labelsCol, textCol);
  container.appendChild(area);

  const submitBtn = mk('button', 'mew-btn mew-btn-primary', 'Check Labels'); submitBtn.style.marginTop = '16px';
  submitBtn.addEventListener('click', () => {
    if (submitted) return;
    submitted = true; submitBtn.disabled = true;
    labelsCol.querySelectorAll('.mew-label-num').forEach(n => { n.draggable = false; n.style.cursor = 'default'; });
    const total = Object.values(correctLabels).reduce((s, a) => s + a.length, 0);
    let score = 0;
    linesEl.querySelectorAll('.mew-text-line').forEach((line, lineIdx) => {
      line.querySelectorAll('.mew-label-badge').forEach(b => {
        const ok = (correctLabels[lineIdx] || []).includes(parseInt(b.dataset.labelIndex));
        if (ok) score++;
        b.classList.add(ok ? 'mew-correct' : 'mew-incorrect');
      });
    });
    const pct = total ? Math.round(score / total * 100) : 0;
    container.appendChild(mk('div', `mew-feedback ${score === total ? 'mew-correct' : 'mew-incorrect'}`, `Score: ${score}/${total} correct (${pct}%)`));
    model.set('value', { placed_labels: placed, score, total, correct: score === total });
    model.save_changes();
  });

  container.appendChild(submitBtn);
  el.appendChild(container);

  function sync() { if (!submitted) { model.set('value', { placed_labels: placed, score: 0, total: 0, correct: false }); model.save_changes(); } }
}

export default { render };
