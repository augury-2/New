/**
 * Renders the designed A4 programme sheet to PDF and a preview JPEG.
 *
 *   node render.mjs
 *
 * Served over localhost rather than file:// so the shared fonts in the
 * invitation project load, and checked for overflow before it is written.
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs';
import http from 'node:http';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..');
const NAME = 'garh-kauthig-2026-itinerary';

const MIME = { '.html': 'text/html', '.css': 'text/css', '.ttf': 'font/ttf',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };

const server = http.createServer((req, res) => {
  const file = path.join(REPO, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!file.startsWith(REPO)) { res.writeHead(403).end(); return; }
  try {
    fs.statSync(file);
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream' });
    fs.createReadStream(file).pipe(res);
  } catch { res.writeHead(404).end('not found'); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const origin = `http://127.0.0.1:${server.address().port}`;

const browser = await puppeteer.launch({
  headless: 'shell',
  args: ['--no-sandbox', '--font-render-hinting=none', '--force-color-profile=srgb'],
});
const tab = await browser.newPage();
const problems = [];
tab.on('pageerror', (e) => problems.push(String(e)));
tab.on('requestfailed', (r) => problems.push(`FAILED ${r.url()}`));

await tab.setViewport({ width: 794, height: 1123, deviceScaleFactor: 1 });
await tab.goto(`${origin}/${path.basename(HERE)}/${NAME}.html`, { waitUntil: 'networkidle0' });
await tab.evaluate(() => document.fonts.ready);
await tab.waitForFunction(() => document.body.dataset.ready === '1', { timeout: 15000 })
  .catch(() => problems.push('fonts never signalled ready'));
await new Promise((r) => setTimeout(r, 250));

const fit = await tab.evaluate(() => {
  const s = document.querySelector('.sheet');
  const i = document.querySelector('.inner');
  return { sheet: s.scrollHeight, sheetClient: s.clientHeight,
           inner: i.scrollHeight, innerClient: i.clientHeight };
});
if (fit.inner - fit.innerClient > 2 || fit.sheet - fit.sheetClient > 2) {
  console.log('  ! content overflows the sheet:', JSON.stringify(fit));
} else {
  console.log('  fits: inner', fit.inner, '/', fit.innerClient, 'px');
}

await tab.pdf({ path: path.join(HERE, `${NAME}.pdf`), width: '210mm', height: '297mm',
  printBackground: true, preferCSSPageSize: true, pageRanges: '1',
  margin: { top: 0, right: 0, bottom: 0, left: 0 } });
console.log('  pdf ->', `${NAME}.pdf`);

await tab.setViewport({ width: 794, height: 1123, deviceScaleFactor: 2.4 });
await new Promise((r) => setTimeout(r, 200));
await tab.screenshot({ path: path.join(HERE, `${NAME}-preview.jpg`), type: 'jpeg', quality: 88 });
console.log('  preview ->', `${NAME}-preview.jpg`);

if (problems.length) console.log('  ! problems:', problems.slice(0, 5));
await browser.close();
server.close();
