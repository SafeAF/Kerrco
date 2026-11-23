(() => {
  const walkthrough = document.querySelector('[data-workflow]');
  if (!walkthrough) return;

  const picker = walkthrough.querySelector('.workflow-step-picker');
  const buttons = [...walkthrough.querySelectorAll('[data-stage]')];
  const stages = [...walkthrough.querySelectorAll('.workflow-stage')];
  const controls = walkthrough.querySelector('.workflow-controls');
  const previous = walkthrough.querySelector('[data-workflow-previous]');
  const next = walkthrough.querySelector('[data-workflow-next]');
  const status = walkthrough.querySelector('[data-workflow-status]');
  if (!picker || !controls || !previous || !next || !status || !stages.length || buttons.length !== stages.length) return;

  let current = 0;
  function showStage(index) {
    current = Math.max(0, Math.min(index, stages.length - 1));
    stages.forEach((stage, position) => { stage.hidden = position !== current; });
    buttons.forEach((button, position) => { button.setAttribute('aria-pressed', String(position === current)); });
    previous.disabled = current === 0;
    next.disabled = current === stages.length - 1;
    status.textContent = `Stage ${current + 1} of ${stages.length}: ${buttons[current].textContent.trim()}`;
  }

  // Ordinary buttons support Tab, Enter, and Space without a custom keyboard model.
  buttons.forEach((button, index) => { button.addEventListener('click', () => showStage(index)); });
  previous.addEventListener('click', () => {
    showStage(current - 1);
    if (previous.disabled) next.focus();
  });
  next.addEventListener('click', () => {
    showStage(current + 1);
    if (next.disabled) previous.focus();
  });

  // Link fragments can select a stage; without JavaScript every stage is visible.
  function selectFragment() {
    const index = stages.findIndex(stage => `#${stage.id}` === window.location.hash);
    if (index < 0) return;
    showStage(index);
    stages[index].scrollIntoView({ block: 'nearest' });
  }
  showStage(0);
  picker.hidden = false;
  controls.hidden = false;
  selectFragment();
  window.addEventListener('hashchange', selectFragment);
})();
