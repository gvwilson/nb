/**
 * Ordering Widget - Drag and Drop
 */

import styles from './styles.css';

function render({ model, el }) {
  // Inject CSS
  const styleSheet = document.createElement('style');
  styleSheet.textContent = styles;
  el.appendChild(styleSheet);
  
  const container = document.createElement('div');
  container.className = 'mew';
  
  const questionEl = document.createElement('div');
  questionEl.className = 'mew-question';
  questionEl.textContent = model.get('question');
  container.appendChild(questionEl);
  
  const instructionsEl = document.createElement('div');
  instructionsEl.className = 'mew-instructions';
  instructionsEl.textContent = 'Drag items to arrange them in the correct order:';
  container.appendChild(instructionsEl);
  
  const correctOrder = model.get('items');
  let currentOrder = model.get('current_order') || [...correctOrder];
  let submitted = false;
  
  const itemsContainer = document.createElement('div');
  itemsContainer.className = 'mew-ordering-items';
  
  function renderItems() {
    itemsContainer.innerHTML = '';
    
    currentOrder.forEach((text, index) => {
      const item = document.createElement('div');
      item.className = 'mew-ordering-item';
      item.draggable = !submitted;
      item.dataset.index = index;
      
      const positionEl = document.createElement('div');
      positionEl.className = 'mew-position';
      positionEl.textContent = index + 1;
      
      const textEl = document.createElement('div');
      textEl.className = 'mew-ordering-text';
      textEl.textContent = text;
      
      item.appendChild(positionEl);
      item.appendChild(textEl);
      
      if (!submitted) {
        item.addEventListener('dragstart', (e) => {
          item.classList.add('mew-dragging');
          e.dataTransfer.effectAllowed = 'move';
          e.dataTransfer.setData('text/plain', index);
        });
        
        item.addEventListener('dragend', () => {
          item.classList.remove('mew-dragging');
        });
        
        item.addEventListener('dragover', (e) => {
          e.preventDefault();
          e.dataTransfer.dropEffect = 'move';
          
          const draggingItem = itemsContainer.querySelector('.mew-dragging');
          if (draggingItem && draggingItem !== item) {
            item.classList.add('mew-drop-target');
          }
        });
        
        item.addEventListener('dragleave', () => {
          item.classList.remove('mew-drop-target');
        });
        
        item.addEventListener('drop', (e) => {
          e.preventDefault();
          item.classList.remove('mew-drop-target');
          
          const fromIndex = parseInt(e.dataTransfer.getData('text/plain'));
          const toIndex = index;
          
          if (fromIndex !== toIndex) {
            // Reorder array
            const [movedItem] = currentOrder.splice(fromIndex, 1);
            currentOrder.splice(toIndex, 0, movedItem);
            
            renderItems();
            updateModel();
          }
        });
      }
      
      itemsContainer.appendChild(item);
    });
  }
  
  renderItems();
  container.appendChild(itemsContainer);
  
  // Buttons
  const buttonRow = document.createElement('div');
  buttonRow.style.marginBottom = '16px';
  
  const checkBtn = document.createElement('button');
  checkBtn.className = 'mew-btn mew-btn-primary';
  checkBtn.textContent = 'Check Order';
  checkBtn.style.marginRight = '12px';
  
  checkBtn.addEventListener('click', () => {
    if (submitted) return;
    
    submitted = true;
    checkBtn.disabled = true;
    resetBtn.style.display = 'none';
    
    const isCorrect = currentOrder.every((item, idx) => item === correctOrder[idx]);
    
    // Update visual feedback
    const itemEls = itemsContainer.querySelectorAll('.mew-ordering-item');
    itemEls.forEach((itemEl, idx) => {
      itemEl.draggable = false;
      itemEl.style.cursor = 'default';
      
      if (currentOrder[idx] === correctOrder[idx]) {
        itemEl.classList.add('mew-correct');
      } else {
        itemEl.classList.add('mew-incorrect');
      }
    });
    
    feedbackEl.textContent = isCorrect ? '✓ Correct order!' : '✗ Incorrect order';
    feedbackEl.className = `mew-feedback ${isCorrect ? 'mew-correct' : 'mew-incorrect'}`;
    feedbackEl.style.display = 'block';
    
    model.set('value', {
      order: currentOrder,
      correct: isCorrect
    });
    model.save_changes();
  });
  
  buttonRow.appendChild(checkBtn);
  
  const resetBtn = document.createElement('button');
  resetBtn.className = 'mew-btn mew-btn-secondary';
  resetBtn.textContent = 'Reset';
  
  resetBtn.addEventListener('click', () => {
    if (submitted) return;
    
    const shouldShuffle = model.get('shuffle');
    if (shouldShuffle) {
      currentOrder = [...correctOrder];
      for (let i = currentOrder.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [currentOrder[i], currentOrder[j]] = [currentOrder[j], currentOrder[i]];
      }
    } else {
      currentOrder = [...correctOrder];
    }
    
    renderItems();
    feedbackEl.style.display = 'none';
    updateModel();
  });
  
  buttonRow.appendChild(resetBtn);
  container.appendChild(buttonRow);
  
  const feedbackEl = document.createElement('div');
  feedbackEl.style.display = 'none';
  container.appendChild(feedbackEl);
  
  function updateModel() {
    if (!submitted) {
      model.set('value', {
        order: currentOrder,
        correct: false
      });
      model.save_changes();
    }
  }
  
  el.appendChild(container);
}

export default { render };
