/**
 * Composes the three A3 invitation pages into output/html/.
 *
 *   node src/build.mjs
 *
 * The ornament sheet is inlined into each document so a page is a single
 * self-contained file (apart from the shared CSS and the font/texture assets),
 * which keeps it openable straight from disk and importable into Figma.
 */

import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { EVENT, LETTERS, SIGNATORIES, PANEL_ICONS } from './content.js';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, '..');

const ornaments = await fs.readFile(path.join(ROOT, 'assets', 'ornaments.svg'), 'utf8');

/* ------------------------------------------------------------- fragments */

const use = (id, cls = '', extra = '') =>
  `<svg class="${cls}" viewBox="${VIEWBOX[id] || '0 0 100 100'}" ${extra}
     preserveAspectRatio="xMidYMid meet"><use href="#${id}"/></svg>`;

/* viewBoxes must match the symbols emitted by make_ornaments.py */
const VIEWBOX = {
  'orn-corner': '0 0 134 134',
  'orn-divider': '0 0 600 60',
  'orn-flourish': '0 0 120 40',
  'orn-rosette': '0 0 76 76',
  'orn-mountains': '0 0 1200 420',
  'orn-peakline': '0 0 600 96',
  'orn-pines': '0 0 140 158',
  'orn-flags': '0 0 244 96',
  'orn-dhol': '0 0 220 150',
  'orn-damau': '0 0 180 130',
  'orn-hudka': '0 0 120 170',
  'orn-ransingha': '0 0 220 140',
  'orn-bell': '0 0 120 170',
  'orn-house': '0 0 220 160',
  'orn-jewellery': '0 0 180 140',
  'orn-kalash': '0 0 110 150',
  'orn-dancers': '0 0 324 172',
  'seal-gesm': '0 0 200 200',
  'seal-swaragini': '0 0 200 200',
};

const patternFill = (patId, cls) =>
  `<svg class="${cls}" preserveAspectRatio="none"><rect width="100%" height="100%" fill="url(#${patId})"/></svg>`;

const backgroundStack = () => `
  <div class="bg">
    <div class="bg-ground"></div>
    <div class="bg-halo"></div>
    <div class="bg-mountains">${use('orn-mountains', '', 'preserveAspectRatio="none"')}</div>
    <div class="bg-motif">${patternFill('pat-aipan', '')}</div>
    <div class="bg-textile">${patternFill('pat-textile', '')}</div>
    <div class="bg-paper"></div>
    <div class="bg-grain"></div>
    <div class="bg-vignette"></div>
  </div>`;

/* what the invitation pages actually use */
const background = () => '<div class="bg-baked"></div>';

/* standalone document used to bake the stack (see: node src/render.mjs --bake) */
const backgroundDoc = () => `<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<title>Garh Kauthig 2026 &mdash; background plate</title>
<link rel="stylesheet" href="../../src/fonts.css">
<link rel="stylesheet" href="../../src/invitation.css">
</head><body>
${ornaments}
<div class="page">${backgroundStack()}</div>
<script>document.fonts.ready.then(()=>{document.body.dataset.ready='1';});</script>
</body></html>`;

const border = () => `
  <div class="frame-outer"></div>
  <div class="band top">${patternFill('pat-carving', '')}</div>
  <div class="band bottom">${patternFill('pat-carving', '')}</div>
  <div class="band left">${patternFill('pat-ringaal', '')}</div>
  <div class="band right">${patternFill('pat-ringaal', '')}</div>
  <div class="frame-mid"></div>
  <div class="corner tl">${use('orn-corner')}</div>
  <div class="corner tr">${use('orn-corner')}</div>
  <div class="corner bl">${use('orn-corner')}</div>
  <div class="corner br">${use('orn-corner')}</div>`;

const masthead = () => `
  <header class="masthead">
    <div class="host-line">${EVENT.university.toUpperCase()} &middot; ${EVENT.city.toUpperCase()}</div>

    <div class="logo-row">
      <div class="logo-unit">
        ${use('seal-gesm')}
        <div class="logo-name">GRAPHIC ERA<br>SCHOOL OF MANAGEMENT</div>
      </div>
      <div class="logo-div"></div>
      <div class="logo-unit">
        ${use('seal-swaragini')}
        <div class="logo-name">SWARAGINI</div>
        <div class="logo-sub">The Cultural Society of Graphic Era University</div>
      </div>
    </div>

    <div class="programme">
      <span class="seg"></span>
      <span class="txt">${EVENT.programme}</span>
      <span class="seg"></span>
    </div>
    <div class="programme-tag"><span class="tag">${EVENT.programmeTag}</span></div>

    <div class="title-deva">${EVENT.nameDevanagari}</div>
    <h1 class="title-main"><span class="face press-red">${EVENT.name}</span></h1>
    <div class="title-year">
      <span class="wing"></span>
      <span class="yr emboss-pair">
        <span class="under" aria-hidden="true">${EVENT.year}</span>
        <span class="face foil">${EVENT.year}</span>
      </span>
      <span class="wing"></span>
    </div>

    <div class="theme-line">${EVENT.theme}</div>
    <div class="divider">${use('orn-divider')}</div>
  </header>`;

const panel = () => `
  <aside class="panel">
    <div class="panel-weave">${patternFill('pat-ringaal', '')}</div>
    <div class="panel-title">${EVENT.name.toUpperCase()} &middot; ${EVENT.year}</div>
    <div class="panel-icons">
      ${PANEL_ICONS.map((id, i) => `
        ${use(id, 'ico')}
        ${i < PANEL_ICONS.length - 1 ? '<span class="bead"></span>' : ''}`).join('')}
    </div>
    <div class="panel-rosette">${use('orn-rosette')}</div>
    <div class="panel-glance">
      <div class="sep"></div>
      <div class="lbl">AT A GLANCE</div>
      <div class="item">${EVENT.dateShort}</div>
      <div class="sep"></div>
      <div class="item">${EVENT.timeShort}</div>
      <div class="sep"></div>
      <div class="item">${EVENT.venueShort}</div>
      <div class="sep"></div>
    </div>
  </aside>`;

const infobox = () => `
  <section class="infobox">
    <div class="cap">THE OCCASION</div>
    <div class="grid">
      <div class="col">
        <div class="row"><span class="k">EVENT</span>
          <span class="v">${EVENT.name} ${EVENT.year}</span></div>
        <div class="row"><span class="k">THEME</span>
          <span class="v"><em>${EVENT.theme}</em></span></div>
        <div class="row"><span class="k">PROGRAMME</span>
          <span class="v">EMERGE &mdash; Induction Program 2026</span></div>
      </div>
      <div class="vrule"></div>
      <div class="col">
        <div class="row"><span class="k">DATE</span>
          <span class="v">${EVENT.date}</span></div>
        <div class="row"><span class="k">TIME</span>
          <span class="v">${EVENT.time}</span></div>
        <div class="row"><span class="k">VENUE</span>
          <span class="v">${EVENT.venue},<br>${EVENT.venueSub}</span></div>
      </div>
      <div class="wide">
        <span class="k">ORGANISED BY</span>
        <span class="v">${EVENT.hostA} &nbsp;&middot;&nbsp; ${EVENT.hostBFull}</span>
      </div>
    </div>
  </section>`;

const signatures = () => `
  <div class="signatures">
    ${SIGNATORIES.map((s) => `
      <div class="sig">
        <div class="line"></div>
        <div class="role">${s.role}</div>
        <div class="org">${s.org}</div>
      </div>`).join('')}
  </div>`;

const footer = () => `
  <footer class="footer">
    <div class="footer-rule">
      <span class="seg"></span>
      ${use('orn-peakline')}
      <span class="seg r"></span>
    </div>
    <div class="footer-hosts">
      <span>${EVENT.hostA.toUpperCase()}</span>
      <span class="dot">&#10022;</span>
      <span>${EVENT.hostB.toUpperCase()}</span>
    </div>
    <div class="footer-addr">
      ${EVENT.university}, ${EVENT.city}, ${EVENT.state}
    </div>
  </footer>`;

const letterBody = (L) => `
  <div class="letter" data-fit="letter">
    <div class="meta">
      <span>REF. NO. <span class="val">${L.ref}</span></span>
      <span>DATE <span class="dotfill"></span></span>
    </div>

    <div class="recipient">
      <span class="to">TO,</span>
      <span class="name">${L.namePrefix ? L.namePrefix + ' ' : ''}<span class="dotfill" style="min-width:64mm"></span></span>
      <span class="desig">The ${L.designation}</span>
      <span class="org">${EVENT.university}, ${EVENT.city}, ${EVENT.state}</span>
    </div>

    <div class="subject">
      <span class="lbl">SUBJECT&nbsp;&mdash;&nbsp;</span>${L.subject}
    </div>

    <div class="salutation">${L.salutation}</div>

    <div class="body-copy lead">
      ${L.paras.slice(0, 2).map((p) => `<p>${p}</p>`).join('')}
    </div>

    <div class="pull">
      <span class="quote"><span class="mark">&ldquo;</span>${EVENT.theme}<span class="mark">&rdquo;</span></span>
      <span class="attrib">THE THEME OF GARH KAUTHIG ${EVENT.year}</span>
    </div>

    <div class="body-copy">
      ${L.paras.slice(2).map((p) => `<p>${p}</p>`).join('')}
    </div>

    <div class="closing-mark">${use('orn-flourish')}</div>

    <div class="signoff">
      <div class="valediction">
        <span class="close">${L.valediction}</span>
      </div>
      ${signatures()}
    </div>

    ${infobox()}
  </div>`;

const page = (L) => `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Garh Kauthig 2026 &mdash; Invitation to the ${L.designation}</title>
<link rel="stylesheet" href="../../src/fonts.css">
<link rel="stylesheet" href="../../src/invitation.css">
</head>
<body>
${ornaments}
<div class="page">
  ${background()}
  <div class="trim">
    ${border()}
    <div class="stage" data-fit="stage">
      ${masthead()}
      <div class="middle">
        ${panel()}
        ${letterBody(L)}
      </div>
      ${footer()}
    </div>
  </div>
</div>
<script>
  document.fonts.ready.then(() => { document.body.dataset.ready = '1'; });
</script>
</body>
</html>`;

/* ------------------------------------------------------------------ write */
const outDir = path.join(ROOT, 'output', 'html');
await fs.mkdir(outDir, { recursive: true });
await fs.writeFile(path.join(outDir, '_background-plate.html'), backgroundDoc(), 'utf8');
console.log('built', path.join('output', 'html', '_background-plate.html'));

for (const L of LETTERS) {
  const file = path.join(outDir, `garh-kauthig-2026-invitation-${L.id}.html`);
  await fs.writeFile(file, page(L), 'utf8');
  console.log('built', path.relative(ROOT, file));
}
