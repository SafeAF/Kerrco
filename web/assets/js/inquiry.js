(() => {
  const form = document.querySelector('[data-inquiry-form]');
  if (!form || !window.fetch || !window.URLSearchParams || !window.FormData) return;
  const status = form.querySelector('[data-inquiry-status]');
  const submit = form.querySelector('[type="submit"]');
  if (!status || !submit) return;
  let sending = false;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (sending || !form.reportValidity()) return;
    sending = true;
    submit.disabled = true;
    form.setAttribute('aria-busy', 'true');
    status.dataset.state = 'pending';
    status.textContent = 'Sending your inquiry…';
    const controller = typeof AbortController === 'function' ? new AbortController() : null;
    const timer = controller ? setTimeout(() => controller.abort(), 30000) : null;
    try {
      const response = await fetch(form.action, {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: new URLSearchParams(new FormData(form)),
        credentials: 'same-origin',
        redirect: 'error',
        ...(controller ? { signal: controller.signal } : {}),
      });
      const type = response.headers.get('content-type') || '';
      if (!type.includes('application/json')) throw new Error('unavailable');
      const result = await response.json();
      if (response.ok && result.preview === true) {
        status.dataset.state = 'preview';
        status.textContent = 'Preview only. Your inquiry has not been sent. Your entries have been kept.';
      } else if (response.status === 201 && result.ok === true) {
        status.dataset.state = 'success';
        status.textContent = 'Thank you. Your inquiry has been submitted. I’ll respond by email.';
        form.reset();
      } else {
        status.dataset.state = 'error';
        status.textContent = (result.error || 'Your inquiry could not be sent. Please try again or use the email address alongside this form.') + ' Your entries have been kept.';
      }
    } catch {
      status.dataset.state = 'error';
      status.textContent = 'Your inquiry could not be confirmed. Please try again or use the email address alongside this form. Your entries have been kept.';
    } finally {
      if (timer !== null) clearTimeout(timer);
      sending = false;
      submit.disabled = false;
      form.removeAttribute('aria-busy');
      status.focus();
    }
  });
})();
