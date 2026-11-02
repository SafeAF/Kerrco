import { readFile, readdir, mkdir, writeFile, copyFile, stat } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash, randomUUID } from 'node:crypto';
import { execFileSync } from 'node:child_process';

const repository = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const origin = 'https://kerrco.us';
const decode = value => value.replaceAll('&amp;', '&');
const attribute = (tag, name) => new RegExp(`\\b${name}="([^"]*)"`).exec(tag)?.[1];
const hash = bytes => createHash('sha256').update(bytes).digest('hex');

function jpegDimensions(bytes) {
  if (bytes.readUInt16BE(0) !== 0xffd8) throw new Error('Expected a JPEG image');
  let offset = 2;
  while (offset < bytes.length) {
    if (bytes[offset++] !== 0xff) throw new Error('Invalid JPEG marker');
    while (bytes[offset] === 0xff) offset++;
    const marker = bytes[offset++];
    if (marker === 0xda || marker === 0xd9) break;
    const length = bytes.readUInt16BE(offset);
    if (length < 2) throw new Error('Invalid JPEG segment length');
    if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) {
      return { height: bytes.readUInt16BE(offset + 3), width: bytes.readUInt16BE(offset + 5) };
    }
    offset += length;
  }
  throw new Error('JPEG dimensions not found');
}

export async function checkSite(webRoot = path.join(repository, 'web')) {
  const pages = (await readdir(webRoot)).filter(name => name.endsWith('.html')).sort();
  const errors = [];
  const sources = new Map();
  const files = new Set([...pages, 'robots.txt', 'sitemap.xml']);
  const titles = new Set();
  let references = 0;
  let images = 0;
  for (const page of pages) sources.set(page, await readFile(path.join(webRoot, page), 'utf8'));

  async function checkReference(raw, from) {
    references++;
    const url = new URL(decode(raw), `${origin}/${from}`);
    if (url.protocol === 'mailto:') {
      if (url.pathname !== 'kerrcoenterprises@gmail.com') errors.push(`${from}: unexpected email recipient`);
      return;
    }
    if (!['https:', 'http:'].includes(url.protocol)) { errors.push(`${from}: unsupported URL scheme`); return; }
    if (url.origin !== origin) return;
    const relative = decodeURIComponent(url.pathname).replace(/^\//, '') || 'index.html';
    const absolute = path.resolve(webRoot, relative);
    if (!absolute.startsWith(path.resolve(webRoot) + path.sep)) { errors.push(`${from}: path outside web root`); return; }
    if (!/\.(html|css|jpg|jpeg|png|svg|ico|webp|txt|xml)$/.test(relative)) { errors.push(`${from}: unexpected release asset ${relative}`); return; }
    try {
      if (!(await stat(absolute)).isFile()) throw new Error('Not a file');
      files.add(relative);
      if (url.hash) {
        const target = sources.get(relative) ?? await readFile(absolute, 'utf8');
        const ids = [...target.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
        if (!ids.includes(decodeURIComponent(url.hash.slice(1)))) errors.push(`${from}: missing anchor ${raw}`);
      }
    } catch { errors.push(`${from}: missing resource ${relative}`); }
  }

  for (const [page, html] of sources) {
    const ids = [...html.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
    if (new Set(ids).size !== ids.length) errors.push(`${page}: duplicate IDs`);
    if ([...html.matchAll(/<h1\b/g)].length !== 1) errors.push(`${page}: expected one H1`);
    const title = /<title>(.*?)<\/title>/.exec(html)?.[1];
    if (!title || titles.has(title)) errors.push(`${page}: missing or duplicate title`);
    titles.add(title);
    for (const required of ['name="description"', 'property="og:title"', 'property="og:description"', 'property="og:image"', 'href="#main"', 'aria-label="Main navigation"']) {
      if (!html.includes(required)) errors.push(`${page}: missing ${required}`);
    }
    for (const match of html.matchAll(/\b(?:href|src)="([^"]+)"/g)) await checkReference(match[1], page);
    for (const match of html.matchAll(/<meta\b[^>]*>/g)) {
      if (attribute(match[0], 'property') === 'og:image') await checkReference(attribute(match[0], 'content'), page);
    }
    for (const match of html.matchAll(/aria-labelledby="([^"]+)"/g)) {
      for (const id of match[1].split(/\s+/)) if (!ids.includes(id)) errors.push(`${page}: missing label ${id}`);
    }
    for (const match of html.matchAll(/<img\b[^>]*>/g)) {
      images++;
      const tag = match[0];
      if (!attribute(tag, 'alt')?.trim()) errors.push(`${page}: missing image description`);
      try {
        const dimensions = jpegDimensions(await readFile(path.join(webRoot, attribute(tag, 'src'))));
        if (dimensions.width !== Number(attribute(tag, 'width')) || dimensions.height !== Number(attribute(tag, 'height'))) errors.push(`${page}: image dimensions do not match ${attribute(tag, 'src')}`);
      } catch (error) { errors.push(`${page}: ${error.message}`); }
    }
    const canonicalTag = [...html.matchAll(/<link\b[^>]*>/g)].find(match => attribute(match[0], 'rel') === 'canonical')?.[0];
    if (page === '404.html') {
      if (canonicalTag || !html.includes('name="robots" content="noindex"')) errors.push('404.html: incorrect indexing metadata');
    } else if (attribute(canonicalTag ?? '', 'href') !== `${origin}/${page === 'index.html' ? '' : page}`) errors.push(`${page}: incorrect canonical URL`);
  }
  // Follow stylesheet assets as well as HTML assets when preparing the release.
  const visitedCSS = new Set();
  for (const file of files) {
    if (!file.endsWith('.css') || visitedCSS.has(file)) continue;
    visitedCSS.add(file);
    const css = await readFile(path.join(webRoot, file), 'utf8');
    for (const match of css.matchAll(/url\(\s*['"]?([^'"\s)]+)['"]?\s*\)/g)) await checkReference(match[1], file);
  }
  const sitemap = await readFile(path.join(webRoot, 'sitemap.xml'), 'utf8');
  const locations = [...sitemap.matchAll(/<loc>(.*?)<\/loc>/g)].map(match => match[1]);
  const expected = pages.filter(page => page !== '404.html').map(page => `${origin}/${page === 'index.html' ? '' : page}`);
  if (locations.length !== expected.length || new Set(locations).size !== locations.length || expected.some(url => !locations.includes(url))) errors.push('Sitemap does not match indexable pages');
  if (!(await readFile(path.join(webRoot, 'robots.txt'), 'utf8')).includes(`Sitemap: ${origin}/sitemap.xml`)) errors.push('robots.txt has no correct sitemap URL');
  if (errors.length) throw new Error(errors.join('\n'));
  return { pages: pages.length, references, images, files: [...files].sort() };
}

export async function prepareRelease() {
  const checks = await checkSite();
  const name = `website-review-${new Date().toISOString().replace(/[:.]/g, '-')}-${randomUUID().slice(0, 8)}`;
  const stage = path.join(repository, 'artifacts', name);
  await mkdir(stage, { recursive: true });
  const manifest = [];
  for (const relative of checks.files) {
    const source = path.join(repository, 'web', relative);
    const destination = path.join(stage, relative);
    await mkdir(path.dirname(destination), { recursive: true });
    await copyFile(source, destination);
    const bytes = await readFile(destination);
    manifest.push({ path: relative, bytes: bytes.length, sha256: hash(bytes) });
  }
  await writeFile(`${stage}-manifest.json`, JSON.stringify({ status: 'Local review bundle; browser and VPS checks pending', origin, checks, files: manifest }, null, 2) + '\n');
  await writeFile(`${stage}-SHA256SUMS`, manifest.map(file => `${file.sha256}  ${file.path}`).join('\n') + '\n');
  const archive = `${stage}.tar.gz`;
  execFileSync('tar', ['-czf', archive, '-C', stage, '.'], { windowsHide: true, stdio: 'pipe' });
  await writeFile(`${archive}.sha256`, `${hash(await readFile(archive))}  ${path.basename(archive)}\n`);
  return { archive, manifest: `${stage}-manifest.json`, fileChecksums: `${stage}-SHA256SUMS`, ...checks, files: manifest.length };
}

if (globalThis.process?.argv?.[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const args = process.argv.slice(2);
    if (args.some(arg => arg !== '--check')) throw new Error('Usage: node scripts/prepare-release.mjs [--check]');
    console.log(JSON.stringify(args.includes('--check') ? await checkSite() : await prepareRelease(), null, 2));
  } catch (error) { console.error(error.message); process.exitCode = 1; }
}
