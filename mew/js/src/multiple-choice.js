/**
 * Multiple Choice Widget
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
  
  const optionsContainer = document.createElement('div');
  optionsContainer.className = 'mew-options';
  
  const options = model.get('options');
  const correctAnswer = model.get('correct_answer');
  
  let selectedIndex = null;
  let answered = false;
  
  options.forEach((option, index) => {
    const optionDiv = document.createElement('div');
    optionDiv.className = 'mew-option';
    
    const radio = document.createElement('input');
    radio.type = 'radio';
    radio.name = 'answer';
    radio.value = index;
    radio.id = `option-${index}`;
    radio.style.marginRight = '10px';
    
    const label = document.createElement('label');
    label.htmlFor = `option-${index}`;
    label.textContent = option;
    label.style.cursor = 'pointer';
    
    optionDiv.appendChild(radio);
    optionDiv.appendChild(label);
    
    const handleSelect = () => {
      if (answered) return;
      
      radio.checked = true;
      selectedIndex = index;
      answered = true;
      
      // Update all options
      const allOptions = optionsContainer.children;
      for (let i = 0; i < allOptions.length; i++) {
        const opt = allOptions[i];
        opt.classList.add('mew-answered');
        
        if (i === correctAnswer) {
          opt.classList.add('mew-correct');
        } else if (i === selectedIndex) {
          opt.classList.add('mew-incorrect');
        } else {
          opt.classList.add('mew-faded');
        }
      }
      
      // Show feedback
      const isCorrect = selectedIndex === correctAnswer;
      feedbackEl.textContent = isCorrect ? '✓ Correct!' : '✗ Incorrect';
      feedbackEl.className = `mew-feedback ${isCorrect ? 'mew-correct' : 'mew-incorrect'}`;
      feedbackEl.style.display = 'block';
      
      // Show explanation
      const explanation = model.get('explanation');
      if (explanation) {
        explanationEl.textContent = explanation;
        explanationEl.className = 'mew-explanation';
        explanationEl.style.display = 'block';
      }
      
      model.set('value', {
        selected: selectedIndex,
        correct: isCorrect,
        answered: true
      });
      model.save_changes();
    };
    
    optionDiv.addEventListener('click', handleSelect);
    radio.addEventListener('change', handleSelect);
    
    optionsContainer.appendChild(optionDiv);
  });
  
  container.appendChild(optionsContainer);
  
  const feedbackEl = document.createElement('div');
  feedbackEl.style.display = 'none';
  container.appendChild(feedbackEl);
  
  const explanationEl = document.createElement('div');
  explanationEl.style.display = 'none';
  container.appendChild(explanationEl);
  
  el.appendChild(container);
}

export default { render };
