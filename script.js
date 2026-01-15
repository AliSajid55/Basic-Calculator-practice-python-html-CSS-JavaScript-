const display = document.getElementById('display');
let current = '';
let resultShown = false;

document.querySelector('.keys').addEventListener('click', e => {
  const target = e.target;
  if (!target.matches('button')) return;
  const val = target.dataset.value;
  const action = target.dataset.action;

  if (action === 'clear') {
    current = '';
    display.textContent = '0';
    resultShown = false;
    return;
  }

  if (action === 'back') {
    if (resultShown) { current=''; resultShown=false; display.textContent='0'; return; }
    current = current.slice(0, -1);
    display.textContent = current || '0';
    return;
  }

  if (action === 'percent') {
    try {
      current = String(parseFloat(current || '0') / 100);
      display.textContent = current;
      resultShown = true;
    } catch { display.textContent = 'Error' }
    return;
  }

  if (action === 'equals') {
    try {
      let expression = current.replace(/×/g, '*').replace(/÷/g, '/').replace(/−/g, '-');
      if (/[^0-9+\-*/(). %]/.test(expression)) { display.textContent = 'Error'; current=''; return; }
      const res = Function('"use strict";return('+expression+')')();
      display.textContent = String(res);
      current = String(res);
      resultShown = true;
    } catch {
      display.textContent = 'Error';
      current = '';
    }
    return;
  }

  // append number or operator
  if (resultShown && /[0-9.]/.test(val)) {
    current = val;
    resultShown = false;
    display.textContent = current;
    return;
  }

  current += val;
  display.textContent = current;
});
