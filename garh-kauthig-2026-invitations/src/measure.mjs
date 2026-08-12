/** Reports the height of every major block in mm, to tune the A3 vertical budget. */
import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import http from 'node:http';
import { createReadStream } from 'node:fs';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');
const MIME = { '.html': 'text/html', '.css': 'text/css', '.svg': 'image/svg+xml',
  '.png': 'image/png', '.ttf': 'font/ttf', '.js': 'text/javascript' };

const server = http.createServer(async (req, res) => {
  const file = path.join(ROOT, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  try {
    await fs.stat(file);
    res.writeHead(200, { 'Content-Type': MIME[path.extname(file)] || 'application/octet-stream' });
    createReadStream(file).pipe(res);
  } catch { res.writeHead(404).end(); }
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const origin = `http://127.0.0.1:${server.address().port}`;

const target = process.argv[2] || 'garh-kauthig-2026-invitation-01-vice-chancellor.html';
const browser = await puppeteer.launch({ headless: 'shell', args: ['--no-sandbox'] });
const tab = await browser.newPage();
await tab.setViewport({ width: 1146, height: 1611 });
await tab.goto(`${origin}/output/html/${target}`, { waitUntil: 'networkidle0' });
await tab.evaluate(() => document.fonts.ready);

const rows = await tab.evaluate(() => {
  const PX = 96 / 25.4;
  const mm = (v) => Math.round((v / PX) * 10) / 10;
  const sel = ['.stage', '.masthead', '.host-line', '.logo-row', '.programme', '.title-deva',
    '.title-main', '.title-year', '.theme-line', '.divider', '.middle', '.panel', '.letter',
    '.meta', '.recipient', '.subject', '.salutation', '.body-copy.lead', '.pull',
    '.body-copy:not(.lead)', '.valediction', '.signatures', '.infobox', '.footer'];
  const out = [];
  for (const s of sel) {
    const el = document.querySelector(s);
    if (!el) { out.push([s, 'MISSING']); continue; }
    const r = el.getBoundingClientRect();
    out.push([s, mm(r.height), mm(r.top), mm(el.scrollHeight)]);
  }
  const st = document.querySelector('.stage');
  out.push(['STAGE client/scroll', mm(st.clientHeight), mm(st.scrollHeight)]);
  const lt = document.querySelector('.letter');
  out.push(['LETTER client/scroll', mm(lt.clientHeight), mm(lt.scrollHeight)]);
  return out;
});
for (const r of rows) console.log(r.map(String).map((v) => v.padEnd(9)).join(' '));
await browser.close();
server.close();
