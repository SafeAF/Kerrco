import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../web/assets/js/inquiry.js', import.meta.url), 'utf8');
function fixture(fetch) {
  const status = { dataset: {}, textContent: '', focus() { this.focused = true; } };
  const submit = { disabled: false };
  const form = {
    action: 'https://kerrco.us/inquiries', attrs: {}, resets: 0,
    querySelector(selector) { return selector === '[data-inquiry-status]' ? status : submit; },
    addEventListener(name, fn) { this[name] = fn; },
    reportValidity() { return true; },
    setAttribute(key, value) { this.attrs[key] = value; },
    removeAttribute(key) { delete this.attrs[key]; },
    reset() { this.resets++; },
  };
  function FormData() { return [['name', 'Test Visitor'], ['email', 'visitor@example.test'], ['message', 'Example inquiry']]; }
  vm.runInNewContext(source, { document: { querySelector: () => form }, window: { fetch, URLSearchParams, FormData }, fetch, URLSearchParams, FormData, AbortController, setTimeout, clearTimeout });
  return { form, status, submit, send: () => form.submit({ preventDefault() {} }) };
}
function response(status, data, type = 'application/json') {
  return { status, ok: status >= 200 && status < 300, headers: { get: () => type }, json: async () => data };
}

test('only an explicit delivery acknowledgement clears the inquiry', async () => {
  const page = fixture(async () => response(201, { ok: true }));
  await page.send();
  assert.equal(page.form.resets, 1);
  assert.equal(page.status.dataset.state, 'success');
  assert(page.status.focused);
  assert.equal(page.submit.disabled, false);
});

test('failures, HTML errors, unexpected redirects, and previews preserve entries', async () => {
  const results = [
    async () => response(503, { ok: false, error: 'Email is unavailable.' }),
    async () => response(429, { ok: false, error: 'Please wait.' }),
    async () => response(200, { ok: true }),
    async () => response(200, { preview: true, ok: false }),
    async () => response(502, {}, 'text/html'),
    async () => { throw new Error('network or redirect failure'); },
  ];
  for (const fetch of results) {
    const page = fixture(fetch);
    await page.send();
    assert.equal(page.form.resets, 0);
    assert.notEqual(page.status.dataset.state, 'success');
    assert.equal(page.submit.disabled, false);
    assert.equal(page.form.attrs['aria-busy'], undefined);
  }
});

test('duplicate clicks send one pending request and use the intended encoding', async () => {
  let resolve;
  let calls = 0;
  const page = fixture((url, options) => {
    calls++;
    assert.equal(url, 'https://kerrco.us/inquiries');
    assert.equal(options.method, 'POST');
    assert.equal(options.redirect, 'error');
    assert.equal(options.body.get('email'), 'visitor@example.test');
    return new Promise(done => { resolve = done; });
  });
  const first = page.send();
  await page.send();
  assert.equal(calls, 1);
  assert(page.submit.disabled);
  resolve(response(201, { ok: true }));
  await first;
  assert.equal(page.form.resets, 1);
});
