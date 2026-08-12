/**
 * Renderer for the Garh Kauthig 2026 invitation suite.
 *
 *   node src/render.mjs                 -> render all three invitations
 *   node src/render.mjs --proof         -> render the ornament proof sheet
 *   node src/render.mjs --png-only      -> skip PDF generation
 *
 * PDFs come out of Chromium as true vector (live text + vector ornament), sized
 * 303 x 426 mm = A3 plus a 3 mm bleed on every edge.  PNGs are rasterised at
 * 300 DPI for on-screen review and for placing into Photoshop/Canva.
 */

import puppeteer from 'puppeteer';
import path from 'node:path';
import fs from 'node:fs/promises';
import http from 'node:http';
import { createReadStream } from 'node:fs';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

/* Chromium refuses fetch() and some font/asset reads over file://, so the whole
   project is served from a throwaway localhost origin while rendering. */
const MIME = {
  '.html': 'text/html', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg', '.ttf': 'font/ttf', '.woff2': 'font/woff2',
  '.json': 'application/json',
};

function serve(root) {
  return new Promise((resolve) => {
    const server = http.createServer(async (req, res) => {
      const rel = decodeURIComponent(new URL(req.url, 'http://x').pathname);
      const file = path.join(root, rel);
      if (!file.startsWith(root)) { res.writeHead(403).end(); return; }
      try {
        const st = await fs.stat(file);
        if (st.isDirectory()) { res.writeHead(404).end(); return; }
        res.writeHead(200, {
          'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream',
          'Cache-Control': 'no-store',
        });
        createReadStream(file).pipe(res);
      } catch { res.writeHead(404).end('not found'); }
    });
    server.listen(0, '127.0.0.1', () => resolve({ server, port: server.address().port }));
  });
}

const MM_PER_IN = 25.4;
const CSS_DPI = 96;
const TARGET_DPI = 300;
const mm2px = (mm) => (mm / MM_PER_IN) * CSS_DPI;

const BLEED_W = 303; // A3 297 + 3 mm bleed each side
const BLEED_H = 426; // A3 420 + 3 mm bleed each side

const args = process.argv.slice(2);
const bakeMode = args.includes('--bake');
const proofMode = args.includes('--proof');
const pngOnly = args.includes('--png-only');
const pdfOnly = args.includes('--pdf-only');

async function main() {
  const { server, port } = await serve(ROOT);
  const origin = `http://127.0.0.1:${port}`;
  const browser = await puppeteer.launch({
    headless: 'shell',
    args: ['--no-sandbox', '--font-render-hinting=none', '--disable-lcd-text',
           '--force-color-profile=srgb', '--allow-file-access-from-files'],
  });

  let jobs;
  if (proofMode) {
    jobs = [{ url: `${origin}/src/proof.html`, name: 'ornament-proof', w: 1200, h: 3000, page: false }];
  } else if (bakeMode) {
    /* bake the background stack to a flat 300 dpi plate */
    jobs = [{ url: `${origin}/output/html/_background-plate.html`, name: 'background',
              page: true, bake: true }];
  } else {
    jobs = (await fs.readdir(path.join(ROOT, 'output', 'html')))
      .filter((f) => f.endsWith('.html') && !f.startsWith('_')).sort()
      .map((f) => ({
        url: `${origin}/output/html/${f}`,
        name: f.replace(/\.html$/, ''),
        page: true,
      }));
  }

  if (!jobs.length) {
    console.error('nothing to render - run `node src/build.mjs` first');
    process.exit(1);
  }

  for (const job of jobs) {
    const tab = await browser.newPage();
    const problems = [];
    tab.on('console', (m) => { if (m.type() === 'error') problems.push(m.text()); });
    tab.on('pageerror', (e) => problems.push(String(e)));
    tab.on('requestfailed', (r) => problems.push(`FAILED ${r.url()}`));

    const vw = job.page ? Math.round(mm2px(BLEED_W)) : job.w;
    const vh = job.page ? Math.round(mm2px(BLEED_H)) : job.h;
    await tab.setViewport({ width: vw, height: vh, deviceScaleFactor: 1 });
    await tab.goto(job.url, { waitUntil: 'networkidle0' });
    await tab.evaluate(() => document.fonts.ready);
    await tab.waitForFunction(() => document.body.dataset.ready === '1', { timeout: 20000 })
      .catch(() => problems.push('ready flag never set'));
    await new Promise((r) => setTimeout(r, 350));

    // --- geometry self-check: nothing may overflow the printable frame -----
    if (job.page) {
      const report = await tab.evaluate(() => {
        const out = { overflow: [], page: null };
        const pg = document.querySelector('.page');
        if (pg) out.page = { w: pg.getBoundingClientRect().width, h: pg.getBoundingClientRect().height };
        document.querySelectorAll('[data-fit]').forEach((el) => {
          if (el.scrollHeight - el.clientHeight > 1.5) {
            out.overflow.push({ sel: el.dataset.fit, scroll: el.scrollHeight, client: el.clientHeight });
          }
        });
        return out;
      });
      if (report.overflow.length) {
        console.log(`  ! ${job.name} overflow:`, JSON.stringify(report.overflow));
      }
    }

    if (job.bake) {
      await tab.setViewport({ width: vw, height: vh, deviceScaleFactor: TARGET_DPI / CSS_DPI });
      await new Promise((r) => setTimeout(r, 400));
      const out = path.join(ROOT, 'assets', 'background.png');
      await tab.screenshot({ path: out, captureBeyondViewport: false, optimizeForSpeed: false });
      console.log('  baked ->', path.relative(ROOT, out));
      if (problems.length) console.log('  ! console:', problems.slice(0, 6));
      await tab.close();
      continue;
    }

    if (!pngOnly) {
      const pdfPath = path.join(ROOT, 'output', 'pdf', `${job.name}.pdf`);
      if (job.page) {
        await tab.pdf({
          path: pdfPath,
          width: `${BLEED_W}mm`,
          height: `${BLEED_H}mm`,
          printBackground: true,
          margin: { top: 0, right: 0, bottom: 0, left: 0 },
          preferCSSPageSize: true,
          pageRanges: '1',
        });
        console.log('  pdf ->', path.relative(ROOT, pdfPath));
      }
    }

    if (!pdfOnly) {
      const pngPath = path.join(ROOT, 'output', 'png', `${job.name}.png`);
      await tab.setViewport({
        width: vw, height: vh,
        deviceScaleFactor: job.page ? TARGET_DPI / CSS_DPI : 1,
      });
      await new Promise((r) => setTimeout(r, 200));
      await tab.screenshot({ path: pngPath, fullPage: !job.page, captureBeyondViewport: false });
      console.log('  png ->', path.relative(ROOT, pngPath));
    }

    if (problems.length) console.log('  ! console:', problems.slice(0, 6));
    await tab.close();
  }

  await browser.close();
  server.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
