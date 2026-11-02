import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, mkdir, copyFile, readFile, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkSite } from './prepare-release.mjs';

test('release validation rejects broken assets, metadata and sitemap entries', async t => {
  const repository = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const webRoot = path.join(repository, 'web');
  const baseline = await checkSite(webRoot);
  assert.equal(baseline.pages, 9);
  assert(!baseline.files.some(file => file.includes('vendor/') || file.endsWith('.php')));
  const artifacts = path.join(repository, 'artifacts');
  await mkdir(artifacts, { recursive: true });
  const fixture = await mkdtemp(path.join(artifacts, 'release-check-test-'));
  try {
    for (const relative of baseline.files) {
      const destination = path.join(fixture, relative);
      await mkdir(path.dirname(destination), { recursive: true });
      await copyFile(path.join(webRoot, relative), destination);
    }
    async function rejectsMutation(relative, transform, expected) {
      const file = path.join(fixture, relative);
      const original = await readFile(file, 'utf8');
      try {
        await writeFile(file, transform(original));
        await assert.rejects(checkSite(fixture), expected);
      } finally { await writeFile(file, original); }
    }
    await t.test('same-origin sharing images must exist locally', () => rejectsMutation(
      'index.html', html => html.replace('content="https://kerrco.us/assets/img/rework/social-software.jpg"', 'content="https://kerrco.us/assets/img/missing.jpg"'), /missing resource assets\/img\/missing.jpg/
    ));
    await t.test('stylesheet asset paths resolve relative to the stylesheet', () => rejectsMutation(
      'assets/css/home.css', css => css + '\n.example { background: url("../img/missing.jpg"); }', /missing resource assets\/img\/missing.jpg/
    ));
    await t.test('incorrect canonical origin is rejected', () => rejectsMutation(
      'index.html', html => html.replace('rel="canonical" href="https://kerrco.us/"', 'rel="canonical" href="https://example.com/"'), /incorrect canonical URL/
    ));
    await t.test('missing sitemap destination is rejected', () => rejectsMutation(
      'sitemap.xml', xml => xml.replace(/\s*<url><loc>https:\/\/kerrco.us\/contact.html<\/loc><\/url>/, ''), /Sitemap does not match/
    ));
    assert.equal((await checkSite(fixture)).files.length, baseline.files.length);
  } finally {
    // This is an owned fixture under ignored artifacts, never the source web root.
    if (!path.resolve(fixture).startsWith(path.resolve(artifacts) + path.sep)) throw new Error('Unexpected fixture cleanup path');
    await rm(fixture, { recursive: true });
  }
});
