/* ==========================================================================
   Content for the Garh Kauthig 2026 invitation suite.
   --------------------------------------------------------------------------
   EVENT is transcribed strictly from the supplied A3 poster.  Nothing here is
   invented: the poster carries no dress code, no contact details and no
   session-by-session schedule, so those fields are simply absent rather than
   filled with plausible guesses.  Anything a sender must complete by hand
   (recipient's name, dispatch date) is rendered as a dotted rule.
   ========================================================================== */

export const EVENT = {
  name: 'Garh Kauthig',
  nameDevanagari: 'गढ़ कौथिग',
  year: '2026',
  theme: 'Tradition, Togetherness, and Timeless Culture',
  date: 'Thursday, 13 August 2026',
  dateShort: '13 AUGUST 2026',
  time: '01:00 PM onwards',
  timeShort: '01:00 PM ONWARDS',
  venue: 'Silver Jubilee Convention Centre',
  venueSub: 'Graphic Era (Deemed to be University)',
  venueShort: 'SILVER JUBILEE CONVENTION CENTRE',
  programme: 'EMERGE \u00b7 INDUCTION PROGRAM 2026',
  programmeTag: 'Discover. Connect. Excel.',
  university: 'Graphic Era (Deemed to be University)',
  city: 'Dehradun',
  state: 'Uttarakhand',
  hostA: 'Graphic Era School of Management',
  hostB: 'Swaragini',
  hostBFull: 'Swaragini \u2014 The Cultural Society of Graphic Era University',
};

/* Signature placeholders, common to all three letters. */
export const SIGNATORIES = [
  { role: 'Event Coordinator', org: 'Garh Kauthig 2026' },
  { role: 'Program Coordinator', org: 'EMERGE Induction Program 2026' },
  { role: 'Faculty Coordinator', org: 'Swaragini \u2014 Cultural Society' },
  { role: 'Head', org: 'Graphic Era School of Management' },
];

/* The decorative side panel: motif icons, top to bottom. */
export const PANEL_ICONS = ['orn-dhol', 'orn-dancers', 'orn-ransingha', 'orn-bell'];

/* --------------------------------------------------------------------------
   The three letters.  Each is written to a different register, as briefed:
   the Registrar's is administrative, the Vice Chancellor's is visionary, the
   Pro Vice Chancellor's is warm and student-facing.

   Note on protocol: the poster does not name a Chief Guest or an Inaugural
   Guest, so no letter assigns that role.  All three use neutral ceremonial
   wording -- "grace the occasion with your esteemed presence".
   -------------------------------------------------------------------------- */

export const LETTERS = [
  {
    id: '01-vice-chancellor',
    ref: 'GESM / SWG / GK-2026 / INV / VC-01',
    designation: 'Vice Chancellor',
    namePrefix: 'Prof. (Dr.)',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; a celebration of Garhwali heritage',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'It would be our great privilege to welcome you to <strong>Garh Kauthig 2026</strong> &mdash; ' +
      'an afternoon of Garhwali music, dance and celebration at the Silver Jubilee Convention Centre ' +
      'on Thursday, 13 August 2026, from 01:00 PM onwards.',

      'A <em>kauthig</em> is how the hills celebrate together. When the dhol and damau begin, the whole ' +
      'village gathers, the old songs are sung again, and everyone belongs. That is the spirit we hope ' +
      'to bring onto our campus.',

      'We have placed the festival at the very start of the academic year, within the EMERGE Induction ' +
      'Program 2026. Most of the students performing have only just joined us, and in learning the ' +
      'music of their own hills and sharing it with their classmates, they find something of where they ' +
      'come from &mdash; and of the University they now belong to. Your presence would mean a great ' +
      'deal to every one of them, and we warmly invite you to grace the occasion with your esteemed ' +
      'presence.',
    ],
    valediction: 'With warm regards and deep respect,',
  },

  {
    id: '02-pro-vice-chancellor',
    ref: 'GESM / SWG / GK-2026 / INV / PVC-02',
    designation: 'Pro Vice Chancellor',
    namePrefix: 'Prof. (Dr.)',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; and to cheer on our student performers',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'We would be delighted to have you with us at <strong>Garh Kauthig 2026</strong>, our celebration ' +
      'of Garhwali folk tradition, at the Silver Jubilee Convention Centre on Thursday, 13 August 2026, ' +
      'from 01:00 PM onwards.',

      'Almost everything you will see has been put together by the students themselves. They chose the ' +
      'songs and set the choreography, gathered the traditional attire and ornaments, found the ' +
      'drummers, and stayed back long after class to rehearse.',

      'Much of it has happened across the lines we usually draw &mdash; between seniors and freshers, ' +
      'between programmes, between those who grew up with these traditions and those meeting them for ' +
      'the first time. That, as much as the performance itself, is what we are proud of. A few words of ' +
      'encouragement from you would stay with them long after the applause, and we warmly invite you to ' +
      'grace the occasion with your esteemed presence.',
    ],
    valediction: 'With warm regards,',
  },

  {
    id: '03-registrar',
    ref: 'GESM / SWG / GK-2026 / INV / REG-03',
    designation: 'Registrar',
    namePrefix: '',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; a celebration of Uttarakhand&rsquo;s folk heritage',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'It is our pleasure to invite you to <strong>Garh Kauthig 2026</strong>, a celebration of the folk ' +
      'heritage of Uttarakhand held as part of the EMERGE Induction Program 2026, at the Silver Jubilee ' +
      'Convention Centre on Thursday, 13 August 2026, from 01:00 PM onwards.',

      'Students from across our programmes have come together for it &mdash; taking charge of the music ' +
      'and dance, the traditional attire and ornamentation, and the running of the afternoon itself. It ' +
      'is a happy thing to see an event of this size resting so largely in their hands.',

      'These traditions live on only by being performed. The dhol and damau, the hudka and the ' +
      'ransingha, and the songs that go with them are handed on each time a young audience hears them. ' +
      'That is exactly what we hope this afternoon will do. We would be honoured to have you with us, ' +
      'and warmly invite you to grace the occasion with your esteemed presence.',
    ],
    valediction: 'With warm regards,',
  },
];
