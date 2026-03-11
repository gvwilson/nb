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
  container.appendChild(mk('div', 'mew-instructions', 'Drag labels from the right column to match with items on the left:'));

  const left = model.get('left'), right = model.get('right');
  const correctMap = Object.fromEntries(Object.entries(model.get('correct_matches')).map(([k, v]) => [+k, +v]));
  const matches = {};
  let submitted = false;

  const grid = mk('div', 'mew-matching-three-col');
  const leftCol = mk('div', 'mew-column'), midCol = mk('div', 'mew-column'), rightCol = mk('div', 'mew-column');

  const leftItems = left.map(text => { const d = mk('div', 'mew-item-fixed', text); leftCol.appendChild(d); return d; });

  const zones = left.map((_, li) => {
    const z = mk('div', 'mew-drop-zone', '(drop here)');
    z.addEventListener('dragover', e => { if (submitted) return; e.preventDefault(); z.classList.add('mew-drop-target'); });
    z.addEventListener('dragleave', () => z.classList.remove('mew-drop-target'));
    z.addEventListener('drop', e => {
      if (submitted) return;
      e.preventDefault(); z.classList.remove('mew-drop-target');
      const ri = parseInt(e.dataTransfer.getData('text/plain'));
      z.textContent = right[ri]; z.className = 'mew-drop-zone mew-filled';
      matches[li] = ri; sync();
      z.addEventListener('click', () => {
        if (submitted) return;
        z.textContent = '(drop here)'; z.className = 'mew-drop-zone';
        delete matches[li]; sync();
      });
    });
    midCol.appendChild(z);
    return z;
  });

  right.forEach((text, i) => {
    const d = mk('div', 'mew-item-draggable', text); d.draggable = true;
    d.addEventListener('dragstart', e => { if (submitted) return; d.classList.add('mew-dragging'); e.dataTransfer.effectAllowed = 'copy'; e.dataTransfer.setData('text/plain', i); });
    d.addEventListener('dragend', () => d.classList.remove('mew-dragging'));
    rightCol.appendChild(d);
  });

  grid.append(leftCol, midCol, rightCol);
  container.appendChild(grid);

  const submitBtn = mk('button', 'mew-btn mew-btn-primary', 'Check Answers'); submitBtn.style.marginBottom = '16px';
  submitBtn.addEventListener('click', () => {
    if (submitted) return;
    if (Object.keys(matches).length !== left.length) { alert('Please match all items before checking answers.'); return; }
    submitted = true; submitBtn.disabled = true;
    rightCol.querySelectorAll('.mew-item-draggable').forEach(d => { d.draggable = false; d.style.cssText = 'cursor:default;opacity:.5'; });
    let score = 0;
    zones.forEach((z, li) => {
      const ok = matches[li] === correctMap[li];
      if (ok) score++;
      leftItems[li].classList.add(ok ? 'mew-correct' : 'mew-incorrect');
      z.classList.add(ok ? 'mew-correct' : 'mew-incorrect');
      z.appendChild(mk('span', ok ? 'mew-correct' : 'mew-incorrect', ok ? ' ✓' : ' ✗'));
    });
    container.appendChild(mk('div', `mew-feedback ${score === left.length ? 'mew-correct' : 'mew-incorrect'}`, `Score: ${score}/${left.length} correct`));
    model.set('value', { matches, correct: score === left.length, score, total: left.length });
    model.save_changes();
  });

  container.appendChild(submitBtn);
  el.appendChild(container);

  function sync() { model.set('value', { matches, correct: false, score: 0, total: left.length }); model.save_changes(); }
}

export default { render };
