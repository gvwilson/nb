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
  container.appendChild(mk('div', 'mew-instructions', 'Drag items to arrange them in the correct order:'));

  const correct = model.get('items');
  let current = model.get('current_order') || [...correct];
  let submitted = false;

  const itemsEl = mk('div', 'mew-ordering-items');
  const feedbackEl = mk('div'); feedbackEl.style.display = 'none';

  function renderItems() {
    itemsEl.innerHTML = '';
    current.forEach((text, i) => {
      const item = mk('div', 'mew-ordering-item');
      item.draggable = !submitted;
      item.append(mk('div', 'mew-position', i + 1), mk('div', 'mew-ordering-text', text));
      if (!submitted) {
        item.addEventListener('dragstart', e => { item.classList.add('mew-dragging'); e.dataTransfer.effectAllowed = 'move'; e.dataTransfer.setData('text/plain', i); });
        item.addEventListener('dragend', () => item.classList.remove('mew-dragging'));
        item.addEventListener('dragover', e => { e.preventDefault(); e.dataTransfer.dropEffect = 'move'; if (itemsEl.querySelector('.mew-dragging') !== item) item.classList.add('mew-drop-target'); });
        item.addEventListener('dragleave', () => item.classList.remove('mew-drop-target'));
        item.addEventListener('drop', e => {
          e.preventDefault(); item.classList.remove('mew-drop-target');
          const from = parseInt(e.dataTransfer.getData('text/plain'));
          if (from !== i) { current.splice(i, 0, current.splice(from, 1)[0]); renderItems(); sync(); }
        });
      }
      itemsEl.appendChild(item);
    });
  }

  renderItems();

  const btnRow = mk('div'); btnRow.style.marginBottom = '16px';
  const checkBtn = mk('button', 'mew-btn mew-btn-primary', 'Check Order'); checkBtn.style.marginRight = '12px';
  const resetBtn = mk('button', 'mew-btn mew-btn-secondary', 'Reset');

  checkBtn.addEventListener('click', () => {
    if (submitted) return;
    submitted = true; checkBtn.disabled = true; resetBtn.style.display = 'none';
    const ok = current.every((v, i) => v === correct[i]);
    [...itemsEl.querySelectorAll('.mew-ordering-item')].forEach((el, i) => {
      el.draggable = false; el.style.cursor = 'default';
      el.classList.add(current[i] === correct[i] ? 'mew-correct' : 'mew-incorrect');
    });
    feedbackEl.textContent = ok ? '✓ Correct order!' : '✗ Incorrect order';
    feedbackEl.className = `mew-feedback ${ok ? 'mew-correct' : 'mew-incorrect'}`;
    feedbackEl.style.display = 'block';
    model.set('value', { order: current, correct: ok }); model.save_changes();
  });

  resetBtn.addEventListener('click', () => {
    if (submitted) return;
    current = [...correct];
    if (model.get('shuffle')) for (let i = current.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [current[i], current[j]] = [current[j], current[i]]; }
    renderItems(); feedbackEl.style.display = 'none'; sync();
  });

  btnRow.append(checkBtn, resetBtn);
  container.append(itemsEl, btnRow, feedbackEl);
  el.appendChild(container);

  function sync() { if (!submitted) { model.set('value', { order: current, correct: false }); model.save_changes(); } }
}

export default { render };
