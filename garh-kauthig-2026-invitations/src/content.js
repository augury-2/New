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
  programmeTag: 'Discover. Connect. Excel.',
  university: 'Graphic Era (Deemed to be University)',
  city: 'Dehradun',
  state: 'Uttarakhand',
  hostA: 'Graphic Era School of Management',
  hostB: 'Swaragini',
  hostBFull: 'Swaragini \u2014 The Cultural Society of Graphic Era University',
};

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
    designation: 'Vice Chancellor',
    addressee: 'The Vice Chancellor',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; a celebration of Garhwali heritage',
    salutation: 'Respected Sir,',
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
    designation: 'Pro Vice Chancellor',
    addressee: 'The Pro Vice Chancellor',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; and to cheer on our student performers',
    salutation: 'Respected Sir,',
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
    designation: 'Registrar',
    addressee: 'The Registrar',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; a celebration of Uttarakhand&rsquo;s folk heritage',
    salutation: 'Respected Sir,',
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
  /* ------------------------------------------------------------------------
     Invitations to the wider University community.  These are written to be
     read for pleasure rather than filed, so the register is warmer and more
     figurative than the three official letters above -- but the facts, the
     date, time, venue and programme, are the same and still come only from
     the poster.
     ------------------------------------------------------------------------ */

  {
    id: '04-faculty-members',
    designation: 'Faculty Members',
    addressee: 'Respected Faculty Members',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; an afternoon of Garhwali music, ' +
      'dance and celebration',
    salutation: 'Respected Sir / Madam,',
    paras: [
      'There is a moment, somewhere in the middle of a <em>kauthig</em>, when the dhol finds its ' +
      'rhythm and a room stops being an audience. We would be honoured to have you there for it ' +
      '&mdash; at the Silver Jubilee Convention Centre on Thursday, 13 August 2026, from 01:00 PM ' +
      'onwards.',

      'You know these students from the lecture hall: hands raised, deadlines negotiated, ' +
      'presentations survived. <strong>Garh Kauthig</strong> offers quite another view of them ' +
      '&mdash; in traditional attire, drumming the dhol and damau, singing the songs their ' +
      'grandmothers sang.',

      'Do come, and be celebrated as much as the performers are. The hills will be loud, the ' +
      'colours bright, and the afternoon will not feel complete without you.',
    ],
    valediction: 'With warm regards and deep respect,',
  },

  {
    id: '05-research-scholars',
    designation: 'Research Scholars',
    addressee: 'Research Scholars',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; where the hills are both the subject ' +
      'and the source',
    salutation: 'Dear Research Scholars,',
    paras: [
      'Much of what a scholar chases through an archive, a <em>kauthig</em> keeps alive in a ' +
      'courtyard. On Thursday, 13 August 2026, from 01:00 PM onwards, the Silver Jubilee ' +
      'Convention Centre becomes exactly that courtyard, and we would be delighted if you joined ' +
      'us in it.',

      'The dhol and damau, the hudka, the ransingha, the jhora circle that closes only when the ' +
      'last dancer joins it &mdash; at <strong>Garh Kauthig 2026</strong> these are not exhibits. ' +
      'They are a living tradition, performed by students who learned them at home rather than ' +
      'from a reading list.',

      'Come for the scholarship of it, or simply for the afternoon. Either way there is a seat ' +
      'waiting, and a great deal of colour to fill it with.',
    ],
    valediction: 'With warm regards,',
  },

  {
    id: '06-mba-seniors-2025-27',
    designation: 'MBA 2025-27 Batch',
    addressee: 'MBA 2025&ndash;27 \u00b7 Seniors',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; your stage, and your welcome to give',
    salutation: 'Dear Seniors,',
    paras: [
      'This time last year somebody else was holding the door open for you. On Thursday, ' +
      '13 August 2026, from 01:00 PM onwards, at the Silver Jubilee Convention Centre, it is your ' +
      'turn &mdash; and <strong>Garh Kauthig</strong> is how we do it.',

      'So take the stage. Teach a step to someone who has never danced it. Cheer loudest for the ' +
      'fresher whose hands are shaking before their first performance: a year ago that was you, ' +
      'and somebody cheered.',

      'Come in your finest, come early, and come ready to make some noise. The hills always sound ' +
      'better when there are more of us singing.',
    ],
    valediction: 'With warm regards,',
  },

  {
    id: '07-mba-freshers-2026-28',
    designation: 'MBA 2026-28 Batch',
    addressee: 'MBA 2026&ndash;28 \u00b7 Freshers',
    subject:
      'An invitation to <em>Garh Kauthig 2026</em> &mdash; your first celebration as one of us',
    salutation: 'Dear Friends,',
    paras: [
      'Welcome. You have barely unpacked and already there is a festival. On Thursday, ' +
      '13 August 2026, from 01:00 PM onwards, at the Silver Jubilee Convention Centre, ' +
      '<strong>Garh Kauthig</strong> is where Graphic Era stops being a campus you joined and ' +
      'starts being a place you belong to.',

      'Some of you grew up with the dhol and damau. Some of you will hear them properly for the ' +
      'first time. By the end of the afternoon it will be difficult to tell which of you was ' +
      'which &mdash; and that, more or less, is the whole point of a <em>kauthig</em>.',

      'So wear something bright, learn a step, and sing the chorus even if you do not know the ' +
      'words yet. Nobody does at first. We are very glad you are here.',
    ],
    valediction: 'With warm regards,',
  },
];
