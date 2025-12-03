/*
key, the unique ID of the person
n, the person's name
s, the person's sex
m, the person's mother's key
f, the person's father's key
ux, the person's wife
vir, the person's husband
a, an Array of the attributes or markers that the person has
*/

const relationdata = [
    {
        "key": 1,
        "n": "Aayodadhaumya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 2,
        "n": "Abhaya",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 3,
        "n": "Abhimanyu",
        "s": "M",
        "m": 410,
        "f": 715,
        "ux": 454
    },
    {
        "key": 6,
        "n": "Aditi",
        "s": "F",
        "m": -99,
        "f": 77,
        "vir": -99
    },
    {
        "key": 7,
        "n": "Adityaketu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 8,
        "n": "Adrika",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 449
    },
    {
        "key": 10,
        "n": "Agniveshya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 12,
        "n": "Ahampati",
        "s": "M",
        "m": 460,
        "f": 356,
        "ux": 62
    },
    {
        "key": 18,
        "n": "Alolupa",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 19,
        "n": "Amitouja",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 20,
        "n": "Anadhrishya",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 22,
        "n": "Anayu",
        "s": "M",
        "m": -99,
        "f": 77,
        "ux": -99
    },
    {
        "key": 23,
        "n": "Angirasa",
        "s": "M",
        "m": -99,
        "f": 77,
        "ux": -99
    },
    {
        "key": 25,
        "n": "Anshumana",
        "s": "M",
        "m": -99,
        "f": 35,
        "ux": -99
    },
    {
        "key": 26,
        "n": "Anudara",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 27,
        "n": "Anuvinda",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 28,
        "n": "Aparajita",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 33,
        "n": "Aruni",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 34,
        "n": "Arushi",
        "s": "F",
        "m": -99,
        "f": 243,
        "vir": 399
    },
    {
        "key": 37,
        "n": "Ashoka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 39,
        "n": "Ashvasena",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 40,
        "n": "Asita",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 42,
        "n": "Atreya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 43,
        "n": "Ayobahu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 45,
        "n": "Ayutanayi",
        "s": "M",
        "m": 430,
        "f": 236,
        "ux": 64
    },
    {
        "key": 48,
        "n": "Bahvashi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 50,
        "n": "Baladeva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 52,
        "n": "Balaki",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 53,
        "n": "Balavardhana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 54,
        "n": "Bali",
        "s": "M",
        "m": -99,
        "f": 489,
        "ux": -99
    },
    {
        "key": 55,
        "n": "Barbarika",
        "s": "M",
        "m": -99,
        "f": 158,
        "ux": -99
    },
    {
        "key": 56,
        "n": "Bhadra",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 57,
        "n": "Bhadramana",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 58,
        "n": "Bhagadatta",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 59,
        "n": "Bhagiratha",
        "s": "M",
        "m": -99,
        "f": 117,
        "ux": -99
    },
    {
        "key": 60,
        "n": "Bhaluki",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 61,
        "n": "Bhangasvari",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 63,
        "n": "Bharata",
        "s": "M",
        "m": 373,
        "f": 150,
        "ux": 421
    },
    {
        "key": 64,
        "n": "Bhasa",
        "s": "F",
        "m": -99,
        "f": 313,
        "vir": 45
    },
    {
        "key": 66,
        "n": "Bhimabala",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 67,
        "n": "Bhimakarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 68,
        "n": "Bhimaratha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 70,
        "n": "Bhimavega",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 71,
        "n": "BhimaVidarbha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 72,
        "n": "Bhishma",
        "s": "M",
        "m": 154,
        "f": 380,
        "ux": -99
    },
    {
        "key": 75,
        "n": "Bibhatsu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 76,
        "n": "Bodhapingala",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 77,
        "n": "Brahma",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 78,
        "n": "Brihadashva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 79,
        "n": "Brihadratha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 80,
        "n": "Brihanta",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 81,
        "n": "Brihaspati",
        "s": "M",
        "m": -99,
        "f": 23,
        "ux": -99
    },
    {
        "key": 82,
        "n": "Chakra",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 83,
        "n": "Chandabhargava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 84,
        "n": "Charuchitra",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 85,
        "n": "Chitra",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 86,
        "n": "Chitrabana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 87,
        "n": "Chitraksha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 88,
        "n": "Chitrakundala",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 89,
        "n": "Chitralekha",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 90,
        "n": "Chitranga",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 91,
        "n": "Chitravarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 92,
        "n": "Chitravarmana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 94,
        "n": "Damayanti",
        "s": "F",
        "m": -99,
        "f": 71,
        "vir": 265
    },
    {
        "key": 95,
        "n": "Dambhodbhava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 96,
        "n": "Danda",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 97,
        "n": "Dandadhara",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 98,
        "n": "Dantavakra",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 99,
        "n": "Danu",
        "s": "F",
        "m": -99,
        "f": 77,
        "vir": -99
    },
    {
        "key": 100,
        "n": "Dashratha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 101,
        "n": "Devadhipa",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 102,
        "n": "Devala",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 105,
        "n": "Devasharma",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 108,
        "n": "Devyani",
        "s": "F",
        "m": -99,
        "f": 399,
        "vir": 505
    },
    {
        "key": 109,
        "n": "Dhanurgraha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 110,
        "n": "Dhara",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 112,
        "n": "Dhrishtadyumna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 113,
        "n": "Dhrishtaketu",
        "s": "M",
        "m": -99,
        "f": 392,
        "ux": -99
    },
    {
        "key": 116,
        "n": "Dhurva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 117,
        "n": "Dilipa",
        "s": "M",
        "m": -99,
        "f": 25,
        "ux": -99
    },
    {
        "key": 118,
        "n": "Dirghabahu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 119,
        "n": "Dirghalochana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 120,
        "n": "Dirghaprajna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 121,
        "n": "Diti",
        "s": "F",
        "m": -99,
        "f": 77,
        "vir": -99
    },
    {
        "key": 124,
        "n": "Dridhahasta",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 125,
        "n": "Dridhakshatra",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 126,
        "n": "Dridharatha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 127,
        "n": "Dridhasandha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 128,
        "n": "Dridhavarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 129,
        "n": "Dridhayudha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 131,
        "n": "Druma",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 132,
        "n": "Drumasena",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 134,
        "n": "Duhsaha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 136,
        "n": "Duhshasana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 137,
        "n": "Duhshashana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 138,
        "n": "Dundu",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 139,
        "n": "Duravara",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 140,
        "n": "Durdharsha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 141,
        "n": "Durmada",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 142,
        "n": "Durmarshana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 143,
        "n": "Durmukha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 144,
        "n": "Durvimochana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 145,
        "n": "Duryodhana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 146,
        "n": "Dushkarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 147,
        "n": "Dushparajaya",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 148,
        "n": "Dushpradharshana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 149,
        "n": "Dushpragaha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 152,
        "n": "Gadhi",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 153,
        "n": "Gandhari",
        "s": "F",
        "m": -99,
        "f": 409,
        "vir": 114
    },
    {
        "key": 156,
        "n": "Gaurmukha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 158,
        "n": "Ghatotkacha",
        "s": "M",
        "m": 169,
        "f": 65,
        "ux": -99
    },
    {
        "key": 159,
        "n": "Gopali",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 160,
        "n": "Gouri",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 161,
        "n": "Goutama",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 162,
        "n": "Halisaka",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 163,
        "n": "Hardikya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 164,
        "n": "Harimedha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 166,
        "n": "Harita",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 167,
        "n": "Harsha",
        "s": "M",
        "m": -99,
        "f": 111,
        "ux": 266
    },
    {
        "key": 169,
        "n": "Hidimba",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 65
    },
    {
        "key": 170,
        "n": "Hiranyakashipu",
        "s": "M",
        "m": 121,
        "f": -99,
        "ux": -99
    },
    {
        "key": 171,
        "n": "Hiranyavaha",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 172,
        "n": "Hotravahana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 173,
        "n": "Hritachi",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 306
    },
    {
        "key": 177,
        "n": "Indradyumna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 179,
        "n": "Jalasandha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 180,
        "n": "Jamadagni",
        "s": "M",
        "m": -99,
        "f": 331,
        "ux": 328
    },
    {
        "key": 181,
        "n": "Jambavati",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 183,
        "n": "Janaki",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 184,
        "n": "Janamejaya",
        "s": "M",
        "m": -99,
        "f": 509,
        "ux": 459
    },
    {
        "key": 186,
        "n": "Jarasandha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 187,
        "n": "JaratkaruM",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": 842
    },
    {
        "key": 188,
        "n": "Jayadratha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 190,
        "n": "Jvala",
        "s": "F",
        "m": -99,
        "f": 432,
        "vir": 332
    },
    {
        "key": 192,
        "n": "Kahoda",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 193,
        "n": "Kakshaka",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 194,
        "n": "Kala",
        "s": "M",
        "m": -99,
        "f": 77,
        "ux": -99
    },
    {
        "key": 195,
        "n": "Kalabha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 196,
        "n": "Kaladantaka",
        "s": "F",
        "m": -99,
        "f": 466,
        "vir": -99
    },
    {
        "key": 197,
        "n": "Kalakriti",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 199,
        "n": "Kalindi",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 201,
        "n": "Kanakadhvaja",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 202,
        "n": "Kanakayu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 204,
        "n": "Karna2",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 205,
        "n": "Karnashrava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 206,
        "n": "Kartaviryaarjuna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 208,
        "n": "Kavachi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 209,
        "n": "Khatavanga",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 210,
        "n": "Konapa",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 211,
        "n": "Konavega",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 212,
        "n": "Kotika",
        "s": "F",
        "m": -99,
        "f": 466,
        "vir": -99
    },
    {
        "key": 213,
        "n": "Koutsarya Jaimini",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 216,
        "n": "Kritacheta",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 218,
        "n": "Krodha",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 220,
        "n": "Kumbhayoni",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 221,
        "n": "Kundabhedi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 222,
        "n": "Kundajathara",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 224,
        "n": "Kundashi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 225,
        "n": "Kundodara",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 228,
        "n": "Kushika",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 229,
        "n": "Kutighata",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 230,
        "n": "Lakshmana",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 231,
        "n": "Lavanashva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 232,
        "n": "Lohitaksha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 233,
        "n": "Lopamudra",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 9
    },
    {
        "key": 234,
        "n": "Madhurasvara",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 235,
        "n": "Mahabahu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 237,
        "n": "Mahodara",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 238,
        "n": "Malla",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 239,
        "n": "Manasa",
        "s": "F",
        "m": -99,
        "f": 466,
        "vir": -99
    },
    {
        "key": 242,
        "n": "Mandhata",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 244,
        "n": "Markandeya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 245,
        "n": "Martanda",
        "s": "M",
        "m": -99,
        "f": 504,
        "ux": -99
    },
    {
        "key": 247,
        "n": "Maya",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 248,
        "n": "Meghavahana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 249,
        "n": "Menaka",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 250,
        "n": "Mishrakeshi",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 251,
        "n": "Mitravinda",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 253,
        "n": "Mondgalya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 257,
        "n": "Muni",
        "s": "M",
        "m": -99,
        "f": 77,
        "ux": -99
    },
    {
        "key": 258,
        "n": "Munja",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 259,
        "n": "Munjakesha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 260,
        "n": "Nabhaga",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 261,
        "n": "Nagadanta",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 262,
        "n": "Nagnajiti",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 265,
        "n": "Nala",
        "s": "M",
        "m": -99,
        "f": 487,
        "ux": 94
    },
    {
        "key": 266,
        "n": "Nanda",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 267,
        "n": "Narada",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 269,
        "n": "Nishangi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 270,
        "n": "NrigaF",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 271,
        "n": "NrigaM",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 272,
        "n": "Ourva",
        "s": "F",
        "m": 34,
        "f": 399,
        "vir": -99
    },
    {
        "key": 273,
        "n": "Oushinara",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 274,
        "n": "Paila",
        "s": "F",
        "m": -99,
        "f": 466,
        "vir": -99
    },
    {
        "key": 275,
        "n": "Panchama",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 277,
        "n": "Panditaka",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 279,
        "n": "Papajita",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 282,
        "n": "Parashurama",
        "s": "M",
        "m": -99,
        "f": 180,
        "ux": -99
    },
    {
        "key": 284,
        "n": "Parikshita",
        "s": "M",
        "m": -99,
        "f": 3,
        "ux": -99
    },
    {
        "key": 286,
        "n": "Parikshit3",
        "s": "M",
        "m": -99,
        "f": 4,
        "ux": -99
    },
    {
        "key": 288,
        "n": "Parvata",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 289,
        "n": "Paschimanupaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 290,
        "n": "Pashi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 293,
        "n": "Paushya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 294,
        "n": "Picchila",
        "s": "F",
        "m": -99,
        "f": 466,
        "vir": -99
    },
    {
        "key": 296,
        "n": "Poundramatsyaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 297,
        "n": "Pourava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 301,
        "n": "Prahlada",
        "s": "M",
        "m": -99,
        "f": 170,
        "ux": -99
    },
    {
        "key": 302,
        "n": "Prahrada",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 303,
        "n": "Prajagara",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 304,
        "n": "Prakalana",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 309,
        "n": "Prativindhya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 313,
        "n": "Prithushrava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 315,
        "n": "Purna",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 317,
        "n": "Purujita",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 318,
        "n": "Purukutsa",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 319,
        "n": "Pururava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": 452
    },
    {
        "key": 320,
        "n": "Pururva",
        "s": "M",
        "m": -99,
        "f": 174,
        "ux": 452
    },
    {
        "key": 321,
        "n": "Purvachitti",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 323,
        "n": "Rahu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 324,
        "n": "Rajarsi Manimana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 326,
        "n": "Rambha",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 327,
        "n": "Rantideva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 330,
        "n": "Richepu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 331,
        "n": "Richika",
        "s": "M",
        "m": -99,
        "f": 272,
        "ux": 825
    },
    {
        "key": 333,
        "n": "Rishika",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 334,
        "n": "Ritava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 335,
        "n": "Ritavasu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 336,
        "n": "Rituparna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 337,
        "n": "Rochamana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 338,
        "n": "Roudrakarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 340,
        "n": "Rukmini",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 342,
        "n": "Ruru",
        "s": "M",
        "m": 173,
        "f": 306,
        "ux": 305
    },
    {
        "key": 343,
        "n": "Sadahsuvaka",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 345,
        "n": "Saha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 346,
        "n": "Saha2",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 347,
        "n": "Saha3",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 349,
        "n": "Sahajanya",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 350,
        "n": "Sahasrapada",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 351,
        "n": "Sama",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 352,
        "n": "Samashrava",
        "s": "M",
        "m": -99,
        "f": 398,
        "ux": -99
    },
    {
        "key": 353,
        "n": "Samasourabha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 355,
        "n": "Samvarana",
        "s": "M",
        "m": -99,
        "f": 15,
        "ux": 435
    },
    {
        "key": 358,
        "n": "Sarvabhouma",
        "s": "M",
        "m": 62,
        "f": 12,
        "ux": 420
    },
    {
        "key": 360,
        "n": "Satvata",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 361,
        "n": "Satyabhama",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 215
    },
    {
        "key": 364,
        "n": "Satyasandha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 366,
        "n": "Saunaka",
        "s": "M",
        "m": -99,
        "f": 763,
        "ux": -99
    },
    {
        "key": 368,
        "n": "Senabindu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 369,
        "n": "Senani",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 370,
        "n": "Senapati",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 372,
        "n": "Shakuni",
        "s": "M",
        "m": -99,
        "f": 409,
        "ux": -99
    },
    {
        "key": 375,
        "n": "Shalya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 377,
        "n": "Shamanthaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 378,
        "n": "Shamatha",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 379,
        "n": "Shamika",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 383,
        "n": "Sharana",
        "s": "M",
        "m": -99,
        "f": 466,
        "ux": -99
    },
    {
        "key": 384,
        "n": "Sharasana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 385,
        "n": "Sharmishtha",
        "s": "F",
        "m": -99,
        "f": 589,
        "vir": 505
    },
    {
        "key": 386,
        "n": "Sharngarava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 387,
        "n": "Shashabindu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 390,
        "n": "Shibi",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 392,
        "n": "Shishupala",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 394,
        "n": "Shounaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 397,
        "n": "Shrutakirti",
        "s": "M",
        "m": 123,
        "f": 715,
        "ux": -99
    },
    {
        "key": 398,
        "n": "Shrutashrava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": 352
    },
    {
        "key": 399,
        "n": "Shukra",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 400,
        "n": "Shunaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 401,
        "n": "Shutarvana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 402,
        "n": "Shvetketu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 403,
        "n": "Simhika",
        "s": "F",
        "m": -99,
        "f": 77,
        "vir": -99
    },
    {
        "key": 406,
        "n": "Somakirti",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 407,
        "n": "Sthunakarna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 408,
        "n": "Subahu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 409,
        "n": "Subala",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 410,
        "n": "Subhadra",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 715
    },
    {
        "key": 411,
        "n": "Suhasta",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 413,
        "n": "Suhotra2",
        "s": "M",
        "m": -99,
        "f": 348,
        "ux": -99
    },
    {
        "key": 414,
        "n": "Suhotra3",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 416,
        "n": "Sulochana",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 418,
        "n": "Sunabha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 419,
        "n": "Sunaka",
        "s": "M",
        "m": 305,
        "f": 342,
        "ux": -99
    },
    {
        "key": 422,
        "n": "Surabhi",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 424,
        "n": "Surya",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 425,
        "n": "Sushena",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 426,
        "n": "Sutasoma",
        "s": "M",
        "m": 123,
        "f": 714,
        "ux": -99
    },
    {
        "key": 427,
        "n": "Suvarcha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 428,
        "n": "Suvarma",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 429,
        "n": "Suvastu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 431,
        "n": "Svayamprabha",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 433,
        "n": "Tamra",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 435,
        "n": "Tapati",
        "s": "F",
        "m": -99,
        "f": 424,
        "vir": 355
    },
    {
        "key": 436,
        "n": "Trasadasyu",
        "s": "M",
        "m": -99,
        "f": 318,
        "ux": -99
    },
    {
        "key": 437,
        "n": "Trita",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 438,
        "n": "Ucchaishrava",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 440,
        "n": "Ugra",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 441,
        "n": "Ugrasena",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 442,
        "n": "Ugrashrava",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 444,
        "n": "Ugrayayi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 445,
        "n": "Ugrayudha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 446,
        "n": "Upachitra",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 447,
        "n": "Upamanyu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 448,
        "n": "Upanandaka",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 450,
        "n": "Urdhvareta",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 451,
        "n": "Urnanabha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 452,
        "n": "Urvashi",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 319
    },
    {
        "key": 453,
        "n": "Ushinara",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 454,
        "n": "Uttara",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": 3
    },
    {
        "key": 455,
        "n": "Vadhryashva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 456,
        "n": "Vaishravana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 457,
        "n": "Vakra",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 458,
        "n": "Valmiki",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 461,
        "n": "Varcha",
        "s": "F",
        "m": -99,
        "f": 405,
        "vir": -99
    },
    {
        "key": 462,
        "n": "Varuna",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": 833
    },
    {
        "key": 463,
        "n": "Varuthini",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 465,
        "n": "Vasudeva",
        "s": "M",
        "m": -99,
        "f": 630,
        "ux": 840
    },
    {
        "key": 467,
        "n": "Vasumana",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 468,
        "n": "Vasumitra",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 469,
        "n": "Vatavega",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 470,
        "n": "Vatsya",
        "s": "F",
        "m": -99,
        "f": -99,
        "vir": -99
    },
    {
        "key": 471,
        "n": "Veda",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 474,
        "n": "Vibhandaka",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 479,
        "n": "Vikarna",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 480,
        "n": "Vikata",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 483,
        "n": "Vinda",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 484,
        "n": "Vira",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 485,
        "n": "Virabahu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 486,
        "n": "Viraja",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 487,
        "n": "Virasena",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 488,
        "n": "Viravi",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 489,
        "n": "Virochana",
        "s": "M",
        "m": -99,
        "f": 301,
        "ux": -99
    },
    {
        "key": 491,
        "n": "Vishalaksha",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 492,
        "n": "Vishnu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 493,
        "n": "Vishva",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 495,
        "n": "Vishvamitra",
        "s": "M",
        "m": -99,
        "f": 152,
        "ux": -99
    },
    {
        "key": 496,
        "n": "Vishvavasu",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 498,
        "n": "Vivimshati",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 499,
        "n": "Vivitsu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 500,
        "n": "Vrishamitra",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 502,
        "n": "Vyasa",
        "s": "M",
        "m": 365,
        "f": 281,
        "ux": -99
    },
    {
        "key": 503,
        "n": "Vyudhoru",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    },
    {
        "key": 504,
        "n": "Yama",
        "s": "M",
        "m": -99,
        "f": 497,
        "ux": -99
    },
    {
        "key": 506,
        "n": "Yayavara",
        "s": "M",
        "m": -99,
        "f": -99,
        "ux": -99
    },
    {
        "key": 508,
        "n": "Yuyutsu",
        "s": "M",
        "m": 153,
        "f": 114,
        "ux": -99
    }
];



// [
//     { key: 0, n: "Aaron", s: "M", m: -10, f: -11, ux: 1, a: ["C", "F", "K"] },
//     { key: 1, n: "Alice", s: "F", m: -12, f: -13, a: ["B", "H", "K"] },
//     { key: 2, n: "Bob", s: "M", m: 1, f: 0, ux: 3, a: ["C", "H", "L"] },
//     { key: 3, n: "Barbara", s: "F", a: ["C"] },
//     { key: 4, n: "Bill", s: "M", m: 1, f: 0, ux: 5, a: ["E", "H"] },
//     { key: 5, n: "Brooke", s: "F", a: ["B", "H", "L"] },
//     { key: 6, n: "Claire", s: "F", m: 1, f: 0, a: ["C"] },
//     { key: 7, n: "Carol", s: "F", m: 1, f: 0, a: ["C", "I"] },
//     { key: 8, n: "Chloe", s: "F", m: 1, f: 0, a: ["E"] },
    
// ];