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

  const q = model.get('question');
  if (q) container.appendChild(mk('div', 'mew-question', q));

  const cards = model.get('cards');
  const total = cards.length;
  const done = new Set();
  const results = {};

  // Build initial queue (0..n-1), shuffle if requested
  let queue = cards.map((_, i) => i);
  if (model.get('shuffle')) {
    for (let i = queue.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [queue[i], queue[j]] = [queue[j], queue[i]];
    }
  }

  // Progress bar
  const progressWrap = mk('div', 'mew-progress');
  const progressFill = mk('div', 'mew-progress-fill'); progressFill.style.width = '0%';
  progressWrap.appendChild(progressFill);
  container.appendChild(progressWrap);

  const counterEl = mk('div', 'mew-instructions');
  container.appendChild(counterEl);

  // Card face
  const cardEl = mk('div', 'mew-card mew-card-front');
  container.appendChild(cardEl);

  // Flip button
  const flipBtn = mk('button', 'mew-btn mew-btn-secondary', 'Flip');
  flipBtn.style.marginBottom = '12px';
  container.appendChild(flipBtn);

  // Rating buttons (hidden until flipped)
  const ratingRow = mk('div', 'mew-rating-btns'); ratingRow.style.display = 'none';
  const gotItBtn  = mk('button', 'mew-btn mew-btn-primary', '✓ Got it');
  const almostBtn = mk('button', 'mew-btn mew-btn-secondary', '~ Almost');
  const noBtn     = mk('button', 'mew-btn', '✗ No');
  noBtn.style.background = '#dc3545';
  ratingRow.append(gotItBtn, almostBtn, noBtn);
  container.appendChild(ratingRow);

  function updateCounter() {
    if (queue.length === 0) return;
    counterEl.textContent = `Card ${done.size + 1} of ${total} — ${queue.length} remaining in queue`;
  }

  function showCard() {
    if (queue.length === 0) return;
    const idx = queue[0];
    cardEl.textContent = cards[idx].front;
    cardEl.className = 'mew-card mew-card-front';
    flipBtn.style.display = '';
    ratingRow.style.display = 'none';
    updateCounter();
  }

  function showComplete() {
    cardEl.textContent = '🎉 All cards reviewed!';
    cardEl.className = 'mew-card mew-card-back';
    counterEl.textContent = `Completed ${total} card${total !== 1 ? 's' : ''}.`;
    flipBtn.style.display = 'none';
    ratingRow.style.display = 'none';
    progressFill.style.width = '100%';
    const restartBtn = mk('button', 'mew-btn mew-btn-secondary', 'Restart');
    restartBtn.addEventListener('click', () => {
      done.clear();
      queue = cards.map((_, i) => i);
      if (model.get('shuffle')) {
        for (let i = queue.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [queue[i], queue[j]] = [queue[j], queue[i]];
        }
      }
      restartBtn.remove();
      showCard();
    });
    container.appendChild(restartBtn);
  }

  flipBtn.addEventListener('click', () => {
    const idx = queue[0];
    cardEl.textContent = cards[idx].back;
    cardEl.className = 'mew-card mew-card-back';
    flipBtn.style.display = 'none';
    ratingRow.style.display = 'flex';
  });

  function rate(rating) {
    const idx = queue.shift();
    if (!results[idx]) results[idx] = { attempts: 0 };
    results[idx].rating = rating;
    results[idx].attempts++;
    if (rating === 'got_it') {
      done.add(idx);
    } else if (rating === 'almost') {
      queue.splice(Math.min(2, queue.length), 0, idx);
    } else {
      queue.splice(Math.min(1, queue.length), 0, idx);
    }
    progressFill.style.width = `${Math.round(done.size / total * 100)}%`;
    model.set('value', { results, complete: done.size === total });
    model.save_changes();
    if (done.size === total) showComplete(); else showCard();
  }

  gotItBtn.addEventListener('click', () => rate('got_it'));
  almostBtn.addEventListener('click', () => rate('almost'));
  noBtn.addEventListener('click', () => rate('no'));

  showCard();
  el.appendChild(container);
}

export default { render };
