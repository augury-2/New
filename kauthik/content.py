"""
KAUTHIK — Content
=================
All researched copy, structured data and speaker notes for the deck.

Sourcing note: every factual claim here is drawn from the references listed
in SOURCES. Where a figure is contested or an etymology is a scholarly
reading rather than a settled fact, the copy says so on the slide.
"""

from __future__ import annotations

# ------------------------------------------------------------------- chapters --
CHAPTERS = [
    ("I", "THE WORD", "What a Kauthik is, and what the word carries"),
    ("II", "THE HISTORY", "A thousand years of coming down the hill"),
    ("III", "THE LAND", "Where the fairs stand, and when they fall"),
    ("IV", "THE SOUND", "Drum, horn and the circle of dancers"),
    ("V", "THE HANDS", "Cloth, copper, bamboo and rice paste"),
    ("VI", "THE SPIRIT", "Goddess, oath and ordeal"),
    ("VII", "THE MARKETPLACE", "What the fair is worth"),
    ("VIII", "THE FUTURE", "Empty houses and a full ground"),
]

# ------------------------------------------------------------- anatomy wheel --
ANATOMY = [
    ("temple", "DEITY",
     "Almost every Kauthik is anchored to a shrine. The fair is the goddess's\nopen house."),
    ("cart", "MARKET",
     "Wool, copper, grain, salt, seed. For centuries the only marketplace a\nhigh village ever saw."),
    ("dhol", "MUSIC",
     "It does not begin when the stalls open. It begins when the dhol and\ndamau are struck."),
    ("hands", "MEETING",
     "Before roads, this was where scattered kin met, matches were made and\ndisputes were settled."),
    ("thali", "MEAL",
     "Millet, hemp-seed chutney, black soybean, and sweets that exist\nnowhere else on earth."),
    ("book", "MEMORY",
     "Songs, dances and dialects survive because a fair gives them somewhere\nto be performed."),
]

# ---------------------------------------------------------------- timeline ----
TIMELINE = [
    ("7th–11th c.", "THE SHRINE FAIRS",
     "Under the Katyuri kings, temples rise across the hills. Deity "
     "processions — jaat — gather villages, and a fair grows at each shrine."),
    ("16th–19th c.", "THE TRANS-HIMALAYAN TRADE",
     "Bhotia caravans carry salt, wool and borax between Tibet and the plains. "
     "The border fairs become the pivot of a mountain economy."),
    ("1914", "JAULJIBI IS FORMALISED",
     "The Zamindar of Askot moves the fair at the Kali–Gori confluence to "
     "Kartik Purnima. Traders come from Tibet, Nepal and Kolkata."),
    ("14 Jan 1921", "THE REGISTERS IN THE SARYU",
     "At the Uttarayani Kauthik, hill farmers end coolie-begar — forced "
     "labour — by tearing up the registers and throwing them in the river."),
    ("1962", "THE PASSES CLOSE",
     "After the war with China the Tibet routes shut. The trade fairs lose "
     "their commerce and survive as cultural gatherings."),
    ("1998 → 2000s", "KAUTHIG COMES TO THE CITY",
     "The Akhil Garhwal Sabha starts a Dehradun festival, renamed Kauthig. "
     "Migrants carry the format to Delhi, Lucknow and Mumbai."),
    ("2000 → today", "A STATE, AND A SEAL",
     "Uttarakhand is formed in 2000. In 2023 the state wins 18 GI tags in a "
     "single day — the fair's crafts acquire legal identity."),
]

# ------------------------------------------------------------ wheel of year ---
CALENDAR = [
    ("CHAITRA", "Mar–Apr", "Phooldei",
     "Children lay flowers on every threshold and are given jaggery and rice."),
    ("BAISAKH", "Apr", "Syalde Bikhauti · Thal Mela",
     "Dwarahat drums in the new year; Thal opens the trading season."),
    ("ASADH", "Jun–Jul", "Ganga Dussehra",
     "River fairs on the Bhagirathi and the Alaknanda."),
    ("SHRAVAN", "Jul", "Harela · Harela Mela",
     "The Day of Green. Sowing begins, and Kauthigs are held across the hills."),
    ("SHRAVAN P.", "Aug", "Bagwal, Devidhura",
     "Four clans meet in ritual combat before Barahi Devi."),
    ("BHADRAPAD", "Aug–Sep", "Nanda Devi Mela",
     "The goddess is worshipped from Almora to Nainital; every 12 years, the Raj Jat."),
    ("KARTIK", "Nov", "Jauljibi · Gauchar · Gad Kauthig",
     "The trade fairs, and statehood week in Dehradun."),
    ("MAKAR S.", "14 Jan", "Uttarayani Kauthik",
     "Bageshwar, on the sand where the Saryu meets the Gomti. The biggest of all."),
]

# ------------------------------------------------------------------- music ----
INSTRUMENTS = [
    ("dhol", "DHOL", "Two-headed barrel drum; the voice that announces."),
    ("damau", "DAMAU", "Kettle drum. Never played without the dhol."),
    ("hurka", "HURKA", "Hourglass drum. Keeps the Jhora circle turning."),
    ("ransingha", "RANSINGHA", "Crescent copper horn. Once a war signal."),
    ("bhankora", "BHANKORA", "Long temple trumpet of Garhwal."),
    ("masakbeen", "MASAKBEEN", "The Himalayan bagpipe."),
]

SONG_FORMS = [
    ("JAGAR", "The invocation. Sung to call a deity into the ground — and into a person."),
    ("JHORA", "Sung and danced at once, in a slow closing circle."),
    ("CHANCHARI", "Long-metre song of Danpur and the high Saryu valley."),
    ("BAIR", "Competitive verse. Two singers, improvising against each other."),
    ("NYOLI", "The song of separation, named for a bird that calls alone."),
    ("BAJUBAND", "A courting dialogue, sung in alternating lines."),
]

DANCES = [
    ("sword", "CHHOLIYA", "Kumaon · also Baitadi & Darchula, Nepal",
     "A sword-and-shield dance in front of a wedding procession. Its purpose "
     "is protective: to clear the path of whatever might envy human happiness. "
     "Ten dancers, two swords, and the dhol-damau setting the duel."),
    ("jhora", "JHORA", "Kumaon · spring and fair season",
     "Men and women link arms and move in a slow, tightening circle to the "
     "hurka. It is danced across community lines — historically one of the few "
     "occasions where that was simply assumed."),
    ("dancer", "JHUMEILA & THADYA", "Garhwal · courtyard and threshing floor",
     "Jhumeila is danced in a ring, Thadya standing; both are sung by the "
     "dancers themselves. The lyrics are the point — they are how a valley "
     "remembers its own gossip, grief and jokes."),
    ("hands", "CHANCHARI & BARADA NATI", "Danpur · Jaunsar-Bhabar",
     "Chanchari moves in a wide double circle on long metre. Barada Nati, from "
     "the Jaunsar-Bhabar country above Chakrata, is danced at religious and "
     "social occasions in full traditional dress."),
]

# ------------------------------------------------------------------ attire ----
ATTIRE = [
    ("pichhora", "RANGWALI PICHHORA",
     "The yellow-and-red odhni of Kumaoni women, hand-painted with a rosette "
     "of dots and a border of motifs. Traditionally painted at home while "
     "shagun-aakhar — auspicious verses — were sung over it. Worn by brides "
     "and by married women at every ceremony since."),
    ("jewel", "NATH · GULOBAND · HANSULI",
     "Hill jewellery is worked in silver and gold and is regionally legible: "
     "the great hoop nath, the guloband collar, the hansuli torque. A woman at "
     "a Kauthik is wearing her family's savings and its history at once."),
    ("loom", "GHAGRA · ANGRA · WOOLLENS",
     "Ghagra and angra with an orni over the head; for men kurta, churidar and "
     "a topi. Above the treeline the whole wardrobe turns to wool — thulma, "
     "dan and pankhi, woven on backstrap looms."),
]

# ------------------------------------------------------------------ crafts ----
CRAFTS = [
    ("aipan", "AIPAN", "Kumaon · Almora belt",
     "Ritual art in white rice paste over red ochre, drawn by women at "
     "thresholds, courtyards and shrines. Every occasion has its own diagram."),
    ("copper", "TAMTA COPPERWARE", "Almora",
     "Beaten copper vessels and temple instruments, made by Tamta artisan "
     "families. The craft names the community that keeps it."),
    ("ringal", "RINGAL BASKETRY", "Higher Garhwal & Kumaon",
     "Himalayan dwarf bamboo split and woven into baskets, mats, rain-shields "
     "and containers — one of the oldest household technologies in the hills."),
    ("chisel", "WOODCARVING", "Village architecture",
     "The carved kholi — the doorframe of a hill house — is the region's "
     "signature sculpture, and increasingly its most endangered."),
    ("loom", "WOOLLEN WEAVING", "Bhotia valleys",
     "Carpets, dan and thulma woven from high-pasture wool by communities who "
     "once ran the Tibet trade."),
    ("gi_seal", "AND NOW, PROTECTED",
     "30+ GI products",
     "In December 2023 Uttarakhand won 18 Geographical Indication tags in a "
     "single day — Aipan, ringal, tamta copper and Bhotia weaves among them."),
]

# ----------------------------------------------------------------- cuisine ----
SAVOURY = [
    ("BHANG KI CHUTNEY",
     "Roasted hemp seed ground with cumin, salt and lemon. The taste people "
     "who left the hills describe first."),
    ("BHATT KI CHURDKANI",
     "Black soybean, slow-cooked. Iron, protein and winter, in one bowl."),
    ("GAHAT / KAFULI",
     "Horse-gram soup; and Kafuli, a thick green of spinach and fenugreek "
     "bound with rice flour."),
    ("MANDUA & JHANGORA",
     "Finger millet and barnyard millet — the grains that actually grew here, "
     "now sold as superfoods."),
]

SWEETS = [
    ("BAL MITHAI",
     "Roasted khoya darkened almost to chocolate, rolled in white sugar "
     "pearls. Almora's most famous export."),
    ("SINGORI",
     "A cone of khoya and coconut wrapped in a malu leaf, which perfumes it."),
    ("ARSA",
     "Rice flour and jaggery, deep-fried. The sweet of Garhwali weddings."),
    ("GHUGHUTE",
     "Dough shaped into birds, pomegranates and drums, threaded into a "
     "necklace and worn by children at Uttarayani."),
]

# ------------------------------------------------------------------ spirit ----
RAJ_JAT = [
    ("12", "YEARS", "between one Raj Jat and the next"),
    ("280", "KILOMETRES", "from Nauti village to Homkund"),
    ("3", "WEEKS", "on foot, at altitude, with the goddess"),
    ("4", "HORNS", "on the ram that walks at the head of the procession"),
]

# ---------------------------------------------------------------- economy -----
TRADE_THEN = ["Raw wool & woven carpets", "Deer musk & shilajit",
              "Himalayan herbs & medicine", "Borax, salt & grain",
              "Honey, ghee & asafoetida"]
TRADE_NOW = ["Munsyari rajma & red rice", "Berinag tea & buransh squash",
             "Bal mithai, mandua, jhangora", "Aipan, ringal & tamta ware",
             "Homestays, guides & festivals"]

# --------------------------------------------------------------- challenges ---
CHALLENGES = [
    ("empty_house", "1,200+ GHOST VILLAGES",
     "Outward migration has emptied over a thousand settlements. A fair needs "
     "a village to walk down from."),
    ("language", "TWO MOTHER TONGUES AT RISK",
     "Garhwali and Kumaoni are losing child speakers. The songs are in those "
     "languages; so is the meaning of the songs."),
    ("thermometer", "AN UNRELIABLE MOUNTAIN",
     "The 2026 Nanda Devi Raj Jat was postponed to 2027 because the high "
     "Himalaya could no longer be relied on for a three-week walk."),
    ("clock", "THE LAST GENERATION WHO KNOWS",
     "Jagar singers, dhol-damau players and Aipan artists are ageing, and few "
     "can live on the work."),
    ("decline", "STAGE, NOT GROUND",
     "Fairs increasingly move to a stage with sponsors and film songs. The "
     "crowd grows; the participation shrinks."),
    ("cart", "SOUVENIR ECONOMICS",
     "Machine-made imitations undercut real craft at the fair that made the "
     "craft famous."),
]

FUTURE = [
    ("gi_seal", "GEOGRAPHICAL INDICATION AS INCOME",
     "30+ protected products, and the state's first GI gallery opened at "
     "Haldwani — provenance turned into price."),
    ("homestay", "THE FAIR AS AN ITINERARY",
     "A published Kauthik calendar makes the off-season sellable: homestays, "
     "guides and food trails around dates that already exist."),
    ("book", "PAY THE CARRIERS",
     "State support for folk artists — including assistance for traditional "
     "instruments and costumes — works only if it reaches the person who "
     "actually knows the song."),
    ("archive", "RECORD EVERYTHING, NOW",
     "High-quality audio and video archives of jagar, chanchari and bair, made "
     "while the last full practitioners are still performing."),
    ("youth", "GIVE IT BACK TO THE YOUNG",
     "School Chholiya troupes, Aipan in the syllabus, and dialect content that "
     "a teenager would actually choose to watch."),
    ("signal", "THE DIASPORA IS AN ASSET",
     "Kauthigs in Delhi, Lucknow and Mumbai already fund and staff the culture. "
     "Treat them as a network, not nostalgia."),
]

FACTS = [
    ("river", "A FAIR ENDED FORCED LABOUR",
     "The registers of coolie-begar were destroyed at a Kauthik, not in a "
     "courtroom — Bageshwar, 14 January 1921."),
    ("trail", "ONE FAIR STANDS IN TWO COUNTRIES",
     "Jauljibi sits where the Kali meets the Gori, and its bazaar spills "
     "across a suspension bridge into Nepal."),
    ("sword", "A DANCE WITH A JOB",
     "Chholiya is not decorative. It is danced in front of a wedding party to "
     "keep harm away from it."),
    ("trident", "AN ORDEAL, THEN A REFORM",
     "At Bagwal, clans once pelted each other with stones until blood was "
     "given. Fruit and flowers now stand in for the stones."),
    ("mountain", "A PILGRIMAGE ONCE IN TWELVE YEARS",
     "The Nanda Devi Raj Jat walks a bride to her husband's house across 280 km "
     "of high Himalaya, led by a four-horned ram."),
    ("sweet", "A SWEET YOU WEAR",
     "At Uttarayani, children wear ghughute — dough birds and drums — strung "
     "into a garland, and feed the first one to a crow."),
]

# ----------------------------------------------------------------- closing ----
CLOSING = "Culture survives when traditions are\ncelebrated, shared, and passed on."

# ----------------------------------------------------------------- sources ----
SOURCES = [
    "Uttarayani Fair; Bageshwar; Coolie-Begar movement; Nanda Devi Raj Jat; "
    "Chholiya; Harela; Jauljibi; Uttarakhandi cuisine — Wikipedia.",
    "“Kauthig — meaning ‘fair’ in Garhwali”; Gad Kauthig, Jauljibi Mela, "
    "Uttarayani Mela and Bagwal reporting — The Times of India, Dehradun & "
    "Lucknow editions, 2014–2026.",
    "Fairs & Festivals of Uttarakhand; Jauljibi and Thal Fairs; Bagwal — "
    "Devidhura; Uttarayani Fair, Bageshwar; Nanda Devi Raj Jat Yatra — "
    "eUttaranchal.",
    "Flavours of the Land; Uttarakhand Tourism Policy 2023; yearly tourism "
    "statistics — Uttarakhand Tourism Development Board, uttarakhandtourism.gov.in.",
    "Aipan: Ritualistic Folk Art of Kumaon — Google Arts & Culture / Project FUEL.",
    "Uttarakhand Economic Survey 2025–26 coverage — ET Government; Economy of "
    "Uttarakhand — Wikipedia.",
    "18 GI tags in a single day (Dec 2023) — Drishti IAS state current affairs; "
    "first GI products gallery, Haldwani — Asianet Newsable.",
    "Ghost villages and out-migration — NPR, The Indian Express, The Times of "
    "India, and the UN India country office.",
    "Zonal Cultural Centres and folk-art support schemes — Ministry of Culture "
    "replies, Lok Sabha & Rajya Sabha; Uttarakhand Department of Culture.",
]

CREDIT = (
    "All artwork in this deck — skies, ranges, mist, particles, silhouettes, "
    "Aipan and mandala motifs, icons and maps — was generated procedurally for "
    "this presentation. Maps are drawn from public Census-2011 district "
    "boundary data. No third-party photography or footage is included."
)

# ======================================================================= notes ==
NOTES: dict[str, str] = {

"cover": """
OPENING — hold the title for a beat before speaking. Let the sky move.

Say: "Kauthik. In Garhwali, it just means 'a fair'. But in Uttarakhand, a fair
is not an event you attend. It is the day a scattered mountain population
becomes a single crowd."

Set the frame: this is not a talk about a festival. It is a talk about how a
culture without cities kept itself alive — and what happens to it now that the
villages are emptying.

Runtime target for the whole deck: 18–22 minutes.
""",

"coldopen": """
COLD OPEN — the most famous folk song in Kumaoni. Almost everyone from the
hills knows the first line; it was carried into national memory by Mohan
Upreti's arrangement.

"Bedu pako baro masa" — the wild fig ripens all twelve months; the kafal, the
Himalayan bayberry, only in Chaitra.

Land the point: it is a song about things that come once a year. Say it plainly
— "So is a Kauthik. And that scarcity is exactly why it matters."

If the Devanagari does not render on the venue machine, just read the
transliteration; the meaning is on screen.
""",

"devbhumi": """
UTTARAKHAND IN THIRTY SECONDS. Do not read the numbers aloud one by one — point
at the map and give only what the audience needs to follow the rest of the talk:

· Two divisions with distinct languages and repertoires: GARHWAL in the west,
  KUMAON in the east. Almost every difference later in this deck traces back to
  this line.
· Formed 9 November 2000 — one of the youngest states in India, with one of the
  oldest continuous fair traditions.
· 13 districts across roughly 53,500 square kilometres, most of it mountain.
· Called Devbhumi, the land of the gods: the four Char Dham shrines, and two
  UNESCO World Heritage sites in Nanda Devi and the Valley of Flowers.

Transition: "In this terrain, the fair was infrastructure."
""",

"ch1": """
CHAPTER I — THE WORD. Pause on the divider. These dividers exist to let the
audience breathe and to reset attention; use them.
""",

"word": """
THE WORD ITSELF.

· In Garhwali, kauthig means fair. In Kumaoni you will hear kauthig, and also
  thol. In practice everyone also just says mela.
· Scholars generally read the word back to Sanskrit KAUTUKA — curiosity,
  festivity, spectacle, the state of being delighted. Flag it as a reading, not
  a certainty; that honesty is worth more than a clean story.
· The important move is the one on screen: the Dehradun festival was launched
  in 1998 as the "Uttarakhand Mahotsav" and later RENAMED Kauthig, specifically
  so the name would be in the regional language. That rename is a small act of
  cultural politics and worth naming as such.

Line to use: "They did not invent a festival. They gave a festival back its
own word."
""",

"anatomy": """
ANATOMY OF A KAUTHIK — the six functions. Let the wheel build; speak to each
node as it lands.

The argument: a Kauthik is not one thing wearing five costumes. It is a single
institution doing six jobs simultaneously — religious, commercial, musical,
social, culinary and archival. Remove the fair and you do not lose a party; you
lose the delivery mechanism for all six.

If short on time, keep MARKET, MEETING and MEMORY. They carry the thesis.
""",

"ch2": "CHAPTER II — THE HISTORY.",

"timeline": """
TIMELINE — the spine of the talk. Let it draw itself; do not race it.

Beats to hit:
· KATYURI ERA — fairs begin as religious gatherings at temples, not as markets.
· TRADE CENTURIES — Bhotia caravans across the passes make the border fairs the
  clearing house of the whole mountain economy.
· 1914 — Jauljibi is formalised by the Zamindar of Askot and shifted to Kartik
  Purnima.
· 1921 — the political moment. Next slide.
· 1962 — the war with China closes the passes. This is the hinge: the trade
  fairs lose their economic reason and survive by becoming cultural events.
  Everything modern about Kauthik starts here.
· 1998 onward — the urban and diaspora Kauthigs.
· 2000 / 2023 — statehood, then legal protection for the crafts.
""",

"1921": """
THE HERO SLIDE. Slow down. This is the emotional and political centre.

Coolie-begar was a system of forced, unpaid labour: hill villagers were
compelled to carry loads and provide supplies for touring officials, recorded
in registers kept by village headmen and patwaris.

On 14 January 1921 — Makar Sankranti, the day of the Uttarayani fair —
thousands gathered at Bageshwar on the sand where the Saryu meets the Gomti.
Led by Badri Datt Pandey and Hargovind Pant of the Kumaun Parishad, the
headmen tore the registers and threw them into the river. The practice
collapsed.

Pandey was afterwards called KUMAON KESARI, the Lion of Kumaon; Pant,
JANNAYAK, leader of the people.

The line that matters: they were able to do it BECAUSE it was a fair. Nothing
else in that landscape could assemble thousands of people from dozens of
valleys on a known date. The fair was the only available public square.

Every January, political parties still walk to that sandbank and repeat the
gesture.
""",

"ch3": "CHAPTER III — THE LAND.",

"map": """
THE MAP. Let Garhwal and then Kumaon fill in, then the pins.

Four to name, and only four:
· BAGESHWAR — Uttarayani Kauthik at the Saryu–Gomti confluence, by the Bagnath
  temple. Historically the largest fair in Kumaon; around fifteen thousand
  people were attending in the early twentieth century.
· JAULJIBI — Pithoragarh district, at the meeting of the Kali and Gori rivers,
  on the Indo-Nepal border and on the Kailash Mansarovar route. A trade fair
  more than a century old.
· DEVIDHURA — Champawat, the Barahi Devi temple. Bagwal.
· NAUTI — Chamoli, where the Nanda Devi Raj Jat begins.

Then add: Thal, Dwarahat for Syalde Bikhauti, Almora, Gauchar, Bhimtal — and
Dehradun, where the modern Gad Kauthig is held.
""",

"calendar": """
THE WHEEL OF THE YEAR. The point of this slide is rhythm, not detail.

Say: "There is no single Kauthik. There is a calendar." The fairs are pinned to
the agricultural and astronomical year — sowing, harvest, the solstice, the
monsoon — which is why they cannot simply be rescheduled for tourism
convenience without breaking their meaning.

Note the two poles of the year: HARELA in July, which opens the sowing cycle,
and UTTARAYANI on 14 January, which marks the sun turning north. The biggest
fair of all sits at the coldest point of the year, which tells you it was never
primarily about the weather.
""",

"ch4": "CHAPTER IV — THE SOUND.",

"music": """
MUSIC. If you can, play four seconds of dhol-damau before you speak. If not,
say the line and let the instruments build.

· The dhol and damau are a PAIR — never one without the other. Together they
  are the announcing voice of any ritual or fair in the region.
· The hurka is the drum of the Jhora circle.
· Ransingha and bhankora are the horns; masakbeen is the local bagpipe.

On the song forms: JAGAR is the one to dwell on. It is not entertainment — it
is invocation, sung to bring a deity into the ground and into a designated
human medium. It is the strongest evidence that this music is functional, not
ornamental.

BAIR is competitive improvised verse; NYOLI is the song of separation, named
for a bird that calls alone. Migration has given that one a second life.
""",

"dance": """
DANCE. Four traditions, one argument: these are participatory forms, not
performances.

· CHHOLIYA — Kumaon's sword-and-shield dance, also found across the border in
  Baitadi and Darchula in Nepal. It accompanies wedding processions and its
  stated purpose is protective.
· JHORA — arms linked, a slow circle to the hurka, historically danced across
  caste lines. Worth saying plainly: the fair was one of the few spaces where
  that was simply assumed.
· JHUMEILA and THADYA — Garhwal; the dancers are also the singers.
· CHANCHARI, and BARADA NATI from Jaunsar-Bhabar above Chakrata.

The distinction to leave with the audience: a stage has an audience; a circle
does not. What is at risk is the circle.
""",

"ch5": "CHAPTER V — THE HANDS.",

"attire": """
ATTIRE. Lead with the Pichhora — it is the single most recognisable object in
Kumaoni material culture.

The Rangwali Pichhora is a yellow ground with a red rosette of dots and a
patterned border, worn by brides and by married women at ceremonies. The detail
that lands: it was painted at home, by women, while auspicious verses —
shagun-aakhar — were sung over the cloth. The object and the song were made in
the same act.

Jewellery is regionally legible — the nath, the guloband, the hansuli — and
functions as stored family wealth as much as ornament.

Above the treeline the wardrobe becomes wool: thulma, dan, pankhi, woven on
backstrap looms by the same Bhotia communities who ran the Tibet trade.
""",

"crafts": """
CRAFTS — the bazaar as a museum that sells.

· AIPAN — white rice paste on red ochre, drawn by women at thresholds and
  shrines, with a specific diagram for each occasion. It is ritual, not
  decoration.
· TAMTA COPPERWARE from Almora — the craft is named for the community that
  keeps it.
· RINGAL — Himalayan dwarf bamboo, split and woven.
· WOODCARVING — the kholi, the carved doorframe, is the region's signature
  sculpture and is being lost with the houses.
· BHOTIA WEAVING — carpets, dan and thulma.

Then the policy beat: in December 2023 Uttarakhand became the first state to
receive 18 GI certificates in one day, and now holds 30-plus. The state's first
GI gallery opened at Haldwani. This is the mechanism by which a fair craft
becomes a defensible livelihood.
""",

"food": """
FOOD. Keep it fast and sensory. The food slide is where a general audience
leans in.

Savoury: bhang ki chutney — roasted hemp seed with cumin, salt and lemon; bhatt
ki churdkani from black soybean; gahat horse-gram; kafuli, a thick green bound
with rice flour; and the millets, mandua and jhangora, that actually grow at
altitude.

Sweet: bal mithai from Almora — roasted khoya rolled in white sugar pearls;
singori, wrapped in a malu leaf that flavours it; arsa, of Garhwali weddings.

Then the specific one: GHUGHUTE, made only for Uttarayani — dough shaped into
birds, drums and pomegranates, strung as a necklace for children, who feed the
first one to a crow. A food that is also a costume and also a rite.

Worth naming: this is millet-and-pulse mountain cooking that the rest of the
world has just rediscovered as nutrition science.
""",

"ch6": "CHAPTER VI — THE SPIRIT.",

"spirit": """
THE SPIRIT. Two set-pieces.

NANDA DEVI RAJ JAT — the "Himalayan Mahakumbh". Once every twelve years, from
Nauti village in Chamoli to Homkund near Roopkund: roughly 280 kilometres on
foot over about three weeks. Nanda Devi is understood as a daughter of the
region, and the procession is her journey to her husband's house — so the
emotional register is not awe, it is farewell. A four-horned ram walks at the
head and is released at Homkund carrying offerings.

BAGWAL at Devidhura — four clans, Walik, Chamyal, Lamgaria and Gaherwal, meet
in ritual combat before Barahi Devi with wooden shields called farra. Blood was
traditionally offered. Since 2013 fruit and flowers have substituted for
stones — a tradition amending itself from inside, which is the more interesting
story than the spectacle.

And JAGAR, from the music slide: possession as a scheduled, communal,
sanctioned event.
""",

"ch7": "CHAPTER VII — THE MARKETPLACE.",

"economy": """
ECONOMY. Let the counters run, then talk over the comparison.

The historical function: at Jauljibi, Indian traders brought wool, carpets,
deer musk and herbal medicine; traders from Nepal brought honey, ghee,
asafoetida and shilajit. Merchants came from Tibet, Nepal and as far as
Kolkata. This was the annual liquidity event for an entire mountain economy.

Then 1962 closed the passes.

What replaced it is the column on the right: named, protected, provenance-led
produce and craft — Munsyari rajma, red rice, Berinag tea, buransh, bal mithai,
mandua, plus Aipan, ringal and tamta ware. Same fairground, different economy.

Frame: "The fair stopped being where goods crossed a border, and became where
goods acquire an identity."
""",

"tourism": """
TOURISM. Use the chart, not the numbers.

The Char Dham pilgrimage is the state's tourism engine: roughly 46.7 lakh
pilgrims in 2024, and about 51.1 lakh in 2025. Uttarakhand's economy grew at
around 7.2 per cent in 2024-25, with gross state domestic product in the region
of 45 billion US dollars.

But make the honest argument: that traffic is concentrated in a few months, on
a few routes, and it strains fragile places. The fairs are the natural
counter-weight — they are DISTRIBUTED across the calendar and across the map,
and they already exist. A published Kauthik calendar is an off-season product
that needs no new construction.

Caveat to state out loud if asked: headline "tourism share of GSDP" figures for
Uttarakhand vary widely between sources because they mix direct and indirect
activity. Do not defend a single percentage.
""",

"ch8": "CHAPTER VIII — THE FUTURE.",

"modern": """
MODERN TRANSFORMATION. Resist the decline narrative here; this slide is about
adaptation.

· The urban Kauthig: Dehradun's Gad Kauthig since around statehood, timed to
  9 November. Uttarayani Kauthig in Lucknow, run by the Parvatiya
  Mahaparishad — a fifteen-day event in its 2026 edition. Kauthig in Mumbai and
  Delhi run by migrant associations, explicitly as community service as much as
  festival.
· Traditional forms are finding audiences on short-video platforms; dialect
  music has a real online market for the first time.
· Self-help groups and women's collectives now hold a large share of the craft
  and food stalls, which changes who the fair pays.
· And Bagwal replacing stones with fruit shows a tradition editing itself
  rather than being edited.

Line: "The fair followed its people down the mountain."
""",

"challenges": """
CHALLENGES. Deliver this plainly, without melodrama.

The central problem is not indifference; it is DEPOPULATION. Over a thousand
villages in Uttarakhand are effectively abandoned, and the fair is downstream of
the village. Language loss follows: the songs are in Garhwali and Kumaoni, and
so is what the songs mean.

Climate is now a scheduling problem, not an abstraction: the Nanda Devi Raj Jat
due in 2026 was postponed to 2027 because a three-week high-altitude walk could
no longer be planned reliably.

Then the livelihood problem — jagar singers, dhol-damau players and Aipan
artists are ageing and few can live on the work — and the format problem: the
move from ground to stage, from participants to spectators.

Do not end the section here. Go straight into the next slide.
""",

"future": """
THE ROAD AHEAD. Six concrete moves, not sentiments. Pick three if time is short
— GI as income, the fair as an itinerary, and pay the carriers.

Existing scaffolding to credit: the Zonal Cultural Centres, Sangeet Natak
Akademi folk-arts schemes, the Uttarakhand Department of Culture's assistance
for traditional instruments and costumes, central grants for the preservation of
Himalayan culture, the Uttarakhand Bhasha Sansthan for the languages, and the
Tourism Policy 2023.

The test to leave in the room: money and policy already exist. The question is
whether they reach the person who still knows the song.
""",

"facts": """
SIX THINGS TO REMEMBER. This slide is designed to be photographed. Pause long
enough for phones.

Use it as a recap of the whole argument: a fair ended forced labour; a fair
stands in two countries; a dance has a job; an ordeal reformed itself; a
pilgrimage happens once in twelve years; and a sweet is also a garland.
""",

"closing": """
CLOSING. Let the line sit. Do not read it twice.

"Culture survives when traditions are celebrated, shared, and passed on."

Then the last thought, in your own words: a Kauthik is not preserved by being
recorded, photographed or funded. It is preserved by being ATTENDED. The
strongest thing anyone in this room can do is turn up — buy from the artisan,
learn the four steps of the Jhora, ask what the song means.

Final beat: "The mountains do not need us. The fair does."
""",

"thanks": """
THANK YOU. Q&A.

Likely questions and short answers:

· "Is Kauthik one specific festival?" — No. It is the Garhwali word for fair.
  It names a category, and also, since 1998, specific modern festivals in
  Dehradun and in diaspora cities.
· "Why is Bagwal still allowed?" — It has been substantially reformed; fruit
  and flowers replace stones, and it is administered with medical support.
· "Best time to attend?" — Uttarayani at Bageshwar around 14 January for scale;
  Jauljibi in November for the trade-fair character; Devidhura on Raksha
  Bandhan for Bagwal; Nauti in 2027 for the Raj Jat.
· "Sources?" — Next slide, and every figure in the deck is attributable.
""",

"sources": """
SOURCES. Leave this up during Q&A.

Two disclosures worth making unprompted:
1. All artwork here was generated for this deck — the skies, ranges, mist,
   silhouettes, Aipan and mandala motifs, icons and maps. Nothing is
   third-party photography, so the deck can be shared and reused freely.
2. Maps use public Census-2011 district boundaries; district lines reflect that
   vintage.
""",
}
