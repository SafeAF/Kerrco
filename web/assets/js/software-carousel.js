(() => {
  document.querySelectorAll('[data-software-carousel]').forEach((carousel) => {
    const slides = [...carousel.querySelectorAll('.software-proof')];
    const picker = carousel.querySelector('.project-picker');
    const buttons = [...picker.querySelectorAll('[data-project]')];
    let current = 0;

    function showProject(index) {
      current = (index + slides.length) % slides.length;
      slides.forEach((slide, position) => {
        slide.hidden = position !== current;
        slide.inert = position !== current;
      });
      buttons.forEach((button, position) => {
        button.setAttribute('aria-selected', String(position === current));
        button.tabIndex = position === current ? 0 : -1;
      });
    }

    buttons.forEach((button, index) => {
      button.setAttribute('role', 'tab');
      button.addEventListener('click', () => showProject(index));
      button.addEventListener('keydown', (event) => {
        const destinations = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 0, End: slides.length - 1 };
        if (!(event.key in destinations)) return;
        event.preventDefault();
        showProject(destinations[event.key]);
        buttons[current].focus();
      });
    });

    // Keep all projects readable if JavaScript is unavailable. No automatic rotation.
    carousel.setAttribute('data-enhanced', '');
    picker.setAttribute('role', 'tablist');
    slides.forEach((slide, index) => {
      slide.setAttribute('role', 'tabpanel');
      slide.setAttribute('aria-labelledby', buttons[index].id);
    });
    showProject(0);
    picker.hidden = false;
  });
})();
