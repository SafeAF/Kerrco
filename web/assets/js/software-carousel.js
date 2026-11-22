(() => {
  document.querySelectorAll('[data-software-carousel]').forEach((carousel) => {
    const slides = [...carousel.querySelectorAll('.software-proof')];
    const picker = carousel.querySelector('.project-picker');
    const buttons = [...picker.querySelectorAll('[data-project]')];
    const controls = carousel.querySelector('.project-controls');
    const status = carousel.querySelector('[data-project-status]');
    let current = 0;

    function showProject(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, position) => {
        slide.hidden = position !== current;
        slide.inert = position !== current;
      });
      buttons.forEach((button, position) => {
        button.setAttribute('aria-pressed', String(position === current));
      });
      status.textContent = `${current + 1} of ${slides.length} · ${buttons[current].textContent}`;
    }

    buttons.forEach((button, index) => {
      button.addEventListener('click', () => showProject(index));
    });
    carousel.querySelector('[data-previous]').addEventListener('click', () => showProject(current - 1));
    carousel.querySelector('[data-next]').addEventListener('click', () => showProject(current + 1));

    // Keep all projects readable if JavaScript is unavailable. No automatic rotation.
    carousel.setAttribute('data-enhanced', '');
    carousel.setAttribute('aria-roledescription', 'carousel');
    slides.forEach((slide, index) => {
      slide.setAttribute('role', 'group');
      slide.setAttribute('aria-roledescription', 'slide');
      slide.setAttribute('aria-label', `${index + 1} of ${slides.length}: ${buttons[index].textContent}`);
    });
    showProject(0);
    picker.hidden = false;
    controls.hidden = false;
  });
})();
