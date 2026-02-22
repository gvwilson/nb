/**
 * Labeling Widget
 * 
 * Left side: Available labels (numbered)
 * Right side: Text with lines that can be labeled
 * Users drag label numbers to the left edge of text lines
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
  instructionsEl.textContent = 'Drag label numbers to the left edge of text lines. Drag outside to remove.';
  container.appendChild(instructionsEl);
  
  const labels = model.get('labels');
  const textLines = model.get('text_lines');
  const correctLabels = model.get('correct_labels');
  
  // Track placed labels: { lineIndex: [labelIndex1, labelIndex2, ...] }
  const placedLabels = {};
  let submitted = false;
  let draggedLabelEl = null;
  
  // Two-column layout
  const labelingArea = document.createElement('div');
  labelingArea.className = 'mew-labeling-area';
  
  // LEFT SIDE - Available labels
  const labelsColumn = document.createElement('div');
  labelsColumn.className = 'mew-labeling-labels';
  
  const labelsTitle = document.createElement('div');
  labelsTitle.className = 'mew-labeling-title';
  labelsTitle.textContent = 'Available Labels:';
  labelsColumn.appendChild(labelsTitle);
  
  labels.forEach((labelText, index) => {
    const labelItem = document.createElement('div');
    labelItem.className = 'mew-label-item';
    
    const labelNum = document.createElement('span');
    labelNum.className = 'mew-label-num';
    labelNum.textContent = index + 1;
    labelNum.draggable = true;
    labelNum.dataset.labelIndex = index;
    
    labelNum.addEventListener('dragstart', (e) => {
      if (submitted) return;
      e.dataTransfer.effectAllowed = 'copy';
      e.dataTransfer.setData('text/plain', index);
      draggedLabelEl = e.target;
      draggedLabelEl.classList.add('mew-dragging');
    });
    
    labelNum.addEventListener('dragend', () => {
      if (draggedLabelEl) {
        draggedLabelEl.classList.remove('mew-dragging');
        draggedLabelEl = null;
      }
    });
    
    const labelTextEl = document.createElement('span');
    labelTextEl.className = 'mew-label-text';
    labelTextEl.textContent = labelText;
    
    labelItem.appendChild(labelNum);
    labelItem.appendChild(labelTextEl);
    labelsColumn.appendChild(labelItem);
  });
  
  labelingArea.appendChild(labelsColumn);
  
  // RIGHT SIDE - Text with label drop zones
  const textColumn = document.createElement('div');
  textColumn.className = 'mew-labeling-text';
  
  const textTitle = document.createElement('div');
  textTitle.className = 'mew-labeling-title';
  textTitle.textContent = 'Text:';
  textColumn.appendChild(textTitle);
  
  const textLinesContainer = document.createElement('div');
  textLinesContainer.className = 'mew-text-lines';
  
  textLines.forEach((lineText, lineIndex) => {
    const lineContainer = document.createElement('div');
    lineContainer.className = 'mew-text-line';
    lineContainer.dataset.lineIndex = lineIndex;
    
    // Drop zone on the left edge
    const dropZone = document.createElement('div');
    dropZone.className = 'mew-label-drop-zone';
    dropZone.dataset.lineIndex = lineIndex;
    
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
      
      const labelIndex = parseInt(e.dataTransfer.getData('text/plain'));
      
      // Add label to this line
      if (!placedLabels[lineIndex]) {
        placedLabels[lineIndex] = [];
      }
      placedLabels[lineIndex].push(labelIndex);
      
      renderPlacedLabels(dropZone, lineIndex);
      updateModel();
    });
    
    // Text content
    const textEl = document.createElement('div');
    textEl.className = 'mew-text-content';
    textEl.textContent = lineText;
    
    lineContainer.appendChild(dropZone);
    lineContainer.appendChild(textEl);
    textLinesContainer.appendChild(lineContainer);
  });
  
  textColumn.appendChild(textLinesContainer);
  labelingArea.appendChild(textColumn);
  container.appendChild(labelingArea);
  
  // Function to render placed labels in a drop zone
  function renderPlacedLabels(dropZone, lineIndex) {
    dropZone.innerHTML = '';
    
    if (placedLabels[lineIndex] && placedLabels[lineIndex].length > 0) {
      placedLabels[lineIndex].forEach((labelIndex) => {
        const badge = document.createElement('span');
        badge.className = 'mew-label-badge';
        badge.textContent = labelIndex + 1;
        badge.draggable = !submitted;
        badge.dataset.labelIndex = labelIndex;
        badge.dataset.currentLine = lineIndex;
        
        if (!submitted) {
          // Allow re-dragging to move to another line
          badge.addEventListener('dragstart', (e) => {
            e.dataTransfer.effectAllowed = 'move';
            e.dataTransfer.setData('text/plain', JSON.stringify({
              labelIndex: labelIndex,
              fromLine: lineIndex
            }));
            draggedLabelEl = badge;
            badge.classList.add('mew-dragging');
          });
          
          badge.addEventListener('dragend', (e) => {
            badge.classList.remove('mew-dragging');
            
            // Check if dragged outside the text column (delete)
            const rect = textColumn.getBoundingClientRect();
            if (e.clientX < rect.left) {
              // Remove this label
              placedLabels[lineIndex] = placedLabels[lineIndex].filter(idx => idx !== labelIndex);
              if (placedLabels[lineIndex].length === 0) {
                delete placedLabels[lineIndex];
              }
              renderPlacedLabels(dropZone, lineIndex);
              updateModel();
            }
            
            draggedLabelEl = null;
          });
        }
        
        dropZone.appendChild(badge);
      });
    }
  }
  
  // Update drop zones to also accept moved labels
  textLinesContainer.querySelectorAll('.mew-label-drop-zone').forEach((zone, lineIndex) => {
    const originalDrop = zone.ondrop;
    
    zone.addEventListener('drop', (e) => {
      if (submitted) return;
      
      const data = e.dataTransfer.getData('text/plain');
      try {
        const moveData = JSON.parse(data);
        // Moving an existing label
        if (moveData.fromLine !== undefined) {
          e.preventDefault();
          zone.classList.remove('mew-drop-target');
          
          const { labelIndex, fromLine } = moveData;
          
          // Remove from old line
          if (placedLabels[fromLine]) {
            placedLabels[fromLine] = placedLabels[fromLine].filter(idx => idx !== labelIndex);
            if (placedLabels[fromLine].length === 0) {
              delete placedLabels[fromLine];
            }
            const oldDropZone = textLinesContainer.children[fromLine].querySelector('.mew-label-drop-zone');
            renderPlacedLabels(oldDropZone, fromLine);
          }
          
          // Add to new line
          if (!placedLabels[lineIndex]) {
            placedLabels[lineIndex] = [];
          }
          placedLabels[lineIndex].push(labelIndex);
          renderPlacedLabels(zone, lineIndex);
          updateModel();
        }
      } catch (e) {
        // Not a move, already handled by original drop handler
      }
    });
  });
  
  // Submit button
  const submitBtn = document.createElement('button');
  submitBtn.className = 'mew-btn mew-btn-primary';
  submitBtn.textContent = 'Check Labels';
  submitBtn.style.marginTop = '16px';
  
  submitBtn.addEventListener('click', () => {
    if (submitted) return;
    
    submitted = true;
    submitBtn.disabled = true;
    
    // Disable all dragging
    labelsColumn.querySelectorAll('.mew-label-num').forEach(num => {
      num.draggable = false;
      num.style.cursor = 'default';
    });
    
    // Calculate score
    let correctCount = 0;
    let totalCorrect = 0;
    
    // Count total correct labels across all lines
    for (const [lineIdx, labelIndices] of Object.entries(correctLabels)) {
      totalCorrect += labelIndices.length;
    }
    
    // Check each placed label
    const lineContainers = textLinesContainer.querySelectorAll('.mew-text-line');
    lineContainers.forEach((lineContainer, lineIndex) => {
      const dropZone = lineContainer.querySelector('.mew-label-drop-zone');
      const badges = dropZone.querySelectorAll('.mew-label-badge');
      
      badges.forEach(badge => {
        const labelIndex = parseInt(badge.dataset.labelIndex);
        const correctForThisLine = correctLabels[lineIndex] || [];
        
        if (correctForThisLine.includes(labelIndex)) {
          correctCount++;
          badge.classList.add('mew-correct');
        } else {
          badge.classList.add('mew-incorrect');
        }
      });
    });
    
    // Show results
    const resultsEl = document.createElement('div');
    resultsEl.className = 'mew-feedback';
    const percentage = totalCorrect > 0 ? Math.round((correctCount / totalCorrect) * 100) : 0;
    resultsEl.textContent = `Score: ${correctCount}/${totalCorrect} correct (${percentage}%)`;
    resultsEl.classList.add(correctCount === totalCorrect ? 'mew-correct' : 'mew-incorrect');
    container.appendChild(resultsEl);
    
    model.set('value', {
      placed_labels: placedLabels,
      score: correctCount,
      total: totalCorrect,
      correct: correctCount === totalCorrect
    });
    model.save_changes();
  });
  
  container.appendChild(submitBtn);
  
  function updateModel() {
    if (!submitted) {
      model.set('value', {
        placed_labels: placedLabels,
        score: 0,
        total: 0,
        correct: false
      });
      model.save_changes();
    }
  }
  
  el.appendChild(container);
}

export default { render };
