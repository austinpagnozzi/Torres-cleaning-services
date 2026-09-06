#!/usr/bin/env node
/* Inline the stylesheet and script into index.html to produce one
   self-contained file that opens with no server and no network.

   Usage: node scripts/build-artifact.mjs [outfile]
          node scripts/build-artifact.mjs --fragment   (no <html>/<head>/<body>)
*/

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const args = process.argv.slice(2);
const fragment = args.includes('--fragment');
const outArg = args.find((a) => !a.startsWith('--'));
const out = resolve(root, outArg ?? (fragment ? 'dist/torres-homepage.fragment.html' : 'dist/torres-homepage.html'));

const html = await readFile(resolve(root, 'index.html'), 'utf8');
let css    = await readFile(resolve(root, 'assets/css/styles.css'), 'utf8');
const js   = await readFile(resolve(root, 'assets/js/main.js'), 'utf8');

// Inline the generated photography as data URIs, referenced from both the
// stylesheet (relative to assets/css/) and the HTML (relative to the repo
// root), so the single-file build has no external asset dependencies.
const mime = (file) => (file.endsWith('.png') ? 'image/png' : 'image/jpeg');

async function dataUri(relativeTo, ref) {
  const abs = resolve(relativeTo, ref);
  const buf = await readFile(abs);
  return `data:${mime(abs)};base64,${buf.toString('base64')}`;
}

for (const match of [...css.matchAll(/url\("(\.\.\/img\/[^"]+)"\)/g)]) {
  const uri = await dataUri(resolve(root, 'assets/css'), match[1]);
  css = css.replace(match[0], `url("${uri}")`);
}

let html2 = html;
for (const match of [...html.matchAll(/src="(assets\/img\/[^"]+)"/g)]) {
  const uri = await dataUri(root, match[1]);
  html2 = html2.replace(match[0], `src="${uri}"`);
}

let result = html2
  .replace('<link rel="stylesheet" href="assets/css/styles.css">', `<style>\n${css}\n</style>`)
  .replace('<script src="assets/js/main.js"></script>', `<script>\n${js}\n</script>`);

if (result.includes('assets/css/styles.css') || result.includes('assets/js/main.js')) {
  throw new Error('Inlining failed — the <link>/<script> tags in index.html no longer match.');
}

if (fragment) {
  // Strip the document shell for hosts that supply their own <head>/<body>.
  const title = (result.match(/<title>([\s\S]*?)<\/title>/) || [])[1] ?? '';
  const head  = result.slice(result.indexOf('<head>') + 6, result.indexOf('</head>'));
  const body  = result.slice(result.indexOf('<body>') + 6, result.lastIndexOf('</body>'));
  const keep  = head
    .split('\n')
    .filter((l) => /<style>|<\/style>|font|^\s*$/.test(l) || l.includes('--') || !/^\s*<(meta|link|title)/.test(l))
    .join('\n');
  result = `<title>${title}</title>\n${keep}\n${body}`;
}

await mkdir(dirname(out), { recursive: true });
await writeFile(out, result);
console.log(`Wrote ${out} (${(Buffer.byteLength(result) / 1024).toFixed(1)} KB)`);
