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
      'Invitation to grace <em>Garh Kauthig 2026</em> &mdash; a celebration of Garhwali heritage',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'With the deepest respect, the Graphic Era School of Management and Swaragini &mdash; The ' +
      'Cultural Society of Graphic Era University request the honour of your presence at ' +
      '<strong>Garh Kauthig 2026</strong>, a festival of Garhwali music, dance and living tradition, ' +
      'at the Silver Jubilee Convention Centre on Thursday, 13 August 2026, from 01:00 PM onwards.',

      'A <em>kauthig</em> has never been merely a gathering. In the hills of Uttarakhand it is the ' +
      'occasion on which a community renews itself &mdash; where the dhol and damau summon the ' +
      'village, and the elder&rsquo;s song passes to the young. To bring it onto our campus is to ' +
      'affirm that a university is a custodian of culture as much as of knowledge.',

      'We have placed the festival at the threshold of the academic year, within the EMERGE Induction ' +
      'Program 2026, so that students newly arrived may discover at the outset that education is ' +
      'inseparable from identity, and that a nation&rsquo;s values endure in what each generation ' +
      'chooses to remember. Your presence would give the endeavour its fullest meaning, and we ' +
      'request you most earnestly to grace the occasion with your esteemed presence.',
    ],
    valediction: 'With profound respect and warm regards,',
  },

  {
    id: '02-pro-vice-chancellor',
    ref: 'GESM / SWG / GK-2026 / INV / PVC-02',
    designation: 'Pro Vice Chancellor',
    namePrefix: 'Prof. (Dr.)',
    subject:
      'Invitation to grace <em>Garh Kauthig 2026</em> and encourage our student performers',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'It is with genuine warmth that the Graphic Era School of Management and Swaragini &mdash; The ' +
      'Cultural Society of Graphic Era University invite you to <strong>Garh Kauthig 2026</strong>, ' +
      'our celebration of Garhwali folk tradition, at the Silver Jubilee Convention Centre on ' +
      'Thursday, 13 August 2026, from 01:00 PM onwards.',

      'What we place before you has been built by the students themselves. They chose the songs and ' +
      'set the choreography, gathered the traditional attire and ornaments, sought out the drummers, ' +
      'and kept rehearsal hours long after class. The creativity is theirs, and so is the quiet ' +
      'leadership that held it together.',

      'Much of it was done across the boundaries we usually observe &mdash; between seniors and freshers, ' +
      'between programmes, between those raised in these traditions and those meeting them for the ' +
      'first time. We would be delighted if you could grace the occasion with your esteemed presence ' +
      'and offer our participants a few words of encouragement, which for students beginning their ' +
      'journey here outlast the applause.',
    ],
    valediction: 'With sincere respect and warm regards,',
  },

  {
    id: '03-registrar',
    ref: 'GESM / SWG / GK-2026 / INV / REG-03',
    designation: 'Registrar',
    namePrefix: '',
    subject:
      'Invitation to grace <em>Garh Kauthig 2026</em>, a celebration of Uttarakhand&rsquo;s folk heritage',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'On behalf of the Graphic Era School of Management and Swaragini &mdash; The Cultural Society of ' +
      'Graphic Era University, it is our privilege to invite you to <strong>Garh Kauthig 2026</strong>, ' +
      'a celebration of the folk heritage of Uttarakhand, at the Silver Jubilee Convention Centre on ' +
      'Thursday, 13 August 2026, from 01:00 PM onwards.',

      'The festival has been organised with wide participation from across our programmes. Students ' +
      'have taken charge of the folk music and dance presentations, of traditional attire and ' +
      'ornamentation, and of the conduct of the afternoon&rsquo;s proceedings &mdash; a matter of ' +
      'considerable institutional pride.',

      'Our purpose is preservation as much as celebration: the dhol and damau, the hudka and the ' +
      'ransingha survive chiefly through performance, and every occasion on which they are presented ' +
      'to a young audience is one on which they are handed forward. We should be deeply honoured if ' +
      'you would grace the occasion with your esteemed presence.',
    ],
    valediction: 'With respectful regards,',
  },
];
