/**
 * Matching Widget - Three Column Drag and Drop
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
  instructionsEl.textContent = 'Drag labels from the right column to match with items on the left:';
  container.appendChild(instructionsEl);
  
  const colLeft = model.get('left');
  const colRight = model.get('right');
  const correctMatches = model.get('correct_matches');
  
  // Convert to integer map
  const correctMatchesMap = {};
  for (const [key, value] of Object.entries(correctMatches)) {
    correctMatchesMap[parseInt(key)] = parseInt(value);
  }
  
  // Track current matches (left index -> right index)
  const matches = {};
  let submitted = false;
  
  // Three-column grid
  const matchingArea = document.createElement('div');
  matchingArea.className = 'mew-matching-three-col';
  
  // Left column - fixed items
  const leftColumn = document.createElement('div');
  leftColumn.className = 'mew-column';
  
  const leftItems = colLeft.map((text, index) => {
    const item = document.createElement('div');
    item.className = 'mew-item-fixed';
    item.textContent = text;
    leftColumn.appendChild(item);
    return item;
  });
  
  matchingArea.appendChild(leftColumn);
  
  // Middle column - drop zones
  const middleColumn = document.createElement('div');
  middleColumn.className = 'mew-column';
  
  const dropZones = colLeft.map((text, leftIndex) => {
    const dropZone = document.createElement('div');
    dropZone.className = 'mew-drop-zone';
    dropZone.dataset.leftIndex = leftIndex;
    dropZone.textContent = '(drop here)';
    
    dropZone.addEventListener('dragover', (e) => {
      if (submitted) return;
      e.preventDefault();
      e.dataTransfer.dropEffect = 'copy';
      dropZone.classList.add('mew-drop-target');
    });
    
    dropZone.addEventListener('dragleave', () => {
      dropZone.classList.remove('mew-drop-target');
    });
    
    dropZone.addEventListener('drop', (e) => {
      if (submitted) return;
      e.preventDefault();
      dropZone.classList.remove('mew-drop-target');
      
      const rightIndex = parseInt(e.dataTransfer.getData('text/plain'));
      const rightText = colRight[rightIndex];
      
      // Place the label in the drop zone
      dropZone.textContent = rightText;
      dropZone.className = 'mew-drop-zone mew-filled';
      dropZone.dataset.rightIndex = rightIndex;
      
      // Store the match
      matches[leftIndex] = rightIndex;
      updateModel();
      
      // Add click handler to remove match
      dropZone.addEventListener('click', () => {
        if (submitted) return;
        dropZone.textContent = '(drop here)';
        dropZone.className = 'mew-drop-zone';
        delete dropZone.dataset.rightIndex;
        delete matches[leftIndex];
        updateModel();
      });
    });
    
    middleColumn.appendChild(dropZone);
    return dropZone;
  });
  
  matchingArea.appendChild(middleColumn);
  
  // Right column - draggable labels (reusable)
  const rightColumn = document.createElement('div');
  rightColumn.className = 'mew-column';
  
  const rightItems = colRight.map((text, index) => {
    const item = document.createElement('div');
    item.className = 'mew-item-draggable';
    item.textContent = text;
    item.draggable = true;
    item.dataset.rightIndex = index;
    
    item.addEventListener('dragstart', (e) => {
      if (submitted) return;
      item.classList.add('mew-dragging');
      e.dataTransfer.effectAllowed = 'copy';
      e.dataTransfer.setData('text/plain', index);
    });
    
    item.addEventListener('dragend', () => {
      item.classList.remove('mew-dragging');
    });
    
    rightColumn.appendChild(item);
    return item;
  });
  
  matchingArea.appendChild(rightColumn);
  container.appendChild(matchingArea);
  
  // Submit button
  const submitBtn = document.createElement('button');
  submitBtn.className = 'mew-btn mew-btn-primary';
  submitBtn.textContent = 'Check Answers';
  submitBtn.style.marginBottom = '16px';
  
  submitBtn.addEventListener('click', () => {
    if (submitted) return;
    
    if (Object.keys(matches).length !== colLeft.length) {
      alert('Please match all items before checking answers.');
      return;
    }
    
    submitted = true;
    submitBtn.disabled = true;
    
    // Disable dragging
    rightItems.forEach(item => {
      item.draggable = false;
      item.style.cursor = 'default';
      item.style.opacity = '0.5';
    });
    
    // Check answers and update display
    let correctCount = 0;
    
    dropZones.forEach((zone, leftIndex) => {
      const selectedMatch = matches[leftIndex];
      const correctMatch = correctMatchesMap[leftIndex];
      
      // Update left column item
      if (selectedMatch === correctMatch) {
        correctCount++;
        leftItems[leftIndex].classList.add('mew-correct');
        zone.classList.add('mew-correct');
        
        const checkmark = document.createElement('span');
        checkmark.className = 'mew-correct';
        checkmark.textContent = ' ✓';
        zone.appendChild(checkmark);
      } else {
        leftItems[leftIndex].classList.add('mew-incorrect');
        zone.classList.add('mew-incorrect');
        
        const xmark = document.createElement('span');
        xmark.className = 'mew-incorrect';
        xmark.textContent = ' ✗';
        zone.appendChild(xmark);
      }
      
      // Disable clicking on drop zones
      zone.style.cursor = 'default';
      zone.onclick = null;
    });
    
    // Show results
    const resultsEl = document.createElement('div');
    resultsEl.className = correctCount === colLeft.length 
      ? 'mew-feedback mew-correct'
      : 'mew-feedback mew-incorrect';
    resultsEl.textContent = `Score: ${correctCount}/${colLeft.length} correct`;
    container.appendChild(resultsEl);
    
    model.set('value', {
      matches: matches,
      correct: correctCount === colLeft.length,
      score: correctCount,
      total: colLeft.length
    });
    model.save_changes();
  });
  
  container.appendChild(submitBtn);
  
  function updateModel() {
    model.set('value', {
      matches: matches,
      correct: false,
      score: 0,
      total: colLeft.length
    });
    model.save_changes();
  }
  
  el.appendChild(container);
}

export default { render };
