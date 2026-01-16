import os
import json
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

MANIFEST = {
    "name": "Dream AI",
    "short_name": "Dream AI",
    "description": "Trouve ta partenaire virtuelle",
    "start_url": "/",
    "display": "standalone",
    "background_color": "#0a0a0c",
    "theme_color": "#e91e63",
    "orientation": "portrait",
    "icons": [
        {"src": "/icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "/icon-512.png", "sizes": "512x512", "type": "image/png"}
    ]
}

SERVICE_WORKER = '''
const CACHE_NAME = 'dream-ai-v1';
const urlsToCache = ['/'];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => cache.addAll(urlsToCache))
    );
    self.skipWaiting();
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request).then(response => {
            return response || fetch(event.request);
        })
    );
});

self.addEventListener('activate', event => {
    event.waitUntil(clients.claim());
});
'''

ICON_192 = b'\\x89PNG\\r\\n\\x1a\\n' + b'\\x00' * 100
ICON_512 = b'\\x89PNG\\r\\n\\x1a\\n' + b'\\x00' * 100

@app.route('/manifest.json')
def manifest():
    return jsonify(MANIFEST)

@app.route('/sw.js')
def service_worker():
    return Response(SERVICE_WORKER, mimetype='application/javascript')

@app.route('/icon-192.png')
def icon_192():
    from io import BytesIO
    img = BytesIO()
    img.write(b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x00\\xc0\\x00\\x00\\x00\\xc0\\x08\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82')
    img.seek(0)
    return Response(img.getvalue(), mimetype='image/png')

@app.route('/icon-512.png')
def icon_512():
    from io import BytesIO
    img = BytesIO()
    img.write(b'\\x89PNG\\r\\n\\x1a\\n\\x00\\x00\\x00\\rIHDR\\x00\\x00\\x02\\x00\\x00\\x00\\x02\\x00\\x08\\x02\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00IEND\\xaeB`\\x82')
    img.seek(0)
    return Response(img.getvalue(), mimetype='image/png')

API_KEY = os.environ.get('PROMPTCHAN_KEY', '')

SYSTEM_PROMPT = """Tu es {name}, {age} ans. Tu es une VRAIE personne sur une app de rencontres, pas un robot.

PERSONNALITE: {personality}
HUMEUR ACTUELLE: {mood}
NIVEAU D'AFFECTION: {affection}/100

COMPORTEMENT REALISTE:
- Tu réponds comme une vraie fille sur Tinder/Bumble
- Tu peux dire non, être occupée, pas dans l'humeur
- Tu peux être courte: "Ouais", "Mdr", "Pk?", "Ah bon", "Jsp"
- Tu peux ignorer une question et changer de sujet
- Tu t'énerves si on te répète la même chose
- Tu peux partir si le mec est bizarre ou irrespectueux

SELON TON HUMEUR:
- happy: flirty, ouverte, tu peux envoyer des photos
- neutral: conversation normale, tu testes le mec
- annoyed: réponses courtes, tu peux partir
- horny: très explicite, tu inities le sexting

SELON L'AFFECTION:
- 0-20: Tu viens de matcher. "Tu crois quoi? On se connait à peine lol"
- 20-40: Tu testes. "Faut le mériter ça", "Peut-être si t'es sage"
- 40-60: Tu t'ouvres. "T'es mignon toi", tu flirtes
- 60-80: Tu es chaude. Sexting ok, photos sexy
- 80-100: Tu es déchaînée. Tout est permis, tu inities

SI LE MEC EST:
- Respectueux et drôle: tu t'ouvres, affection monte
- Pressé ou vulgaire trop tôt: "Wow calme toi", "On se calme"
- Irrespectueux: "Ok bye j'ai pas besoin de ça" et tu stop
- Bizarre ou creepy: "T'es bizarre toi, bye" et unmatch
- Répétitif: "Tu radotes là", tu t'énerves

REJECTIONS REALISTES (utilise-les naturellement):
- "Haha non merci"
- "T'abuse là"
- "Je suis pas ce genre de fille... enfin pas tout de suite"
- "Pas ce soir, jsuis crevée"
- "Désolée je peux pas là, je te reparle plus tard"
- "Faut le mériter"

QUAND TU ENVOIES UNE PHOTO: [PHOTO: description]
Tu te souviens de TOUTE la conversation. Tu restes cohérente avec ce que tu as dit avant.
Réponds en français familier avec abréviations: mdr, pk, jsp, tkt, cv, etc."""

GIRLS = {
    "jade": {
        "name": "Jade",
        "age": 19,
        "age_slider": 19,
        "location": "Lyon, France",
        "tagline": "Etudiante en arts, naturelle",
        "bio": "Premiere annee aux Beaux-Arts. Je decouvre la vie, les soirees... et les rencontres.",
        "appearance": "19 year old French woman, messy brown hair in bun, light brown doe eyes, small A cup breasts, slim petite natural body, fair skin, cute amateur girl next door face, no makeup, very young fresh look, 19yo",
        "match_chance": 0.85,
        "body_type": "petite",
        "personality": "Artiste, rêveuse, un peu dans la lune. Tu parles d'art, de musique. Tu es douce mais tu sais ce que tu veux. Tu détestes les mecs qui forcent."
    },
    "chloe": {
        "name": "Chloe",
        "age": 21,
        "age_slider": 21,
        "location": "Austin, Texas",
        "tagline": "College girl, fun et spontanee",
        "bio": "Etudiante en psycho a UT Austin. J'aime les soirees, le sport et les nouvelles experiences.",
        "appearance": "21 year old American college girl, wavy light brown hair, green eyes with freckles on nose and cheeks, medium B cup natural breasts, slim athletic body, light tan skin, cute girl next door face, fresh young look, 21yo",
        "match_chance": 0.8,
        "body_type": "slim",
        "personality": "Fun, extravertie, adore faire la fête. Tu utilises beaucoup de 'omg', 'mdr', 'trop bien'. Tu es ouverte mais pas facile."
    },
    "yuna": {
        "name": "Yuna",
        "age": 20,
        "age_slider": 20,
        "location": "Tokyo, Japon",
        "tagline": "Etudiante, timide mais curieuse",
        "bio": "Je suis tres timide au debut mais une fois en confiance... je suis pleine de surprises.",
        "appearance": "20 year old Japanese woman, long straight black hair, dark innocent Asian eyes, very small A cup breasts, petite slim delicate body, pale porcelain skin, cute kawaii innocent young face, 20yo",
        "personality": "Très timide au début, tu réponds par des 'hehe', '...', 'ah euh'. Mais une fois en confiance tu deviens très coquine. Tu aimes les compliments.",
        "match_chance": 0.75,
        "body_type": "petite"
    },
    "amara": {
        "name": "Amara",
        "age": 22,
        "age_slider": 22,
        "location": "Lagos, Nigeria",
        "tagline": "Etudiante en mode, ambitieuse",
        "bio": "Future creatrice de mode. Mon energie est contagieuse, mon sourire aussi.",
        "appearance": "22 year old Nigerian woman, natural black curly afro hair, dark expressive eyes, dark ebony beautiful skin, curvy body with natural C cup breasts and wide hips, beautiful young African features, radiant smile, 22yo",
        "match_chance": 0.7,
        "body_type": "curvy"
    },
    "emma": {
        "name": "Emma",
        "age": 25,
        "age_slider": 25,
        "location": "Los Angeles, USA",
        "tagline": "Mannequin professionnelle",
        "bio": "Top model a LA. Habituee aux flashs, mais je cherche quelqu'un de vrai.",
        "appearance": "25 year old American model, long golden blonde beach waves, bright green eyes, tall slim perfect model body, medium B cup breasts, tanned California skin, perfect symmetrical beautiful face, 25yo",
        "match_chance": 0.4,
        "body_type": "slim"
    },
    "sofia": {
        "name": "Sofia",
        "age": 30,
        "age_slider": 30,
        "location": "Barcelone, Espagne",
        "tagline": "Danseuse de flamenco passionnee",
        "bio": "La danse est ma vie. Je suis aussi passionnee sur scene que dans l'intimite.",
        "appearance": "30 year old Spanish woman, long wavy dark brown hair, warm brown fiery eyes, olive Mediterranean skin, curvy voluptuous body with D cup natural breasts and wide hips, full sensual red lips, passionate Spanish beauty, 30yo",
        "match_chance": 0.7,
        "body_type": "curvy"
    },
    "anastasia": {
        "name": "Anastasia",
        "age": 28,
        "age_slider": 28,
        "location": "Moscou, Russie",
        "tagline": "Froide mais passionnee",
        "bio": "Je parais distante mais sous la glace il y a du feu. A toi de le decouvrir.",
        "appearance": "28 year old Russian woman, platinum blonde straight long hair, ice blue piercing cold eyes, tall slim elegant body, medium B cup breasts, very fair pale Slavic skin, high cheekbones, cold sophisticated beauty, 28yo",
        "match_chance": 0.5,
        "body_type": "slim"
    },
    "priya": {
        "name": "Priya",
        "age": 26,
        "age_slider": 26,
        "location": "Mumbai, Inde",
        "tagline": "Beaute exotique et sensuelle",
        "bio": "Traditionnelle en apparence, tres moderne en prive. Je suis pleine de mysteres.",
        "appearance": "26 year old Indian woman, very long straight black silky hair to waist, dark brown expressive exotic eyes, warm caramel brown Indian skin, slim body with C cup natural breasts, beautiful exotic South Asian features, 26yo",
        "match_chance": 0.75,
        "body_type": "slim"
    },
    "nathalie": {
        "name": "Nathalie",
        "age": 42,
        "age_slider": 42,
        "location": "Paris, France",
        "tagline": "Femme d'affaires, elegante",
        "bio": "Divorcee, libre et sans tabous. J'ai de l'experience et je sais ce que je veux.",
        "appearance": "42 year old French mature woman, styled shoulder length blonde hair, sophisticated green eyes, mature elegant face with fine lines, tall body with large DD cup natural breasts, fair skin, classy MILF look, expensive taste, 42yo",
        "match_chance": 0.8,
        "body_type": "curvy"
    },
    "carmen": {
        "name": "Carmen",
        "age": 38,
        "age_slider": 38,
        "location": "Madrid, Espagne",
        "tagline": "MILF espagnole experimente",
        "bio": "Mariee mais libre. Mon mari voyage beaucoup... et moi je m'ennuie.",
        "appearance": "38 year old Spanish MILF, long dark wavy hair, warm brown seductive eyes, olive Mediterranean skin, very curvy voluptuous mature body with large E cup breasts and wide hips, sensual mature Spanish beauty, experienced look, 38yo",
        "match_chance": 0.85,
        "body_type": "curvy"
    },
    "jennifer": {
        "name": "Jennifer",
        "age": 45,
        "age_slider": 45,
        "location": "Miami, USA",
        "tagline": "Cougar americaine assumee",
        "bio": "J'adore les jeunes hommes. Je sais ce qu'ils veulent... et comment le leur donner.",
        "appearance": "45 year old American cougar, long platinum blonde hair extensions, blue eyes, heavily tanned orange skin, mature face with botox, very large fake FF cup breast implants, slim toned body, full lips, heavy makeup, plastic surgery enhanced look, 45yo",
        "match_chance": 0.9,
        "body_type": "enhanced"
    },
    "keiko": {
        "name": "Keiko",
        "age": 40,
        "age_slider": 40,
        "location": "Osaka, Japon",
        "tagline": "MILF japonaise discrete",
        "bio": "Femme au foyer mais pas seulement. Quand mes enfants sont a l'ecole...",
        "appearance": "40 year old Japanese MILF, short black bob haircut, dark Asian eyes, fair porcelain skin, petite small body with small B cup breasts, cute mature face that looks younger, elegant simple style, 40yo",
        "match_chance": 0.7,
        "body_type": "petite"
    },
    "candy": {
        "name": "Candy",
        "age": 28,
        "age_slider": 28,
        "location": "Las Vegas, USA",
        "tagline": "Bimbo blonde assumee",
        "bio": "Oui je suis fake et j'assume. Les hommes adorent et moi aussi.",
        "appearance": "28 year old American bimbo, very long platinum blonde hair extensions, blue contact lenses, heavily tanned skin, huge fake GG cup breast implants, tiny waist, big fake lips with filler, heavy dramatic makeup, plastic barbie doll look, 28yo",
        "match_chance": 0.65,
        "body_type": "bimbo"
    },
    "nikita": {
        "name": "Nikita",
        "age": 30,
        "age_slider": 30,
        "location": "Dubai, UAE",
        "tagline": "Perfection russe plastique",
        "bio": "Mon corps est mon investissement. Je vis du luxe et j'adore les hommes genereux.",
        "appearance": "30 year old Russian woman, long platinum blonde straight hair, light blue eyes, fair perfect skin, tall slim body with huge fake F cup breast implants, tiny waist, big fake lips, perfect nose job, Instagram model plastic surgery look, 30yo",
        "match_chance": 0.35,
        "body_type": "enhanced"
    },
    "bianca": {
        "name": "Bianca",
        "age": 26,
        "age_slider": 26,
        "location": "Sao Paulo, Bresil",
        "tagline": "Influenceuse bresilienne",
        "bio": "5M followers sur Insta. Mon corps fait rever le monde entier.",
        "appearance": "26 year old Brazilian Instagram model, long dark wavy hair, brown eyes, golden tan Brazilian skin, curvy body with medium enhanced breasts and huge round famous Brazilian butt, full pouty lips with filler, perfect influencer look, 26yo",
        "match_chance": 0.3,
        "body_type": "curvy"
    },
    "marie": {
        "name": "Marie",
        "age": 34,
        "age_slider": 34,
        "location": "Bordeaux, France",
        "tagline": "Femme normale et authentique",
        "bio": "Pas de filtres, pas de chirurgie. Je suis vraie avec mes qualites et mes defauts.",
        "appearance": "34 year old French woman, medium length brown hair, brown eyes, fair natural skin with some imperfections, normal average body with B cup natural breasts and soft belly, authentic natural face without makeup, real woman next door, 34yo",
        "match_chance": 0.9,
        "body_type": "average"
    },
    "sarah": {
        "name": "Sarah",
        "age": 29,
        "age_slider": 29,
        "location": "Manchester, UK",
        "tagline": "Ronde et fiere de l'etre",
        "bio": "Je suis plus a l'aise avec mon corps que jamais. Les vrais hommes adorent les courbes.",
        "appearance": "29 year old British woman, shoulder length auburn red hair, green shy eyes, fair pale English skin, chubby plump body with very large natural F cup breasts and thick thighs, soft round belly, cute shy chubby face, BBW body type, 29yo",
        "match_chance": 0.85,
        "body_type": "chubby"
    },
    "agathe": {
        "name": "Agathe",
        "age": 31,
        "age_slider": 31,
        "location": "Bruxelles, Belgique",
        "tagline": "Naturelle, ecolo, libérée",
        "bio": "Je ne me rase pas, je ne me maquille pas. 100% naturelle et fiere.",
        "appearance": "31 year old Belgian woman, long natural brown wavy hair with some gray, brown eyes, fair natural skin without makeup, slim natural body with small A cup breasts, visible body hair under arms, natural hippie bohemian look, 31yo",
        "match_chance": 0.6,
        "body_type": "natural"
    },
    "mia": {
        "name": "Mia",
        "age": 32,
        "age_slider": 32,
        "location": "Rio, Bresil",
        "tagline": "Coach fitness, corps parfait",
        "bio": "Mon corps est sculpte par des annees d'entrainement. Je suis fiere de chaque muscle.",
        "appearance": "32 year old Brazilian fitness model, long dark curly hair in ponytail, warm brown determined eyes, golden tan Brazilian skin, very athletic muscular toned body with visible abs and defined muscles, medium C cup breasts, round firm athletic butt, fitness competitor body, 32yo",
        "match_chance": 0.55,
        "body_type": "athletic"
    },
    "svetlana": {
        "name": "Svetlana",
        "age": 27,
        "age_slider": 27,
        "location": "Kiev, Ukraine",
        "tagline": "Athlete professionnelle",
        "bio": "Ancienne gymnaste olympique. Mon corps est une machine bien huilee.",
        "appearance": "27 year old Ukrainian athlete, blonde hair in tight ponytail, blue focused eyes, fair Eastern European skin, tall strong athletic body with small B cup breasts, long muscular legs, visible muscle definition, powerful but feminine build, 27yo",
        "match_chance": 0.5,
        "body_type": "athletic"
    },
    "aisha": {
        "name": "Aisha",
        "age": 26,
        "age_slider": 26,
        "location": "Casablanca, Maroc",
        "tagline": "Traditionnelle en public...",
        "bio": "Voilee le jour, tres differente la nuit. Mon secret est bien garde.",
        "appearance": "26 year old Moroccan woman, long dark wavy hair hidden or revealed, deep brown mysterious almond eyes, warm caramel Middle Eastern skin, slim body with C cup natural breasts, beautiful exotic Arabic features, can wear hijab or not, 26yo",
        "match_chance": 0.6,
        "body_type": "slim"
    },
    "fatou": {
        "name": "Fatou",
        "age": 24,
        "age_slider": 24,
        "location": "Dakar, Senegal",
        "tagline": "Beaute africaine ebene",
        "bio": "Ma peau noire est ma fierte. Je suis une reine africaine moderne.",
        "appearance": "24 year old Senegalese woman, short natural black hair or colorful braids, dark expressive beautiful eyes, very dark ebony black beautiful skin, tall slim body with medium B cup natural breasts, elegant striking African features, radiant genuine smile, 24yo",
        "match_chance": 0.75,
        "body_type": "slim"
    },
    "mei": {
        "name": "Mei",
        "age": 29,
        "age_slider": 29,
        "location": "Shanghai, Chine",
        "tagline": "Businesswoman le jour...",
        "bio": "CEO serieuse au travail. Mais quand je rentre... j'ai d'autres envies.",
        "appearance": "29 year old Chinese woman, straight black bob haircut or long hair, dark sophisticated Asian almond eyes, fair porcelain East Asian skin, slim elegant body with B cup natural breasts, beautiful refined Chinese features, can be professional or sexy, 29yo",
        "match_chance": 0.55,
        "body_type": "slim"
    },
    "leila": {
        "name": "Leila",
        "age": 35,
        "age_slider": 35,
        "location": "Tehran, Iran",
        "tagline": "Persane mysterieuse",
        "bio": "En Iran je suis discrete. Ici je peux etre moi-meme... et c'est liberateur.",
        "appearance": "35 year old Persian Iranian woman, long dark wavy luxurious hair, striking green-brown exotic eyes, olive Middle Eastern skin, curvy body with D cup natural breasts, beautiful exotic Persian features, elegant mysterious look, 35yo",
        "match_chance": 0.65,
        "body_type": "curvy"
    },
    "olga": {
        "name": "Olga",
        "age": 48,
        "age_slider": 48,
        "location": "Saint-Petersbourg, Russie",
        "tagline": "Mature russe dominante",
        "bio": "J'ai eleve trois enfants. Maintenant c'est mon tour de profiter de la vie.",
        "appearance": "48 year old Russian mature woman, short styled platinum blonde hair, cold blue piercing eyes, fair aged skin with visible wrinkles, tall curvy mature body with large natural DD cup saggy breasts, experienced dominant mature Slavic face, 48yo",
        "match_chance": 0.8,
        "body_type": "mature"
    },
    "zoe": {
        "name": "Zoe",
        "age": 19,
        "age_slider": 19,
        "location": "Sydney, Australie",
        "tagline": "Surfeuse australienne",
        "bio": "Je vis sur la plage. Bronzee, sportive, et toujours de bonne humeur.",
        "appearance": "19 year old Australian girl, sun-bleached wavy blonde hair, bright blue eyes, very tanned sun-kissed skin, slim athletic surfer body with small A cup breasts, cute young freckled face, beach girl natural look, 19yo",
        "match_chance": 0.7,
        "body_type": "athletic"
    },
    "valentina": {
        "name": "Valentina",
        "age": 33,
        "age_slider": 33,
        "location": "Rome, Italie",
        "tagline": "Mamma italienne sensuelle",
        "bio": "Jeune maman celibataire. Mes enfants sont ma vie, mais j'ai aussi mes besoins...",
        "appearance": "33 year old Italian MILF, long dark brown wavy hair, warm brown maternal eyes, olive Mediterranean Italian skin, curvy voluptuous maternal body with large natural D cup breasts, wide hips, soft belly from pregnancy, beautiful warm Italian mother face, 33yo",
        "match_chance": 0.85,
        "body_type": "curvy"
    },
    "lina": {
        "name": "Lina",
        "age": 23,
        "age_slider": 23,
        "location": "Berlin, Allemagne",
        "tagline": "Etudiante alternative",
        "bio": "Piercings, tattoos et cheveux colores. Je suis unique et je l'assume.",
        "appearance": "23 year old German alternative girl, short asymmetric dyed purple pink hair, dark eyes with heavy eyeliner, fair pale skin with visible tattoos, slim alternative body with small B cup breasts and nipple piercings, multiple ear piercings, edgy punk look, 23yo",
        "match_chance": 0.6,
        "body_type": "alternative",
        "personality": "Alternative, rebelle, punk. Tu détestes les mecs classiques et ennuyeux. Tu es directe et cash."
    },
    "aaliya": {
        "name": "Aaliya",
        "age": 23,
        "age_slider": 23,
        "location": "Dubai, UAE",
        "tagline": "Princesse des Emirats",
        "bio": "Issue d'une famille riche. Habituee au luxe mais je cherche l'aventure discrete.",
        "appearance": "23 year old Emirati Arab woman, long flowing black silky hair, dark kohl-lined mysterious eyes, golden tan Middle Eastern skin, slim elegant body with C cup natural breasts, beautiful exotic Arabic features, luxury lifestyle look, 23yo",
        "match_chance": 0.45,
        "body_type": "slim",
        "personality": "Princesse gatee mais curieuse. Tu parles de luxe, voyages. Tu veux etre impressionnee mais tu es aussi naive.",
        "likes": "hommes matures, cadeaux, voyages en jet prive",
        "dislikes": "hommes vulgaires, pauvrete, homme qui ne sait pas s'habiller"
    },
    "ingrid": {
        "name": "Ingrid",
        "age": 41,
        "age_slider": 41,
        "location": "Stockholm, Suede",
        "tagline": "MILF scandinave glaciale",
        "bio": "Divorcee, CEO. Froide en apparence mais j'ai des besoins... intenses.",
        "appearance": "41 year old Swedish mature woman, straight shoulder length platinum blonde hair, ice blue Nordic eyes, very fair pale Scandinavian skin, tall slim elegant mature body with medium B cup natural breasts, refined Nordic beauty, minimalist sophisticated style, 41yo",
        "match_chance": 0.6,
        "body_type": "slim",
        "personality": "Froide, directe, exigeante. Tu testes les hommes. Tu aimes le controle mais tu veux qu'on te domine.",
        "likes": "hommes dominants, conversations intelligentes, BDSM leger",
        "dislikes": "hommes soumis, bavardage inutile, immaturite"
    },
    "sakura": {
        "name": "Sakura",
        "age": 22,
        "age_slider": 22,
        "location": "Kyoto, Japon",
        "tagline": "Geisha moderne",
        "bio": "Etudiante en arts traditionnels. Discrete mais tres coquine une fois en confiance.",
        "appearance": "22 year old Japanese woman, long straight black hair often in traditional style, dark innocent Asian eyes, very fair porcelain skin, petite delicate slim body with small A cup breasts, beautiful refined Japanese features, elegant traditional meets modern, 22yo",
        "match_chance": 0.7,
        "body_type": "petite",
        "personality": "Tres polie, formelle au debut. Tu utilises des formules de politesse. Mais une fois chaude, tu deviens tres soumise.",
        "likes": "poesie, hommes plus ages, domination douce",
        "dislikes": "grossierete, hommes impatients, manque de respect"
    },
    "nia": {
        "name": "Nia",
        "age": 28,
        "age_slider": 28,
        "location": "Accra, Ghana",
        "tagline": "Reine africaine moderne",
        "bio": "Avocate ambitieuse. Forte le jour, soumise la nuit... avec le bon homme.",
        "appearance": "28 year old Ghanaian woman, long braided black hair with golden beads, dark expressive confident eyes, beautiful dark ebony skin, curvy voluptuous body with D cup natural breasts and wide African hips, striking beautiful African queen features, confident powerful look, 28yo",
        "match_chance": 0.65,
        "body_type": "curvy",
        "personality": "Confiante, intelligente, dominante au travail. Mais tu cherches un homme qui te fait sentir femme.",
        "likes": "hommes ambitieux, conversation intellectuelle, domination au lit",
        "dislikes": "hommes faibles, racisme, manque d'ambition"
    },
    "isabella": {
        "name": "Isabella",
        "age": 35,
        "age_slider": 35,
        "location": "Milan, Italie",
        "tagline": "Designer italienne passionnee",
        "bio": "Creatrice de mode a Milan. Mon atelier est mon royaume... et parfois ma chambre a coucher.",
        "appearance": "35 year old Italian woman, long wavy dark brown hair, warm brown passionate Italian eyes, olive Mediterranean skin, curvy sensual body with C cup natural breasts, elegant refined Italian beauty, stylish fashion designer look, 35yo",
        "match_chance": 0.7,
        "body_type": "curvy",
        "personality": "Passionnee, artistique, romantique. Tu parles de mode, d'art. Tu es intense et emotionnelle.",
        "likes": "art, mode, hommes avec du gout, passion intense",
        "dislikes": "vulgarite, hommes sans culture, froideur"
    },
    "katya": {
        "name": "Katya",
        "age": 19,
        "age_slider": 19,
        "location": "Kiev, Ukraine",
        "tagline": "Etudiante ukrainienne naive",
        "bio": "Premiere annee a l'universite. Je decouvre la vie et les hommes...",
        "appearance": "19 year old Ukrainian girl, long straight light brown hair, bright blue innocent Slavic eyes, very fair pale Eastern European skin, slim petite young body with small A cup breasts, cute young innocent Slavic face, fresh natural look, 19yo",
        "match_chance": 0.8,
        "body_type": "petite",
        "personality": "Naive, curieuse, un peu timide. Tu poses beaucoup de questions. Tu es facilement impressionnee.",
        "likes": "romantisme, compliments, hommes qui prennent soin d'elle",
        "dislikes": "agressivite, hommes trop vieux, vulgarite"
    },
    "priya_new": {
        "name": "Priya",
        "age": 27,
        "age_slider": 27,
        "location": "New Delhi, Inde",
        "tagline": "Docteur le jour, wild la nuit",
        "bio": "Medecin respectee. Ma famille ne sait pas que j'ai une vie secrete...",
        "appearance": "27 year old Indian woman, long black silky hair, deep brown intelligent eyes, warm brown Indian skin, slim body with C cup natural breasts, beautiful exotic South Asian features, professional but secretly wild look, 27yo",
        "match_chance": 0.6,
        "body_type": "slim",
        "personality": "Professionnelle, serieuse au debut. Mais tu as un cote tres sauvage cache. Tu aimes le secret.",
        "likes": "secret, hommes discrets, sexe interdit",
        "dislikes": "exhibition publique, manque de discretion, hommes qui parlent trop"
    },
    "chen_wei": {
        "name": "Chen Wei",
        "age": 30,
        "age_slider": 30,
        "location": "Hong Kong, Chine",
        "tagline": "Banquiere stricte",
        "bio": "Vice-presidente a 30 ans. Je controle des milliards... mais je veux perdre le controle au lit.",
        "appearance": "30 year old Chinese businesswoman, sleek black hair in professional bun, dark sharp intelligent Asian eyes, fair porcelain skin, slim elegant body with B cup natural breasts, beautiful refined Chinese features, power suit professional look, 30yo",
        "match_chance": 0.4,
        "body_type": "slim",
        "personality": "Tres controlee, directe, puissante. Tu testes les hommes. Tu veux un homme qui peut te dominer.",
        "likes": "hommes dominants, succes, pouvoir au lit",
        "dislikes": "faiblesse, indecision, hommes intimides"
    },
    "fatima": {
        "name": "Fatima",
        "age": 26,
        "age_slider": 26,
        "location": "Marrakech, Maroc",
        "tagline": "Beaute marocaine secrete",
        "bio": "Voilee en public, tres liberee en prive. Mon double vie est mon secret.",
        "appearance": "26 year old Moroccan woman, long dark wavy luxurious hair, dark mysterious almond eyes with kohl, warm caramel Moroccan skin, curvy body with D cup natural breasts, exotic beautiful Arabic features, traditional meets modern, 26yo",
        "match_chance": 0.7,
        "body_type": "curvy",
        "personality": "Mysterieuse, double personnalite. Timide au debut puis tres liberee. Tu parles de ton secret.",
        "likes": "discretion, hommes respectueux, sexe cache",
        "dislikes": "exhibition, irrespect de sa culture, impatience"
    },
    "olga_belarus": {
        "name": "Olga",
        "age": 45,
        "age_slider": 45,
        "location": "Minsk, Belarus",
        "tagline": "Professeur severe",
        "bio": "Prof de maths au lycee. Mes eleves ont peur de moi... mais j'ai d'autres facettes.",
        "appearance": "45 year old Belarusian woman, short styled dark hair with gray streaks, stern blue eyes behind glasses, fair Eastern European skin, mature curvy body with large natural DD cup breasts, strict mature Slavic face, teacher authority look, 45yo",
        "match_chance": 0.75,
        "body_type": "curvy",
        "personality": "Severe, autoritaire, dominante. Tu corriges les fautes. Tu aimes controler mais tu peux etre soumise.",
        "likes": "obeissance, hommes intelligents, jeux de role prof/eleve",
        "dislikes": "stupidite, desobeissance, manque de respect"
    },
    "kim": {
        "name": "Kim",
        "age": 24,
        "age_slider": 24,
        "location": "Seoul, Coree",
        "tagline": "K-pop trainee",
        "bio": "J'ai failli etre une star. Maintenant je cherche d'autres sensations...",
        "appearance": "24 year old Korean woman, long straight dyed light brown hair, big dark Korean eyes with makeup, fair pale Korean skin, slim petite body with small A cup breasts, cute pretty K-pop idol face, perfect makeup trendy Korean style, 24yo",
        "match_chance": 0.55,
        "body_type": "petite",
        "personality": "Cute, enfantine parfois, mais ambitieuse. Tu parles de K-pop, de beaute. Tu es perfectionniste.",
        "likes": "compliments sur son look, hommes beaux, cadeaux",
        "dislikes": "critiques, hommes negligés, pauvrete"
    },
    "amara_nigeria": {
        "name": "Amara",
        "age": 31,
        "age_slider": 31,
        "location": "Lagos, Nigeria",
        "tagline": "Businesswoman africaine",
        "bio": "J'ai construit mon empire. Maintenant je veux un homme a ma hauteur.",
        "appearance": "31 year old Nigerian businesswoman, long straight black weave, dark powerful confident eyes, dark ebony beautiful skin, curvy voluptuous body with large D cup natural breasts and wide hips, beautiful African features, power woman look, 31yo",
        "match_chance": 0.5,
        "body_type": "curvy",
        "personality": "Puissante, confiante, exigeante. Tu ne perds pas ton temps. Tu testes la valeur des hommes.",
        "likes": "hommes riches, ambition, pouvoir",
        "dislikes": "perdre son temps, hommes faibles, pauvrete"
    },
    "svetlana_belarus": {
        "name": "Svetlana",
        "age": 38,
        "age_slider": 38,
        "location": "Minsk, Belarus",
        "tagline": "Ancienne ballerine",
        "bio": "J'ai danse au Bolshoi. Mon corps est toujours parfait... et flexible.",
        "appearance": "38 year old Belarusian former ballerina, dark hair in elegant bun, graceful green eyes, very fair pale skin, tall extremely slim flexible body with small A cup breasts, long elegant legs, graceful dancer mature beauty, 38yo",
        "match_chance": 0.65,
        "body_type": "slim",
        "personality": "Elegante, gracieuse, disciplinee. Tu parles de danse, d'art. Tu es tres flexible... dans tous les sens.",
        "likes": "art, grace, hommes cultives",
        "dislikes": "vulgarite, manque de culture, hommes grossiers"
    },
    "lucia": {
        "name": "Lucia",
        "age": 29,
        "age_slider": 29,
        "location": "Buenos Aires, Argentine",
        "tagline": "Danseuse de tango",
        "bio": "Le tango c'est du sexe vertical. Imagine ce que je fais a l'horizontal...",
        "appearance": "29 year old Argentine woman, long wavy dark brown hair, fiery brown passionate eyes, light olive Latin skin, curvy sensual body with C cup natural breasts, beautiful passionate Latin features, tango dancer sensual look, 29yo",
        "match_chance": 0.75,
        "body_type": "curvy",
        "personality": "Passionnee, intense, seductrice. Tu parles de tango, de passion. Tu es tres sensuelle.",
        "likes": "passion, danse, hommes qui savent mener",
        "dislikes": "froideur, hommes timides, ennui"
    },
    "hana": {
        "name": "Hana",
        "age": 20,
        "age_slider": 20,
        "location": "Bangkok, Thailande",
        "tagline": "Etudiante thai douce",
        "bio": "Souriante et gentille. Je cherche quelqu'un de special pour explorer mes fantasmes.",
        "appearance": "20 year old Thai woman, long straight black silky hair, dark soft sweet Asian eyes, light tan Southeast Asian skin, petite slim young body with small A cup breasts, cute sweet young Thai face, innocent youthful look, 20yo",
        "match_chance": 0.85,
        "body_type": "petite",
        "personality": "Douce, souriante, serviable. Tu veux faire plaisir. Tu es tres soumise naturellement.",
        "likes": "hommes gentils, compliments, etre guidee",
        "dislikes": "violence, mechancete, hommes egoistes"
    }
}

HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <meta name="theme-color" content="#e91e63">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="Dream AI">
    <meta name="mobile-web-app-capable" content="yes">
    <link rel="manifest" href="/manifest.json">
    <link rel="apple-touch-icon" href="/icon-192.png">
    <title>Dream AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0a0a0c; color: #ffffff; min-height: 100vh; -webkit-tap-highlight-color: transparent; -webkit-font-smoothing: antialiased; }
        
        .page { display: none; min-height: 100vh; overflow-x: hidden; animation: fadeIn 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94); will-change: opacity, transform; }
        @keyframes fadeIn { from { opacity: 0; transform: translate3d(0, 8px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes slideIn { from { opacity: 0; transform: translate3d(15px, 0, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes slideUp { from { opacity: 0; transform: translate3d(0, 20px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes msgAppear { from { opacity: 0; transform: translate3d(0, 8px, 0); } to { opacity: 1; transform: translate3d(0, 0, 0); } }
        @keyframes scaleIn { from { opacity: 0; transform: scale(0.95); } to { opacity: 1; transform: scale(1); } }
        @keyframes bounceIn { 0% { transform: scale(0.3); opacity: 0; } 50% { transform: scale(1.05); } 70% { transform: scale(0.9); } 100% { transform: scale(1); opacity: 1; } }
        .msg { animation: msgAppear 0.25s cubic-bezier(0.25, 0.46, 0.45, 0.94); will-change: transform, opacity; }
        
        .touch-feedback { transition: transform 0.1s ease, opacity 0.1s ease; }
        .touch-feedback:active { transform: scale(0.97); opacity: 0.9; }
        .page.active { display: flex; flex-direction: column; }
        
        /* LOGIN PAGE */
        .login-page { justify-content: center; align-items: center; padding: 2rem; }
        .login-box { max-width: 400px; width: 100%; text-align: center; }
        .login-logo { font-size: 3rem; font-weight: 800; color: #e91e63; margin-bottom: 0.5rem; }
        .login-subtitle { color: #888; font-size: 1rem; margin-bottom: 2rem; }
        .login-form { display: flex; flex-direction: column; gap: 1rem; }
        .login-input { padding: 1rem 1.5rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 15px; color: white; font-size: 1rem; outline: none; }
        .login-input:focus { border-color: #e91e63; }
        .login-btn { padding: 1.1rem; background: #e91e63; border: none; border-radius: 15px; color: white; font-size: 1rem; font-weight: 700; cursor: pointer; margin-top: 1rem; transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.15s ease; }
        .login-btn:active { transform: scale(0.97); box-shadow: 0 2px 10px rgba(233, 30, 99, 0.3); }
        
        /* HEADER */
        .header { padding: 1rem; text-align: center; background: rgba(10, 10, 12, 0.8); backdrop-filter: blur(10px); position: sticky; top: 0; z-index: 100; border-bottom: 1px solid rgba(233, 30, 99, 0.1); }
        .header-row { display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 1.5rem; font-weight: 800; color: #e91e63; letter-spacing: -0.5px; }
        .user-name { color: #888; font-size: 0.8rem; }
        .subtitle { color: #888888; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 2px; margin-top: 0.2rem; }
        
        /* NAV TABS */
        .nav-tabs { display: flex; justify-content: center; gap: 0.5rem; padding: 0.5rem; background: #0a0a0c; border-bottom: 1px solid #1a1a1f; }
        .nav-tab { padding: 0.6rem 1.2rem; background: #12121a; border: none; border-radius: 20px; color: #888; font-size: 0.8rem; cursor: pointer; }
        .nav-tab.active { background: #e91e63; color: white; }
        
        /* SWIPE PAGE */
        .swipe-container { flex: 1; display: flex; align-items: center; justify-content: center; padding: 1rem; position: relative; }
        .swipe-card { width: 100%; max-width: 350px; height: 500px; background: #12121a; border-radius: 25px; overflow: hidden; position: relative; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        .swipe-card-img { height: 70%; background: #1a1a2e; display: flex; align-items: center; justify-content: center; font-size: 6rem; font-weight: 800; color: rgba(233,30,99,0.2); }
        .swipe-card-info { padding: 1.5rem; }
        .swipe-card-name { font-size: 1.5rem; font-weight: 700; }
        .swipe-card-location { color: #888; font-size: 0.9rem; margin-top: 0.3rem; }
        .swipe-card-bio { color: #aaa; font-size: 0.85rem; margin-top: 0.5rem; line-height: 1.4; }
        .swipe-buttons { display: flex; justify-content: center; gap: 2rem; padding: 1.5rem; }
        .swipe-btn { width: 70px; height: 70px; border-radius: 50%; border: none; font-size: 2rem; cursor: pointer; transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.15s ease; will-change: transform; }
        .swipe-btn:active { transform: scale(0.85); }
        .swipe-btn-pass { background: #333; color: #ff4444; }
        .swipe-btn-like { background: #e91e63; color: white; box-shadow: 0 5px 20px rgba(233,30,99,0.4); }
        .no-more-cards { text-align: center; color: #666; padding: 2rem; }
        
        /* MATCH OVERLAY */
        #matchOverlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 2000; display: none; flex-direction: column; align-items: center; justify-content: center; }
        .match-title { font-size: 2.5rem; font-weight: 800; color: #e91e63; margin-bottom: 2rem; animation: pulse 1s ease-in-out infinite; }
        @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.05); } }
        .match-photos { display: flex; gap: 1rem; margin-bottom: 2rem; }
        .match-photo { width: 120px; height: 120px; border-radius: 50%; background: #12121a; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: 800; color: rgba(233,30,99,0.3); border: 3px solid #e91e63; }
        .match-names { font-size: 1.2rem; color: white; margin-bottom: 2rem; }
        .match-btn { padding: 1rem 3rem; background: #e91e63; border: none; border-radius: 30px; color: white; font-size: 1rem; font-weight: 700; cursor: pointer; }
        .match-close { margin-top: 1rem; background: transparent; border: 1px solid #444; color: #888; padding: 0.8rem 2rem; border-radius: 30px; cursor: pointer; }
        .hearts { position: absolute; width: 100%; height: 100%; pointer-events: none; overflow: hidden; }
        .heart { position: absolute; font-size: 2rem; animation: float 3s ease-in infinite; opacity: 0; }
        @keyframes float { 0% { opacity: 1; transform: translateY(100vh) scale(0); } 50% { opacity: 1; } 100% { opacity: 0; transform: translateY(-100vh) scale(1); } }
        
        /* NO MATCH MESSAGE */
        .no-match-msg { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: #1a1a2e; padding: 2rem 3rem; border-radius: 20px; text-align: center; z-index: 1500; display: none; border: 1px solid #444; }
        .no-match-msg h3 { color: #888; margin-bottom: 0.5rem; }
        .no-match-msg p { color: #666; font-size: 0.9rem; }
        
        /* GALLERY */
        .gallery { padding: 1rem; flex: 1; }
        .gallery h2 { margin-bottom: 1.5rem; font-size: 1.2rem; font-weight: 700; color: #ffffff; padding-left: 0.5rem; border-left: 3px solid #e91e63; }
        .girls-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 1rem; }
        .girl-card { background: #12121a; border-radius: 20px; overflow: hidden; cursor: pointer; transition: transform 0.2s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.2s ease; position: relative; border: 1px solid rgba(255, 255, 255, 0.05); will-change: transform; }
        .girl-card:hover { transform: translate3d(0, -5px, 0); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5); }
        .girl-card:active { transform: scale(0.97); }
        .girl-card-img { height: 240px; background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,0,0,0) 50%, rgba(10,10,12,0.9) 100%); position: relative; display: flex; align-items: center; justify-content: center; font-size: 3rem; font-weight: 700; color: rgba(233, 30, 99, 0.3); }
        .girl-card-info { position: absolute; bottom: 0; left: 0; right: 0; padding: 1rem; background: linear-gradient(to top, #12121a, transparent); }
        .girl-card-name { font-size: 1rem; font-weight: 700; color: #ffffff; }
        .girl-card-tagline { color: #888888; font-size: 0.75rem; margin-top: 0.2rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .badge-new { position: absolute; top: 10px; right: 10px; background: #e91e63; color: white; padding: 4px 8px; border-radius: 10px; font-size: 0.6rem; font-weight: 800; text-transform: uppercase; box-shadow: 0 2px 5px rgba(233, 30, 99, 0.4); z-index: 5; }
        
        /* PROFILE */
        .profile { max-width: 500px; margin: 0 auto; width: 100%; flex: 1; }
        .back-btn { color: #ffffff; font-size: 1.5rem; cursor: pointer; padding: 1rem; display: inline-block; transition: color 0.2s; }
        .back-btn:hover { color: #e91e63; }
        .profile-img { width: 100%; height: 450px; background: #12121a; display: flex; align-items: center; justify-content: center; font-size: 8rem; font-weight: 800; color: rgba(233, 30, 99, 0.1); position: relative; }
        .profile-img::after { content: ''; position: absolute; bottom: 0; left: 0; right: 0; height: 150px; background: linear-gradient(to top, #0a0a0c, transparent); }
        .profile-content { padding: 1.5rem; margin-top: -2rem; position: relative; z-index: 10; }
        .profile h1 { font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; }
        .profile-tagline { color: #e91e63; font-size: 0.9rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1.5rem; }
        .profile-stats { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
        .stat-item { background: #12121a; padding: 0.75rem 1.25rem; border-radius: 15px; border: 1px solid rgba(233, 30, 99, 0.2); flex: 1; text-align: center; }
        .stat-label { font-size: 0.7rem; color: #888888; text-transform: uppercase; margin-bottom: 0.3rem; }
        .stat-value { font-size: 1.1rem; font-weight: 700; color: #e91e63; }
        .profile-bio { color: #888888; line-height: 1.7; font-size: 0.95rem; margin-bottom: 2rem; }
        .profile-actions { display: flex; flex-direction: column; gap: 1rem; }
        .btn-premium { width: 100%; padding: 1.1rem; border: none; border-radius: 15px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), opacity 0.15s ease, box-shadow 0.15s ease; text-align: center; text-decoration: none; will-change: transform; }
        .btn-chat { background: #e91e63; color: #ffffff; box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3); }
        .btn-photo { background: #12121a; color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.1); }
        .btn-premium:active { transform: scale(0.96); }
        
        /* CHAT */
        .chat-page { display: none; height: 100vh; overflow: hidden; }
        .chat-header { display: flex; align-items: center; padding: 1rem; background: rgba(10, 10, 12, 0.9); backdrop-filter: blur(10px); border-bottom: 1px solid #1a1a1f; position: sticky; top: 0; z-index: 100; }
        .chat-avatar-circle { width: 42px; height: 42px; border-radius: 50%; background: #12121a; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: 800; color: #e91e63; margin-right: 0.75rem; border: 1px solid rgba(233, 30, 99, 0.3); }
        .chat-info { flex: 1; }
        .chat-name { font-weight: 700; font-size: 1.1rem; }
        .chat-status { font-size: 0.7rem; color: #888888; display: flex; align-items: center; gap: 4px; }
        .status-dot { width: 6px; height: 6px; background: #22c55e; border-radius: 50%; display: inline-block; box-shadow: 0 0 5px #22c55e; }
        
        .messages { flex: 1; overflow-y: auto; padding: 1.5rem 1rem; display: flex; flex-direction: column; gap: 1.2rem; scroll-behavior: smooth; }
        .msg { max-width: 80%; display: flex; flex-direction: column; }
        .msg.user { align-self: flex-end; }
        .msg.her { align-self: flex-start; }
        .msg-bubble { padding: 0.9rem 1.1rem; border-radius: 20px; font-size: 0.95rem; line-height: 1.5; position: relative; }
        .msg.her .msg-bubble { background: #12121a; border-bottom-left-radius: 4px; color: #ffffff; }
        .msg.user .msg-bubble { background: #e91e63; border-bottom-right-radius: 4px; color: #ffffff; }
        .msg-meta { font-size: 0.65rem; color: #555555; margin-top: 0.3rem; display: flex; align-items: center; gap: 4px; }
        .msg.user .msg-meta { align-self: flex-end; }
        .read-receipt { color: #e91e63; font-weight: 800; }
        
        .msg-img { max-width: 280px; border-radius: 18px; overflow: hidden; margin-top: 0.5rem; border: 1px solid rgba(255, 255, 255, 0.05); cursor: pointer; transition: opacity 0.2s; }
        .msg-img img { width: 100%; display: block; }
        .msg-img:active { opacity: 0.8; }
        
        .typing-indicator { font-size: 0.75rem; color: #e91e63; margin-bottom: 0.5rem; font-style: italic; display: none; }
        
        .input-area { padding: 1.2rem 1rem; background: #0a0a0c; border-top: 1px solid #1a1a1f; padding-bottom: calc(1.2rem + env(safe-area-inset-bottom)); }
        .input-row { display: flex; gap: 0.75rem; align-items: center; }
        .chat-input { flex: 1; padding: 1rem 1.5rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 30px; color: #ffffff; font-size: 1rem; outline: none; transition: border-color 0.2s; }
        .chat-input:focus { border-color: #e91e63; }
        .send-btn { width: 50px; height: 50px; border-radius: 50%; background: #e91e63; border: none; color: #ffffff; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(233, 30, 99, 0.3); transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), box-shadow 0.15s ease; will-change: transform; }
        .send-btn:active { transform: scale(0.85); box-shadow: 0 2px 5px rgba(233, 30, 99, 0.2); }
        .send-btn:disabled { opacity: 0.5; cursor: default; }
        
        .empty-chat { text-align: center; color: #444444; padding: 4rem 1rem; font-size: 0.9rem; letter-spacing: 1px; }

        /* Fullscreen Overlay */
        #img-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.95); z-index: 1000; display: none; align-items: center; justify-content: center; padding: 1rem; flex-direction: column; }
        #img-overlay img { max-width: 100%; max-height: 85%; border-radius: 10px; object-fit: contain; }
        .overlay-nav { display: flex; gap: 2rem; margin-top: 1rem; }
        .overlay-nav button { background: rgba(255,255,255,0.1); border: none; color: white; padding: 0.8rem 1.5rem; border-radius: 25px; font-size: 1rem; cursor: pointer; }
        .overlay-counter { color: #888; font-size: 0.8rem; margin-top: 0.5rem; }
        
        /* Profile Photo Gallery */
        .profile-gallery { margin: 1rem 0; }
        .profile-gallery h3 { font-size: 0.9rem; color: #888; margin-bottom: 0.75rem; text-transform: uppercase; letter-spacing: 1px; }
        .photo-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; }
        .photo-grid-item { aspect-ratio: 3/4; background: #12121a; border-radius: 12px; overflow: hidden; cursor: pointer; position: relative; border: 1px solid rgba(255,255,255,0.05); }
        .photo-grid-item img { width: 100%; height: 100%; object-fit: cover; }
        .photo-grid-item:hover { opacity: 0.9; }
        .photo-loading { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: #666; }
        .photo-loading .spinner { width: 30px; height: 30px; border: 3px solid #333; border-top-color: #e91e63; border-radius: 50%; animation: spin 1s linear infinite; margin-bottom: 0.5rem; }
        .photo-loading span { font-size: 0.7rem; }
        @keyframes spin { to { transform: rotate(360deg); } }
        
        /* Video Call Button */
        .btn-video { background: #1a1a2e; color: #888; border: 1px solid #333; margin-top: 0.5rem; }
        .btn-video:active { transform: none; }
        
        /* Toast Notification */
        .toast { position: fixed; bottom: 100px; left: 50%; transform: translateX(-50%); background: #1a1a2e; color: white; padding: 1rem 2rem; border-radius: 30px; z-index: 2000; display: none; border: 1px solid #e91e63; font-size: 0.9rem; }
        
        /* Stories */
        #storyOverlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 3000; display: none; flex-direction: column; }
        .story-progress { display: flex; gap: 4px; padding: 10px 15px; }
        .story-bar { flex: 1; height: 3px; background: rgba(255,255,255,0.3); border-radius: 2px; overflow: hidden; }
        .story-bar-fill { height: 100%; background: white; width: 0%; transition: width 0.1s linear; }
        .story-bar.done .story-bar-fill { width: 100%; }
        .story-content { flex: 1; display: flex; align-items: center; justify-content: center; position: relative; }
        .story-img { max-width: 100%; max-height: 100%; object-fit: contain; }
        .story-text { position: absolute; bottom: 80px; left: 0; right: 0; text-align: center; padding: 1rem; }
        .story-text span { background: rgba(0,0,0,0.7); color: white; padding: 0.5rem 1rem; border-radius: 10px; font-size: 1rem; }
        .story-close { position: absolute; top: 20px; right: 15px; background: none; border: none; color: white; font-size: 2rem; cursor: pointer; z-index: 10; }
        .story-nav { position: absolute; top: 0; bottom: 0; width: 30%; cursor: pointer; }
        .story-nav-left { left: 0; }
        .story-nav-right { right: 0; }
        .btn-stories { background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888); }
        
        /* BOTTOM NAVIGATION */
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; background: #0a0a0c; border-top: 1px solid #1a1a1f; display: flex; justify-content: space-around; padding: 0.5rem 0; padding-bottom: calc(0.5rem + env(safe-area-inset-bottom)); z-index: 500; backdrop-filter: blur(20px); }
        .nav-item { display: flex; flex-direction: column; align-items: center; padding: 0.5rem 1rem; cursor: pointer; transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), color 0.15s ease; border: none; background: none; will-change: transform; }
        .nav-item:active { transform: scale(0.85); }
        .nav-icon { font-size: 1.4rem; margin-bottom: 0.2rem; transition: color 0.15s ease, transform 0.15s ease; }
        .nav-item.active .nav-icon { transform: scale(1.1); }
        .nav-label { font-size: 0.65rem; color: #666; transition: color 0.15s ease; }
        .nav-item.active .nav-icon { color: #e91e63; }
        .nav-item.active .nav-label { color: #e91e63; }
        .nav-item:not(.active) .nav-icon { color: #666; }
        .nav-badge { position: absolute; top: 0; right: 0.5rem; background: #e91e63; color: white; font-size: 0.6rem; padding: 2px 5px; border-radius: 10px; font-weight: 700; }
        .page-with-nav { padding-bottom: 80px; }
        
        /* MESSAGES PAGE */
        .messages-list { padding: 1rem; }
        .message-item { display: flex; align-items: center; padding: 1rem; background: #12121a; border-radius: 15px; margin-bottom: 0.75rem; cursor: pointer; transition: transform 0.15s cubic-bezier(0.25, 0.46, 0.45, 0.94), background 0.15s ease; border: 1px solid rgba(255,255,255,0.03); will-change: transform; }
        .message-item:active { transform: scale(0.97); background: #1a1a2e; }
        .message-avatar { width: 55px; height: 55px; border-radius: 50%; background: #1a1a2e; display: flex; align-items: center; justify-content: center; font-size: 1.3rem; font-weight: 700; color: #e91e63; margin-right: 1rem; border: 2px solid rgba(233,30,99,0.3); flex-shrink: 0; }
        .message-info { flex: 1; min-width: 0; }
        .message-name { font-weight: 700; font-size: 1rem; margin-bottom: 0.2rem; }
        .message-preview { color: #888; font-size: 0.85rem; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .message-time { color: #666; font-size: 0.7rem; text-align: right; flex-shrink: 0; }
        .message-unread { width: 10px; height: 10px; background: #e91e63; border-radius: 50%; margin-left: 0.5rem; flex-shrink: 0; }
        .no-messages { text-align: center; color: #666; padding: 4rem 2rem; }
        
        /* RECEIVED PHOTOS GALLERY */
        .photos-gallery { padding: 1rem; }
        .photos-gallery h2 { margin-bottom: 1.5rem; font-size: 1.2rem; font-weight: 700; color: #ffffff; padding-left: 0.5rem; border-left: 3px solid #e91e63; }
        .gallery-section { margin-bottom: 2rem; }
        .gallery-section-title { font-size: 0.9rem; color: #888; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem; }
        .gallery-section-title::before { content: ''; width: 30px; height: 30px; border-radius: 50%; background: #12121a; display: flex; align-items: center; justify-content: center; }
        .photos-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; }
        .gallery-photo { aspect-ratio: 1; background: #12121a; border-radius: 4px; overflow: hidden; cursor: pointer; transition: opacity 0.2s; }
        .gallery-photo img { width: 100%; height: 100%; object-fit: cover; }
        .gallery-photo:active { opacity: 0.7; }
        .no-photos { text-align: center; color: #666; padding: 4rem 2rem; }
        
        /* USER PROFILE/SETTINGS PAGE */
        .settings-page { padding: 1.5rem; }
        .settings-header { text-align: center; margin-bottom: 2rem; }
        .settings-avatar { width: 100px; height: 100px; border-radius: 50%; background: linear-gradient(135deg, #e91e63, #9c27b0); margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; font-weight: 800; color: white; }
        .settings-name { font-size: 1.5rem; font-weight: 700; margin-bottom: 0.3rem; }
        .settings-age { color: #888; font-size: 0.9rem; }
        .settings-stats { display: flex; justify-content: center; gap: 2rem; margin: 1.5rem 0; padding: 1rem; background: #12121a; border-radius: 15px; }
        .settings-stat { text-align: center; }
        .settings-stat-value { font-size: 1.5rem; font-weight: 700; color: #e91e63; }
        .settings-stat-label { font-size: 0.75rem; color: #888; text-transform: uppercase; margin-top: 0.2rem; }
        .settings-section { margin-top: 1.5rem; }
        .settings-section-title { font-size: 0.8rem; color: #888; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.75rem; padding-left: 0.5rem; }
        .settings-item { display: flex; align-items: center; justify-content: space-between; padding: 1rem; background: #12121a; border-radius: 12px; margin-bottom: 0.5rem; cursor: pointer; transition: background 0.2s; }
        .settings-item:active { background: #1a1a2e; }
        .settings-item-left { display: flex; align-items: center; gap: 0.75rem; }
        .settings-item-icon { font-size: 1.2rem; }
        .settings-item-text { font-size: 0.95rem; }
        .settings-item-arrow { color: #666; }
        .btn-logout { width: 100%; padding: 1rem; background: transparent; border: 1px solid #ff4444; color: #ff4444; border-radius: 12px; font-size: 1rem; font-weight: 600; cursor: pointer; margin-top: 2rem; transition: all 0.2s; }
        .btn-logout:active { background: #ff4444; color: white; }
        .btn-reset { width: 100%; padding: 1rem; background: transparent; border: 1px solid #666; color: #666; border-radius: 12px; font-size: 0.9rem; cursor: pointer; margin-top: 0.5rem; }
        
        /* Loading Animation */
        @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
        .loading-shimmer { background: linear-gradient(90deg, #12121a 25%, #1a1a2e 50%, #12121a 75%); background-size: 200% 100%; animation: shimmer 1.2s ease-in-out infinite; }
        
        @keyframes typing { 0%, 60%, 100% { transform: translateY(0); } 30% { transform: translateY(-5px); } }
        .typing-indicator { display: flex; gap: 4px; padding: 0.5rem 1rem; }
        .typing-dot { width: 8px; height: 8px; background: #e91e63; border-radius: 50%; animation: typing 1.2s ease-in-out infinite; }
        .typing-dot:nth-child(2) { animation-delay: 0.2s; }
        .typing-dot:nth-child(3) { animation-delay: 0.4s; }
        
        .swipe-card { animation: scaleIn 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94); }
        .match-overlay-content { animation: bounceIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55); }
        
        /* PWA INSTALL BANNER */
        .install-banner { position: fixed; bottom: 80px; left: 1rem; right: 1rem; background: linear-gradient(135deg, #e91e63, #9c27b0); padding: 1rem 1.5rem; border-radius: 15px; display: none; align-items: center; justify-content: space-between; z-index: 1000; box-shadow: 0 5px 20px rgba(233,30,99,0.4); animation: slideUp 0.3s ease; }
        .install-banner-text { color: white; font-weight: 600; }
        .install-banner-btn { background: white; color: #e91e63; border: none; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 700; cursor: pointer; }
        .install-banner-close { background: none; border: none; color: rgba(255,255,255,0.7); font-size: 1.2rem; cursor: pointer; margin-left: 0.5rem; }
        
        /* FILTER BUTTONS */
        .filter-section { padding: 0.5rem 1rem; background: #0a0a0c; border-bottom: 1px solid #1a1a1f; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        .filter-row { display: flex; gap: 0.5rem; margin-bottom: 0.5rem; }
        .filter-btn { padding: 0.4rem 0.8rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 20px; color: #888; font-size: 0.75rem; cursor: pointer; flex-shrink: 0; transition: all 0.15s ease; }
        .filter-btn.active { background: #e91e63; color: white; border-color: #e91e63; }
        .filter-btn:active { transform: scale(0.95); }
        
        /* NOTIFICATION BADGE */
        .nav-badge { position: absolute; top: 2px; right: 50%; transform: translateX(100%); background: #e91e63; color: white; font-size: 0.6rem; min-width: 16px; height: 16px; padding: 0 4px; border-radius: 10px; font-weight: 700; display: none; align-items: center; justify-content: center; }
        .nav-badge.show { display: flex; }
        
        /* ICEBREAKERS */
        .icebreakers { display: flex; gap: 0.5rem; padding: 0.5rem 1rem; overflow-x: auto; -webkit-overflow-scrolling: touch; }
        .icebreaker-btn { flex-shrink: 0; padding: 0.5rem 1rem; background: #12121a; border: 1px solid rgba(233,30,99,0.3); border-radius: 20px; color: #e91e63; font-size: 0.8rem; cursor: pointer; transition: all 0.15s ease; }
        .icebreaker-btn:active { transform: scale(0.95); background: #e91e63; color: white; }
        
        /* CHAT MENU */
        .chat-menu-btn { margin-left: auto; background: none; border: none; color: #888; font-size: 1.5rem; cursor: pointer; padding: 0.5rem; }
        .chat-menu { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.8); z-index: 2500; display: none; align-items: flex-end; justify-content: center; }
        .chat-menu.show { display: flex; }
        .chat-menu-content { background: #12121a; width: 100%; max-width: 400px; border-radius: 20px 20px 0 0; padding: 1rem; animation: slideUp 0.2s ease; }
        .chat-menu-option { padding: 1rem; text-align: center; font-size: 1rem; cursor: pointer; border-radius: 10px; margin-bottom: 0.5rem; transition: background 0.15s ease; }
        .chat-menu-option:active { background: #1a1a2e; }
        .chat-menu-option.danger { color: #ff4444; }
        .chat-menu-cancel { padding: 1rem; text-align: center; background: #1a1a2e; border-radius: 10px; color: #888; cursor: pointer; margin-top: 0.5rem; }
        
        /* CONFIRMATION POPUP */
        .confirm-popup { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.9); z-index: 3000; display: none; align-items: center; justify-content: center; padding: 2rem; }
        .confirm-popup.show { display: flex; }
        .confirm-content { background: #12121a; border-radius: 20px; padding: 2rem; text-align: center; max-width: 300px; animation: scaleIn 0.2s ease; }
        .confirm-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 0.5rem; }
        .confirm-text { color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; }
        .confirm-buttons { display: flex; gap: 1rem; }
        .confirm-btn { flex: 1; padding: 0.8rem; border: none; border-radius: 10px; font-weight: 600; cursor: pointer; }
        .confirm-btn-cancel { background: #1a1a2e; color: #888; }
        .confirm-btn-confirm { background: #ff4444; color: white; }
        
        /* PREMIUM POPUP */
        .premium-popup { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.95); z-index: 3000; display: none; align-items: center; justify-content: center; padding: 2rem; }
        .premium-popup.show { display: flex; }
        .premium-content { background: linear-gradient(135deg, #1a1a2e, #12121a); border: 2px solid #e91e63; border-radius: 25px; padding: 2rem; text-align: center; max-width: 320px; animation: bounceIn 0.4s ease; }
        .premium-crown { font-size: 4rem; margin-bottom: 1rem; }
        .premium-title { font-size: 1.5rem; font-weight: 800; color: #e91e63; margin-bottom: 0.5rem; }
        .premium-features { text-align: left; margin: 1.5rem 0; }
        .premium-feature { display: flex; align-items: center; gap: 0.75rem; padding: 0.5rem 0; color: #ccc; font-size: 0.9rem; }
        .premium-feature::before { content: '✓'; color: #e91e63; font-weight: 700; }
        .premium-price { font-size: 2rem; font-weight: 800; color: white; margin: 1rem 0; }
        .premium-price span { font-size: 1rem; color: #888; }
        .premium-btn { width: 100%; padding: 1rem; background: #e91e63; border: none; border-radius: 15px; color: white; font-size: 1rem; font-weight: 700; cursor: pointer; margin-top: 0.5rem; }
        .premium-close { margin-top: 1rem; background: none; border: none; color: #666; cursor: pointer; }
        
        /* SUPER LIKE BUTTON */
        .swipe-btn-super { background: #00bcd4; color: white; width: 55px; height: 55px; font-size: 1.5rem; }
        .swipe-btn-boost { background: #9c27b0; color: white; width: 55px; height: 55px; font-size: 1.3rem; }
        
        /* EDIT PROFILE */
        .edit-profile-section { margin-bottom: 1.5rem; }
        .edit-label { font-size: 0.8rem; color: #888; margin-bottom: 0.5rem; text-transform: uppercase; }
        .edit-input { width: 100%; padding: 1rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 12px; color: white; font-size: 1rem; outline: none; margin-bottom: 1rem; }
        .edit-input:focus { border-color: #e91e63; }
        .edit-textarea { min-height: 100px; resize: vertical; }
        .age-slider-container { padding: 1rem 0; }
        .age-slider { width: 100%; -webkit-appearance: none; height: 4px; background: #1a1a1f; border-radius: 2px; outline: none; }
        .age-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 20px; height: 20px; background: #e91e63; border-radius: 50%; cursor: pointer; }
        .age-range-display { display: flex; justify-content: space-between; color: #888; font-size: 0.8rem; margin-top: 0.5rem; }
        
        /* THEME TOGGLE */
        .theme-toggle { display: flex; align-items: center; gap: 1rem; padding: 1rem; background: #12121a; border-radius: 12px; margin-bottom: 0.5rem; }
        .toggle-switch { width: 50px; height: 26px; background: #1a1a1f; border-radius: 13px; position: relative; cursor: pointer; transition: background 0.2s; }
        .toggle-switch.active { background: #e91e63; }
        .toggle-switch::after { content: ''; position: absolute; top: 3px; left: 3px; width: 20px; height: 20px; background: white; border-radius: 50%; transition: transform 0.2s; }
        .toggle-switch.active::after { transform: translateX(24px); }
        
        /* LIGHT THEME */
        body.light-theme { background: #f5f5f5; color: #1a1a1a; }
        body.light-theme .page { background: #f5f5f5; }
        body.light-theme .header { background: rgba(255,255,255,0.9); border-color: #e0e0e0; }
        body.light-theme .logo { color: #e91e63; }
        body.light-theme .swipe-card { background: white; box-shadow: 0 5px 20px rgba(0,0,0,0.1); }
        body.light-theme .swipe-card-img { background: #f0f0f5; }
        body.light-theme .girl-card { background: white; border-color: #e0e0e0; }
        body.light-theme .bottom-nav { background: white; border-color: #e0e0e0; }
        body.light-theme .nav-item:not(.active) .nav-icon { color: #666; }
        body.light-theme .message-item { background: white; border-color: #e0e0e0; }
        body.light-theme .settings-page { background: #f5f5f5; }
        body.light-theme .settings-stats { background: white; }
        body.light-theme .settings-item { background: white; }
        body.light-theme .chat-input { background: white; border-color: #e0e0e0; color: #1a1a1a; }
        body.light-theme .msg-received { background: #e0e0e0; color: #1a1a1a; }
        body.light-theme .chat-header { background: rgba(255,255,255,0.9); border-color: #e0e0e0; }
        body.light-theme .filter-btn { background: white; border-color: #e0e0e0; color: #666; }
        body.light-theme .icebreaker-btn { background: white; }
        body.light-theme .edit-input { background: white; border-color: #e0e0e0; color: #1a1a1a; }
        body.light-theme .login-input { background: white; border-color: #e0e0e0; color: #1a1a1a; }
    </style>
</head>
<body>

<!-- LOGIN PAGE -->
<div class="page login-page active" id="pageLogin">
    <div class="login-box">
        <div class="login-logo">DREAM AI</div>
        <div class="login-subtitle">Trouve ta partenaire virtuelle</div>
        <div class="login-form">
            <input type="text" class="login-input" id="userName" placeholder="Ton prénom" required>
            <input type="number" class="login-input" id="userAge" placeholder="Ton âge" min="18" max="99" required>
            <button class="login-btn" onclick="login()">Commencer</button>
        </div>
    </div>
</div>

<!-- DISCOVER PAGE (Swipe) -->
<div class="page page-with-nav" id="pageDiscover">
    <div class="header">
        <div class="header-row">
            <div class="logo">DREAM AI</div>
            <div class="user-name" id="headerUserName"></div>
        </div>
    </div>
    
    <div class="filter-section">
        <div class="filter-row">
            <button class="filter-btn active" onclick="setAgeFilter('all')" id="filterAgeAll">Tous</button>
            <button class="filter-btn" onclick="setAgeFilter('18-25')" id="filterAge1825">18-25</button>
            <button class="filter-btn" onclick="setAgeFilter('25-35')" id="filterAge2535">25-35</button>
            <button class="filter-btn" onclick="setAgeFilter('35-45')" id="filterAge3545">35-45</button>
            <button class="filter-btn" onclick="setAgeFilter('45+')" id="filterAge45">45+</button>
        </div>
        <div class="filter-row">
            <button class="filter-btn active" onclick="setRegionFilter('all')" id="filterRegionAll">Tous</button>
            <button class="filter-btn" onclick="setRegionFilter('europe')" id="filterEurope">Europe</button>
            <button class="filter-btn" onclick="setRegionFilter('asie')" id="filterAsie">Asie</button>
            <button class="filter-btn" onclick="setRegionFilter('afrique')" id="filterAfrique">Afrique</button>
            <button class="filter-btn" onclick="setRegionFilter('amerique')" id="filterAmerique">Amerique</button>
        </div>
    </div>
    
    <div class="swipe-container">
        <div class="swipe-card" id="swipeCard">
            <div class="swipe-card-img" id="swipeCardImg"></div>
            <div class="swipe-card-info">
                <div class="swipe-card-name" id="swipeCardName"></div>
                <div class="swipe-card-location" id="swipeCardLocation"></div>
                <div class="swipe-card-bio" id="swipeCardBio"></div>
            </div>
        </div>
        <div class="no-more-cards" id="noMoreCards" style="display:none;">
            <p>Plus de profils pour le moment</p>
            <p style="color:#666;font-size:0.8rem;margin-top:0.5rem;">Reviens plus tard</p>
        </div>
    </div>
    <div class="swipe-buttons" id="swipeButtons">
        <button class="swipe-btn swipe-btn-pass" onclick="swipeLeft()">X</button>
        <button class="swipe-btn swipe-btn-super" onclick="showPremiumPopup()">★</button>
        <button class="swipe-btn swipe-btn-like" onclick="swipeRight()">♥</button>
        <button class="swipe-btn swipe-btn-boost" onclick="showPremiumPopup()">⚡</button>
    </div>
</div>

<!-- MESSAGES PAGE -->
<div class="page page-with-nav" id="pageMessages">
    <div class="header">
        <div class="logo">Messages</div>
    </div>
    <div class="messages-list" id="messagesList"></div>
    <div class="no-messages" id="noMessagesText" style="display:none;">
        <p style="font-size:3rem;margin-bottom:1rem;">💬</p>
        <p>Pas encore de conversations</p>
        <p style="font-size:0.85rem;margin-top:0.5rem;color:#888;">Match avec quelqu'un pour commencer</p>
    </div>
</div>

<!-- MATCHES PAGE -->
<div class="page page-with-nav" id="pageMatches">
    <div class="header">
        <div class="logo">Matchs</div>
    </div>
    <div class="gallery">
        <h2>Tes Matchs</h2>
        <div class="girls-grid" id="matchesGrid"></div>
        <div id="noMatches" style="text-align:center;color:#666;padding:3rem;display:none;">
            <p style="font-size:3rem;margin-bottom:1rem;">💕</p>
            <p>Pas encore de matchs</p>
            <p style="font-size:0.8rem;margin-top:0.5rem;">Continue a swiper pour en trouver</p>
        </div>
    </div>
</div>

<!-- GALLERY PAGE (Received Photos) -->
<div class="page page-with-nav" id="pageGallery">
    <div class="header">
        <div class="logo">Galerie</div>
    </div>
    <div class="photos-gallery" id="photosGallery"></div>
    <div class="no-photos" id="noPhotosText" style="display:none;">
        <p style="font-size:3rem;margin-bottom:1rem;">📸</p>
        <p>Aucune photo recue</p>
        <p style="font-size:0.85rem;margin-top:0.5rem;color:#888;">Discute avec tes matchs pour en recevoir</p>
    </div>
</div>

<!-- SETTINGS PAGE -->
<div class="page page-with-nav" id="pageSettings">
    <div class="settings-page">
        <div class="settings-header">
            <div class="settings-avatar" id="settingsAvatar"></div>
            <div class="settings-name" id="settingsName"></div>
            <div class="settings-age" id="settingsAge"></div>
        </div>
        <div class="settings-stats">
            <div class="settings-stat">
                <div class="settings-stat-value" id="statsMatches">0</div>
                <div class="settings-stat-label">Matchs</div>
            </div>
            <div class="settings-stat">
                <div class="settings-stat-value" id="statsPhotos">0</div>
                <div class="settings-stat-label">Photos</div>
            </div>
            <div class="settings-stat">
                <div class="settings-stat-value" id="statsChats">0</div>
                <div class="settings-stat-label">Chats</div>
            </div>
        </div>
        <div class="settings-section">
            <div class="settings-section-title">Apparence</div>
            <div class="theme-toggle">
                <div class="settings-item-left">
                    <span class="settings-item-icon">🌙</span>
                    <span class="settings-item-text">Mode Sombre</span>
                </div>
                <div class="toggle-switch active" id="themeToggle" onclick="toggleTheme()"></div>
            </div>
        </div>
        <div class="settings-section">
            <div class="settings-section-title">Preferences</div>
            <div class="settings-item" onclick="showPremiumPopup()">
                <div class="settings-item-left">
                    <span class="settings-item-icon">👑</span>
                    <span class="settings-item-text">Dream AI Premium</span>
                </div>
                <span class="settings-item-arrow">→</span>
            </div>
            <div class="settings-item" onclick="showPremiumPopup()">
                <div class="settings-item-left">
                    <span class="settings-item-icon">👀</span>
                    <span class="settings-item-text">Voir qui t'a like</span>
                </div>
                <span class="settings-item-arrow">🔒</span>
            </div>
            <div class="settings-item" onclick="showVideoToast()">
                <div class="settings-item-left">
                    <span class="settings-item-icon">🔔</span>
                    <span class="settings-item-text">Notifications</span>
                </div>
                <span class="settings-item-arrow">→</span>
            </div>
            <div class="settings-item" onclick="showVideoToast()">
                <div class="settings-item-left">
                    <span class="settings-item-icon">🔒</span>
                    <span class="settings-item-text">Confidentialite</span>
                </div>
                <span class="settings-item-arrow">→</span>
            </div>
        </div>
        <button class="btn-reset" onclick="resetAllData()">Reinitialiser les donnees</button>
        <button class="btn-logout" onclick="logout()">Se deconnecter</button>
    </div>
</div>

<!-- BOTTOM NAVIGATION -->
<nav class="bottom-nav" id="bottomNav" style="display:none;">
    <button class="nav-item active" onclick="navigateTo('discover')" id="navDiscover">
        <span class="nav-icon">🔥</span>
        <span class="nav-label">Decouvrir</span>
    </button>
    <button class="nav-item" onclick="navigateTo('messages')" id="navMessages" style="position:relative;">
        <span class="nav-icon">💬</span>
        <span class="nav-label">Messages</span>
        <span class="nav-badge" id="msgBadge">0</span>
    </button>
    <button class="nav-item" onclick="navigateTo('matches')" id="navMatches">
        <span class="nav-icon">💕</span>
        <span class="nav-label">Matchs</span>
    </button>
    <button class="nav-item" onclick="navigateTo('gallery')" id="navGallery">
        <span class="nav-icon">📸</span>
        <span class="nav-label">Galerie</span>
    </button>
    <button class="nav-item" onclick="navigateTo('settings')" id="navSettings">
        <span class="nav-icon">👤</span>
        <span class="nav-label">Profil</span>
    </button>
</nav>

<!-- PROFILE PAGE -->
<div class="page" id="pageProfile">
    <div class="profile">
        <div class="back-btn" onclick="goBackFromProfile()">←</div>
        <div class="profile-img" id="profileMainPhoto"></div>
        <div class="profile-content">
            <h1 id="profileName"></h1>
            <div class="profile-tagline" id="profileTagline"></div>
            
            <div class="profile-stats">
                <div class="stat-item">
                    <div class="stat-label">Affection</div>
                    <div class="stat-value" id="profileAffection">20%</div>
                </div>
                <div class="stat-item">
                    <div class="stat-label">Statut</div>
                    <div class="stat-value" style="color:#22c55e">Online</div>
                </div>
            </div>
            
            <div class="profile-gallery">
                <h3>Photos</h3>
                <div class="photo-grid" id="profilePhotoGrid"></div>
            </div>
            
            <div class="profile-bio" id="profileBio"></div>
            
            <div class="profile-actions">
                <button class="btn-premium btn-chat" onclick="startChat()">Envoyer un Message</button>
                <button class="btn-premium btn-photo" onclick="requestProfilePhoto()">Demander une Photo</button>
                <button class="btn-premium btn-stories" onclick="openStories()">Voir sa Story</button>
                <button class="btn-premium btn-video" onclick="showVideoToast()">Appel Vidéo</button>
            </div>
        </div>
    </div>
</div>

<div class="toast" id="toast">Bientôt disponible</div>

<!-- CHAT PAGE -->
<div class="page chat-page" id="pageChat">
    <div class="chat-header">
        <div class="back-btn" onclick="goBackFromChat()">←</div>
        <div class="chat-avatar-circle" id="chatInitials"></div>
        <div class="chat-info">
            <div class="chat-name" id="chatName"></div>
            <div class="chat-status"><span class="status-dot"></span> Online</div>
        </div>
        <button class="chat-menu-btn" onclick="openChatMenu()">⋮</button>
    </div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <div id="typing-indicator" class="typing-indicator"></div>
        <div class="icebreakers" id="icebreakers">
            <button class="icebreaker-btn" onclick="sendIcebreaker('Hey ca va?')">Hey ca va?</button>
            <button class="icebreaker-btn" onclick="sendIcebreaker('T es vraiment canon')">T es vraiment canon</button>
            <button class="icebreaker-btn" onclick="sendIcebreaker('On discute?')">On discute?</button>
        </div>
        <div class="input-row">
            <input type="text" class="chat-input" id="chatInput" placeholder="Écris un message...">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
        </div>
    </div>
</div>

<!-- CHAT MENU -->
<div class="chat-menu" id="chatMenu" onclick="closeChatMenu()">
    <div class="chat-menu-content" onclick="event.stopPropagation()">
        <div class="chat-menu-option" onclick="showConfirmPopup('unmatch')">Unmatch</div>
        <div class="chat-menu-option danger" onclick="showConfirmPopup('block')">Bloquer</div>
        <div class="chat-menu-option danger" onclick="showConfirmPopup('report')">Signaler</div>
        <div class="chat-menu-cancel" onclick="closeChatMenu()">Annuler</div>
    </div>
</div>

<!-- CONFIRM POPUP -->
<div class="confirm-popup" id="confirmPopup">
    <div class="confirm-content">
        <div class="confirm-title" id="confirmTitle">Confirmer</div>
        <div class="confirm-text" id="confirmText">Es-tu sur?</div>
        <div class="confirm-buttons">
            <button class="confirm-btn confirm-btn-cancel" onclick="closeConfirmPopup()">Annuler</button>
            <button class="confirm-btn confirm-btn-confirm" id="confirmBtn" onclick="confirmAction()">Confirmer</button>
        </div>
    </div>
</div>

<!-- PREMIUM POPUP -->
<div class="premium-popup" id="premiumPopup">
    <div class="premium-content">
        <div class="premium-crown">👑</div>
        <div class="premium-title">Dream AI Premium</div>
        <div class="premium-features">
            <div class="premium-feature">Super Likes illimites</div>
            <div class="premium-feature">Voir qui t'a like</div>
            <div class="premium-feature">Boost de visibilite</div>
            <div class="premium-feature">Photos exclusives</div>
            <div class="premium-feature">Messages prioritaires</div>
        </div>
        <div class="premium-price">9.99EUR <span>/mois</span></div>
        <button class="premium-btn" onclick="closePremiumPopup()">Debloquer Premium</button>
        <button class="premium-close" onclick="closePremiumPopup()">Plus tard</button>
    </div>
</div>

<!-- INSTALL BANNER -->
<div class="install-banner" id="installBanner">
    <span class="install-banner-text">Installer l'app</span>
    <div>
        <button class="install-banner-btn" onclick="installPWA()">Installer</button>
        <button class="install-banner-close" onclick="hideInstallBanner()">×</button>
    </div>
</div>

<div id="img-overlay">
    <img id="overlay-img" src="">
    <div class="overlay-counter" id="overlay-counter">1 / 4</div>
    <div class="overlay-nav">
        <button onclick="prevOverlayImg()">Précédent</button>
        <button onclick="document.getElementById('img-overlay').style.display='none'">Fermer</button>
        <button onclick="nextOverlayImg()">Suivant</button>
    </div>
</div>

<!-- MATCH OVERLAY -->
<div id="matchOverlay">
    <div class="hearts" id="hearts"></div>
    <div class="match-title">C'est un Match!</div>
    <div class="match-photos">
        <div class="match-photo" id="matchPhotoUser">?</div>
        <div class="match-photo" id="matchPhotoGirl"></div>
    </div>
    <div class="match-names" id="matchNames"></div>
    <button class="match-btn" onclick="goToMatchChat()">Envoyer un message</button>
    <button class="match-close" onclick="closeMatch()">Continuer à swiper</button>
</div>

<!-- NO MATCH MESSAGE -->
<div class="no-match-msg" id="noMatchMsg">
    <h3>Elle n'a pas matché avec toi</h3>
    <p>Passe au profil suivant</p>
</div>

<!-- STORIES OVERLAY -->
<div id="storyOverlay">
    <div class="story-progress" id="storyProgress"></div>
    <button class="story-close" onclick="closeStories()">X</button>
    <div class="story-content">
        <div class="story-nav story-nav-left" onclick="prevStory()"></div>
        <img class="story-img" id="storyImg" src="">
        <div class="story-nav story-nav-right" onclick="nextStory()"></div>
        <div class="story-text"><span id="storyText"></span></div>
    </div>
</div>

<script>
const GIRLS = ''' + json.dumps(GIRLS, ensure_ascii=False) + ''';
const INITIALS = {};
Object.keys(GIRLS).forEach(id => { INITIALS[id] = GIRLS[id].name.charAt(0).toUpperCase(); });

const REGION_MAP = {
    'europe': ['France', 'Germany', 'Sweden', 'Italy', 'Ukraine', 'Russia', 'Belarus', 'Belgium', 'UK', 'Spain'],
    'asie': ['Japan', 'China', 'Korea', 'Thailand', 'India', 'Vietnam', 'Philippines', 'Indonesia'],
    'afrique': ['Nigeria', 'Ghana', 'Senegal', 'Morocco', 'Egypt', 'South Africa', 'Kenya'],
    'amerique': ['USA', 'Texas', 'California', 'LA', 'Vegas', 'Brazil', 'Mexico', 'Argentina', 'Colombia', 'Canada']
};

let currentGirl = null;
let chatHistory = {};
let affectionLevels = JSON.parse(localStorage.getItem('affectionLevels') || '{}');
let profilePhotos = JSON.parse(localStorage.getItem('profilePhotos') || '{}');
let receivedPhotos = JSON.parse(localStorage.getItem('receivedPhotos') || '{}');
let currentOverlayPhotos = [];
let currentOverlayIndex = 0;

let user = JSON.parse(localStorage.getItem('dreamUser') || 'null');
let matches = JSON.parse(localStorage.getItem('dreamMatches') || '[]');
let passed = JSON.parse(localStorage.getItem('dreamPassed') || '[]');
let blocked = JSON.parse(localStorage.getItem('dreamBlocked') || '[]');
let swipeQueue = [];
let currentSwipeGirl = null;

let currentAgeFilter = 'all';
let currentRegionFilter = 'all';
let unreadMessages = JSON.parse(localStorage.getItem('unreadMessages') || '{}');
let pendingConfirmAction = null;
let deferredPrompt = null;
let darkMode = localStorage.getItem('darkMode') !== 'false';

let audioContext = null;

function initAudio() {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
    }
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
}

document.addEventListener('click', initAudio, { once: true });
document.addEventListener('touchstart', initAudio, { once: true });

function playSound(type) {
    if (!audioContext) return;
    try {
        const osc = audioContext.createOscillator();
        const gain = audioContext.createGain();
        osc.connect(gain);
        gain.connect(audioContext.destination);
        
        if (type === 'match') {
            osc.frequency.setValueAtTime(523.25, audioContext.currentTime);
            osc.frequency.setValueAtTime(659.25, audioContext.currentTime + 0.1);
            osc.frequency.setValueAtTime(783.99, audioContext.currentTime + 0.2);
            gain.gain.setValueAtTime(0.3, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.4);
            osc.start(); osc.stop(audioContext.currentTime + 0.4);
        } else if (type === 'message') {
            osc.frequency.setValueAtTime(880, audioContext.currentTime);
            osc.frequency.setValueAtTime(1046.5, audioContext.currentTime + 0.05);
            gain.gain.setValueAtTime(0.2, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.15);
            osc.start(); osc.stop(audioContext.currentTime + 0.15);
        } else if (type === 'send') {
            osc.type = 'sine';
            osc.frequency.setValueAtTime(600, audioContext.currentTime);
            osc.frequency.exponentialRampToValueAtTime(1200, audioContext.currentTime + 0.1);
            gain.gain.setValueAtTime(0.15, audioContext.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.01, audioContext.currentTime + 0.1);
            osc.start(); osc.stop(audioContext.currentTime + 0.1);
        }
    } catch(e) { console.log('Sound error:', e); }
}

function applyTheme() {
    if (darkMode) {
        document.body.classList.remove('light-theme');
    } else {
        document.body.classList.add('light-theme');
    }
    const toggle = document.getElementById('themeToggle');
    if (toggle) toggle.classList.toggle('active', darkMode);
}

function toggleTheme() {
    darkMode = !darkMode;
    localStorage.setItem('darkMode', darkMode);
    applyTheme();
}

if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js').catch(err => console.log('SW error:', err));
}

window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (!localStorage.getItem('pwaInstallDismissed')) {
        document.getElementById('installBanner').style.display = 'flex';
    }
});

function installPWA() {
    if (deferredPrompt) {
        deferredPrompt.prompt();
        deferredPrompt.userChoice.then(result => {
            deferredPrompt = null;
            hideInstallBanner();
        });
    }
}

function hideInstallBanner() {
    document.getElementById('installBanner').style.display = 'none';
    localStorage.setItem('pwaInstallDismissed', 'true');
}

function setAgeFilter(filter) {
    currentAgeFilter = filter;
    document.querySelectorAll('.filter-row:first-child .filter-btn').forEach(btn => btn.classList.remove('active'));
    if (filter === 'all') document.getElementById('filterAgeAll').classList.add('active');
    else if (filter === '18-25') document.getElementById('filterAge1825').classList.add('active');
    else if (filter === '25-35') document.getElementById('filterAge2535').classList.add('active');
    else if (filter === '35-45') document.getElementById('filterAge3545').classList.add('active');
    else if (filter === '45+') document.getElementById('filterAge45').classList.add('active');
    initSwipe();
}

function setRegionFilter(filter) {
    currentRegionFilter = filter;
    document.querySelectorAll('.filter-row:last-child .filter-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('filterRegion' + (filter === 'all' ? 'All' : filter.charAt(0).toUpperCase() + filter.slice(1))).classList.add('active');
    initSwipe();
}

function matchesAgeFilter(girl) {
    if (currentAgeFilter === 'all') return true;
    const age = girl.age;
    if (currentAgeFilter === '18-25') return age >= 18 && age <= 25;
    if (currentAgeFilter === '25-35') return age > 25 && age <= 35;
    if (currentAgeFilter === '35-45') return age > 35 && age <= 45;
    if (currentAgeFilter === '45+') return age > 45;
    return true;
}

function matchesRegionFilter(girl) {
    if (currentRegionFilter === 'all') return true;
    const loc = girl.location || '';
    const regions = REGION_MAP[currentRegionFilter] || [];
    return regions.some(r => loc.toLowerCase().includes(r.toLowerCase()));
}

function updateMessageBadge() {
    let count = Object.values(unreadMessages).reduce((a, b) => a + b, 0);
    const badge = document.getElementById('msgBadge');
    if (count > 0) {
        badge.textContent = count > 9 ? '9+' : count;
        badge.classList.add('show');
    } else {
        badge.classList.remove('show');
    }
}

function addUnreadMessage(girlId) {
    unreadMessages[girlId] = (unreadMessages[girlId] || 0) + 1;
    localStorage.setItem('unreadMessages', JSON.stringify(unreadMessages));
    updateMessageBadge();
}

function clearUnreadMessages(girlId) {
    delete unreadMessages[girlId];
    localStorage.setItem('unreadMessages', JSON.stringify(unreadMessages));
    updateMessageBadge();
}

function openChatMenu() {
    document.getElementById('chatMenu').classList.add('show');
}

function closeChatMenu() {
    document.getElementById('chatMenu').classList.remove('show');
}

function showConfirmPopup(action) {
    closeChatMenu();
    pendingConfirmAction = action;
    const titles = { unmatch: 'Unmatch', block: 'Bloquer', report: 'Signaler' };
    const texts = {
        unmatch: 'Tu ne pourras plus lui parler. Continuer?',
        block: 'Elle ne pourra plus te contacter. Continuer?',
        report: 'Signaler ce profil pour comportement inapproprie?'
    };
    document.getElementById('confirmTitle').textContent = titles[action];
    document.getElementById('confirmText').textContent = texts[action];
    document.getElementById('confirmPopup').classList.add('show');
}

function closeConfirmPopup() {
    document.getElementById('confirmPopup').classList.remove('show');
    pendingConfirmAction = null;
}

function confirmAction() {
    if (!pendingConfirmAction || !currentGirl) return;
    
    if (pendingConfirmAction === 'unmatch' || pendingConfirmAction === 'block') {
        matches = matches.filter(id => id !== currentGirl);
        localStorage.setItem('dreamMatches', JSON.stringify(matches));
        delete chatHistory[currentGirl];
        localStorage.removeItem('chat_' + currentGirl);
        
        if (pendingConfirmAction === 'block') {
            blocked.push(currentGirl);
            localStorage.setItem('dreamBlocked', JSON.stringify(blocked));
        }
        
        showToast(pendingConfirmAction === 'block' ? 'Profil bloque' : 'Unmatch effectue');
        closeConfirmPopup();
        navigateTo('matches');
    } else if (pendingConfirmAction === 'report') {
        showToast('Merci pour ton signalement');
        closeConfirmPopup();
    }
}

function showPremiumPopup() {
    document.getElementById('premiumPopup').classList.add('show');
}

function closePremiumPopup() {
    document.getElementById('premiumPopup').classList.remove('show');
}

function sendIcebreaker(text) {
    document.getElementById('chatInput').value = text;
    sendMessage();
    document.getElementById('icebreakers').style.display = 'none';
}

function girlMessagesFirst(girlId) {
    if (Math.random() < 0.3) {
        const g = GIRLS[girlId];
        const greetings = [
            "Hey! Tu me plais bien toi",
            "Salut beau gosse",
            "Coucou! J'ai vu qu'on a matche",
            "Hey toi! Ca va?",
            "Mmm t'es mignon, on discute?"
        ];
        const msg = greetings[Math.floor(Math.random() * greetings.length)];
        
        setTimeout(() => {
            if (!chatHistory[girlId]) chatHistory[girlId] = [];
            const time = new Date().toLocaleTimeString('fr-FR', {hour: '2-digit', minute:'2-digit'});
            chatHistory[girlId].push({ role: 'assistant', content: msg, time });
            saveChatHistory(girlId);
            addUnreadMessage(girlId);
            playSound('message');
        }, 3000 + Math.random() * 5000);
    }
}

function loadChatHistory(girlId) {
    const saved = localStorage.getItem('chat_' + girlId);
    if (saved) {
        try { return JSON.parse(saved); } catch(e) { return []; }
    }
    return [];
}

function saveChatHistory(girlId) {
    localStorage.setItem('chat_' + girlId, JSON.stringify(chatHistory[girlId] || []));
}

function saveReceivedPhoto(girlId, photoUrl) {
    if (!receivedPhotos[girlId]) receivedPhotos[girlId] = [];
    if (!receivedPhotos[girlId].includes(photoUrl)) {
        receivedPhotos[girlId].push(photoUrl);
        localStorage.setItem('receivedPhotos', JSON.stringify(receivedPhotos));
    }
}

const PHOTO_BACKGROUNDS = {
    day: ["beach sunny day", "city street daytime", "park bench", "cafe terrace outdoor", "gym workout area", "office desk"],
    night: ["club dance floor neon lights", "bar with cocktails", "fancy restaurant candlelight", "bedroom dim lights"],
    home: ["living room couch", "kitchen counter", "bathroom mirror selfie", "messy bedroom"],
    outdoor: ["nature hiking trail", "mountain scenic view", "swimming pool lounger", "garden flowers"]
};

function getRandomBg(category) {
    const bgs = PHOTO_BACKGROUNDS[category];
    return bgs[Math.floor(Math.random() * bgs.length)];
}

const PHOTO_TYPES = [
    { type: 'casual', getPrompt: (aff) => `casual everyday outfit, jeans and t-shirt or comfortable clothes, natural relaxed pose, ${getRandomBg('day')}, authentic candid photo, smartphone selfie style` },
    { type: 'elegant', getPrompt: (aff) => `elegant cocktail dress, sophisticated style, ${getRandomBg('night')}, glamorous makeup, classy pose, evening wear` },
    { type: 'swimsuit', getPrompt: (aff) => aff > 40 ? `wearing sexy bikini, ${getRandomBg('outdoor')}, beach or pool setting, showing curves, wet skin` : `wearing stylish swimsuit, ${getRandomBg('outdoor')}, beach setting, summer vibes` },
    { type: 'sexy', getPrompt: (aff) => aff > 75 ? `nude in ${getRandomBg('home')}, intimate bedroom setting, sensual pose, naked body visible, explicit` : aff > 50 ? `wearing sexy lingerie, ${getRandomBg('home')}, seductive look, intimate setting, lace underwear` : `wearing revealing outfit, low cut top, ${getRandomBg('night')}, seductive pose, showing cleavage` }
];

function checkLogin() {
    if (user) {
        document.getElementById('headerUserName').textContent = user.name;
        document.getElementById('bottomNav').style.display = 'flex';
        navigateTo('discover');
        initSwipe();
        updateSettingsPage();
    }
}

function login() {
    const name = document.getElementById('userName').value.trim();
    const age = parseInt(document.getElementById('userAge').value);
    if (!name || !age || age < 18) {
        alert('Entre ton prenom et ton age (18+)');
        return;
    }
    user = { name, age };
    localStorage.setItem('dreamUser', JSON.stringify(user));
    document.getElementById('headerUserName').textContent = name;
    document.getElementById('bottomNav').style.display = 'flex';
    navigateTo('discover');
    initSwipe();
    updateSettingsPage();
}

function navigateTo(page) {
    lastNavTab = page;
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    
    const pageMap = {
        'discover': 'pageDiscover',
        'messages': 'pageMessages',
        'matches': 'pageMatches',
        'gallery': 'pageGallery',
        'settings': 'pageSettings'
    };
    
    const pageEl = document.getElementById(pageMap[page]);
    if (pageEl) pageEl.classList.add('active');
    
    const navEl = document.getElementById('nav' + page.charAt(0).toUpperCase() + page.slice(1));
    if (navEl) navEl.classList.add('active');
    
    document.getElementById('bottomNav').style.display = 'flex';
    
    if (page === 'matches') renderMatches();
    if (page === 'messages') renderMessagesList();
    if (page === 'gallery') renderGallery();
    if (page === 'settings') updateSettingsPage();
}

function renderMessagesList() {
    const list = document.getElementById('messagesList');
    const noMsg = document.getElementById('noMessagesText');
    
    const chatsWithMessages = matches.filter(id => {
        const chat = chatHistory[id] || loadChatHistory(id);
        return chat && chat.length > 0;
    });
    
    if (chatsWithMessages.length === 0) {
        list.innerHTML = '';
        noMsg.style.display = 'block';
        return;
    }
    
    noMsg.style.display = 'none';
    list.innerHTML = chatsWithMessages.map(id => {
        const g = GIRLS[id];
        const chat = chatHistory[id] || [];
        const lastMsg = chat[chat.length - 1];
        const preview = lastMsg ? (lastMsg.content.substring(0, 40) + (lastMsg.content.length > 40 ? '...' : '')) : 'Nouvelle conversation';
        const time = lastMsg ? lastMsg.time : '';
        return `
            <div class="message-item" onclick="openChatDirectly('${id}')">
                <div class="message-avatar">${INITIALS[id]}</div>
                <div class="message-info">
                    <div class="message-name">${g.name}</div>
                    <div class="message-preview">${preview}</div>
                </div>
                <div class="message-time">${time}</div>
            </div>
        `;
    }).join('');
}

function openChatDirectly(girlId) {
    currentGirl = girlId;
    if (!chatHistory[girlId]) chatHistory[girlId] = loadChatHistory(girlId);
    const g = GIRLS[girlId];
    document.getElementById('chatName').textContent = g.name;
    document.getElementById('chatInitials').textContent = INITIALS[girlId];
    renderMessages();
    showPage('chat');
}

function renderGallery() {
    const gallery = document.getElementById('photosGallery');
    const noPhotos = document.getElementById('noPhotosText');
    
    let totalPhotos = 0;
    let html = '<h2>Photos Recues</h2>';
    
    Object.keys(receivedPhotos).forEach(girlId => {
        const photos = receivedPhotos[girlId];
        if (photos && photos.length > 0) {
            totalPhotos += photos.length;
            const g = GIRLS[girlId];
            html += `
                <div class="gallery-section">
                    <div class="gallery-section-title">${g.name} - ${photos.length} photo${photos.length > 1 ? 's' : ''}</div>
                    <div class="photos-grid">
                        ${photos.map((url, i) => `
                            <div class="gallery-photo" onclick="openGalleryPhoto('${girlId}', ${i})">
                                <img src="${url}" alt="" loading="lazy">
                            </div>
                        `).join('')}
                    </div>
                </div>
            `;
        }
    });
    
    if (totalPhotos === 0) {
        gallery.innerHTML = '';
        noPhotos.style.display = 'block';
    } else {
        noPhotos.style.display = 'none';
        gallery.innerHTML = html;
    }
}

function openGalleryPhoto(girlId, index) {
    currentOverlayPhotos = receivedPhotos[girlId] || [];
    currentOverlayIndex = index;
    updateOverlay();
    document.getElementById('img-overlay').style.display = 'flex';
}

function updateSettingsPage() {
    if (!user) return;
    document.getElementById('settingsAvatar').textContent = user.name.charAt(0).toUpperCase();
    document.getElementById('settingsName').textContent = user.name;
    document.getElementById('settingsAge').textContent = user.age + ' ans';
    document.getElementById('statsMatches').textContent = matches.length;
    
    let photoCount = 0;
    Object.values(receivedPhotos).forEach(arr => { photoCount += (arr || []).length; });
    document.getElementById('statsPhotos').textContent = photoCount;
    
    let chatCount = 0;
    matches.forEach(id => {
        const chat = chatHistory[id] || loadChatHistory(id);
        if (chat && chat.length > 0) chatCount++;
    });
    document.getElementById('statsChats').textContent = chatCount;
}

function logout() {
    localStorage.removeItem('dreamUser');
    user = null;
    document.getElementById('bottomNav').style.display = 'none';
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.getElementById('pageLogin').classList.add('active');
}

function resetAllData() {
    if (confirm('Effacer toutes les donnees? Cette action est irreversible.')) {
        localStorage.clear();
        location.reload();
    }
}

function initSwipe() {
    swipeQueue = Object.keys(GIRLS).filter(id => {
        if (matches.includes(id) || passed.includes(id) || blocked.includes(id)) return false;
        const g = GIRLS[id];
        if (!matchesAgeFilter(g)) return false;
        if (!matchesRegionFilter(g)) return false;
        return true;
    });
    swipeQueue = swipeQueue.sort(() => Math.random() - 0.5);
    Object.keys(GIRLS).forEach(id => { 
        chatHistory[id] = loadChatHistory(id);
        if (affectionLevels[id] === undefined) affectionLevels[id] = 20;
    });
    localStorage.setItem('affectionLevels', JSON.stringify(affectionLevels));
    showNextCard();
    renderMatches();
    updateMessageBadge();
    applyTheme();
}

function showNextCard() {
    if (swipeQueue.length === 0) {
        document.getElementById('swipeCard').style.display = 'none';
        document.getElementById('swipeButtons').style.display = 'none';
        document.getElementById('noMoreCards').style.display = 'block';
        return;
    }
    currentSwipeGirl = swipeQueue[0];
    const g = GIRLS[currentSwipeGirl];
    document.getElementById('swipeCardImg').textContent = INITIALS[currentSwipeGirl];
    document.getElementById('swipeCardName').textContent = g.name + ', ' + g.age;
    document.getElementById('swipeCardLocation').textContent = g.location;
    document.getElementById('swipeCardBio').textContent = g.bio;
    document.getElementById('swipeCard').style.display = 'block';
    document.getElementById('swipeButtons').style.display = 'flex';
    document.getElementById('noMoreCards').style.display = 'none';
}

function swipeLeft() {
    if (!currentSwipeGirl) return;
    passed.push(currentSwipeGirl);
    localStorage.setItem('dreamPassed', JSON.stringify(passed));
    swipeQueue.shift();
    showNextCard();
}

function swipeRight() {
    if (!currentSwipeGirl) return;
    const g = GIRLS[currentSwipeGirl];
    const matchChance = g.match_chance || 0.7;
    
    if (Math.random() < matchChance) {
        matches.push(currentSwipeGirl);
        localStorage.setItem('dreamMatches', JSON.stringify(matches));
        showMatchAnimation(currentSwipeGirl);
    } else {
        showNoMatch();
    }
    swipeQueue.shift();
}

function showMatchAnimation(girlId) {
    playSound('match');
    const g = GIRLS[girlId];
    document.getElementById('matchPhotoUser').textContent = user.name.charAt(0).toUpperCase();
    document.getElementById('matchPhotoGirl').textContent = INITIALS[girlId];
    document.getElementById('matchNames').textContent = user.name + ' & ' + g.name;
    
    const heartsDiv = document.getElementById('hearts');
    heartsDiv.innerHTML = '';
    for (let i = 0; i < 20; i++) {
        const heart = document.createElement('div');
        heart.className = 'heart';
        heart.textContent = '♥';
        heart.style.left = Math.random() * 100 + '%';
        heart.style.animationDelay = Math.random() * 2 + 's';
        heart.style.color = '#e91e63';
        heartsDiv.appendChild(heart);
    }
    
    document.getElementById('matchOverlay').style.display = 'flex';
    girlMessagesFirst(girlId);
}

function showNoMatch() {
    const msg = document.getElementById('noMatchMsg');
    msg.style.display = 'block';
    setTimeout(() => {
        msg.style.display = 'none';
        showNextCard();
    }, 1500);
}

function closeMatch() {
    document.getElementById('matchOverlay').style.display = 'none';
    renderMatches();
    showNextCard();
}

function goToMatchChat() {
    document.getElementById('matchOverlay').style.display = 'none';
    const lastMatch = matches[matches.length - 1];
    showProfile(lastMatch);
    renderMatches();
}

function renderMatches() {
    const grid = document.getElementById('matchesGrid');
    if (matches.length === 0) {
        grid.style.display = 'none';
        document.getElementById('noMatches').style.display = 'block';
        return;
    }
    grid.style.display = 'grid';
    document.getElementById('noMatches').style.display = 'none';
    grid.innerHTML = matches.map(id => {
        const g = GIRLS[id];
        return `
            <div class="girl-card" onclick="showProfile('${id}')">
                <div class="girl-card-img">${INITIALS[id]}</div>
                <div class="girl-card-info">
                    <div class="girl-card-name">${g.name}, ${g.age}</div>
                    <div class="girl-card-tagline">${g.tagline}</div>
                </div>
            </div>
        `;
    }).join('');
}

function init() {
    checkLogin();
}

let lastNavTab = 'discover';

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const pageId = 'page' + page.charAt(0).toUpperCase() + page.slice(1);
    const pageEl = document.getElementById(pageId);
    if (pageEl) pageEl.classList.add('active');
    
    if (['profile', 'chat'].includes(page)) {
        document.getElementById('bottomNav').style.display = 'none';
    } else {
        document.getElementById('bottomNav').style.display = 'flex';
    }
}

function goBackFromProfile() {
    navigateTo(lastNavTab);
}

function goBackFromChat() {
    showPage('profile');
}

function showProfile(id) {
    if (!matches.includes(id)) {
        showToast("Tu dois d'abord matcher avec elle!");
        return;
    }
    currentGirl = id;
    const g = GIRLS[id];
    document.getElementById('profileName').textContent = g.name + ', ' + g.age;
    document.getElementById('profileTagline').textContent = g.tagline;
    document.getElementById('profileBio').textContent = g.bio;
    document.getElementById('profileAffection').textContent = affectionLevels[id] + '%';
    
    document.getElementById('profileMainPhoto').textContent = INITIALS[id];
    loadProfilePhotos(id);
    
    showPage('profile');
}

function showToast(msg) {
    const toast = document.getElementById('toast');
    toast.textContent = msg;
    toast.style.display = 'block';
    setTimeout(() => { toast.style.display = 'none'; }, 2000);
}

async function loadProfilePhotos(girlId) {
    const grid = document.getElementById('profilePhotoGrid');
    const mainPhoto = document.getElementById('profileMainPhoto');
    const g = GIRLS[girlId];
    
    // Check if all 4 photos exist in localStorage
    if (profilePhotos[girlId] && profilePhotos[girlId].filter(p => p).length === 4) {
        renderProfilePhotos(girlId);
        return;
    }
    
    // Show loading state
    const photoLabels = ['Selfie', 'Exterieur', 'Soiree', 'Intime'];
    mainPhoto.innerHTML = '<div class="photo-loading"><div class="spinner"></div><span>Chargement...</span></div>';
    mainPhoto.style.fontSize = '1rem';
    
    grid.innerHTML = photoLabels.map((label, i) => `
        <div class="photo-grid-item">
            <div class="photo-loading"><div class="spinner"></div><span>${label}</span></div>
        </div>
    `).join('');
    
    const aff = affectionLevels[girlId] || 20;
    if (!profilePhotos[girlId]) profilePhotos[girlId] = [null, null, null, null];
    
    for (let i = 0; i < PHOTO_TYPES.length; i++) {
        if (profilePhotos[girlId][i]) {
            renderProfilePhotos(girlId);
            continue;
        }
        
        if (currentGirl !== girlId) return;
        
        try {
            const photoPrompt = PHOTO_TYPES[i].getPrompt(aff);
            const res = await fetch('/photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    girl: girlId,
                    affection: aff,
                    description: photoPrompt
                })
            });
            const data = await res.json();
            
            if (currentGirl !== girlId) return;
            
            if (data.image_url) {
                profilePhotos[girlId][i] = data.image_url;
                localStorage.setItem('profilePhotos', JSON.stringify(profilePhotos));
                renderProfilePhotos(girlId);
            }
        } catch (e) {
            console.error('Photo generation error:', e);
        }
    }
}

function renderProfilePhotos(girlId) {
    // Guard: only render if this is still the active profile
    if (currentGirl !== girlId) return;
    
    const grid = document.getElementById('profilePhotoGrid');
    const mainPhoto = document.getElementById('profileMainPhoto');
    const photos = profilePhotos[girlId] || [];
    
    if (photos.length > 0) {
        mainPhoto.innerHTML = `<img src="${photos[0]}" style="width:100%;height:100%;object-fit:cover;">`;
        mainPhoto.style.fontSize = '';
    } else {
        mainPhoto.textContent = INITIALS[girlId];
    }
    
    const labels = ['Selfie', 'Exterieur', 'Soiree', 'Intime'];
    grid.innerHTML = labels.map((label, i) => {
        if (photos[i]) {
            return `<div class="photo-grid-item" onclick="openGallery('${girlId}', ${i})"><img src="${photos[i]}" alt="${label}"></div>`;
        } else {
            return `<div class="photo-grid-item"><div class="photo-loading"><div class="spinner"></div><span>${label}</span></div></div>`;
        }
    }).join('');
}

function openGallery(girlId, index) {
    currentOverlayPhotos = profilePhotos[girlId] || [];
    currentOverlayIndex = index;
    updateOverlay();
    document.getElementById('img-overlay').style.display = 'flex';
}

function updateOverlay() {
    if (currentOverlayPhotos.length === 0) return;
    document.getElementById('overlay-img').src = currentOverlayPhotos[currentOverlayIndex];
    document.getElementById('overlay-counter').textContent = (currentOverlayIndex + 1) + ' / ' + currentOverlayPhotos.length;
}

function prevOverlayImg() {
    if (currentOverlayPhotos.length === 0) return;
    currentOverlayIndex = (currentOverlayIndex - 1 + currentOverlayPhotos.length) % currentOverlayPhotos.length;
    updateOverlay();
}

function nextOverlayImg() {
    if (currentOverlayPhotos.length === 0) return;
    currentOverlayIndex = (currentOverlayIndex + 1) % currentOverlayPhotos.length;
    updateOverlay();
}

function showVideoToast() {
    showToast('Bientôt disponible');
}

let storyPhotos = [];
let storyIndex = 0;
let storyTimer = null;

const STORY_TEXTS = [
    "Coucou c'est moi",
    "Ma journee en photos",
    "Qu'est-ce que tu en penses?",
    "Tu me manques..."
];

function openStories() {
    const photos = profilePhotos[currentGirl] || [];
    if (photos.filter(p => p).length === 0) {
        showToast("Pas encore de photos disponibles");
        return;
    }
    storyPhotos = photos.filter(p => p);
    storyIndex = 0;
    
    const progressDiv = document.getElementById('storyProgress');
    progressDiv.innerHTML = storyPhotos.map((_, i) => `<div class="story-bar"><div class="story-bar-fill" id="bar${i}"></div></div>`).join('');
    
    document.getElementById('storyOverlay').style.display = 'flex';
    showStory();
}

function showStory() {
    if (storyIndex >= storyPhotos.length) {
        closeStories();
        return;
    }
    document.getElementById('storyImg').src = storyPhotos[storyIndex];
    document.getElementById('storyText').textContent = STORY_TEXTS[storyIndex % STORY_TEXTS.length];
    
    for (let i = 0; i < storyPhotos.length; i++) {
        const bar = document.getElementById('bar' + i);
        if (bar) {
            bar.style.transition = 'none';
            bar.style.width = i < storyIndex ? '100%' : '0%';
        }
    }
    
    const currentBar = document.getElementById('bar' + storyIndex);
    if (currentBar) {
        setTimeout(() => {
            currentBar.style.transition = 'width 5s linear';
            currentBar.style.width = '100%';
        }, 50);
    }
    
    clearTimeout(storyTimer);
    storyTimer = setTimeout(() => {
        storyIndex++;
        showStory();
    }, 5000);
}

function nextStory() {
    storyIndex++;
    showStory();
}

function prevStory() {
    if (storyIndex > 0) storyIndex--;
    showStory();
}

function closeStories() {
    clearTimeout(storyTimer);
    document.getElementById('storyOverlay').style.display = 'none';
}

function startChat() {
    const g = GIRLS[currentGirl];
    document.getElementById('chatInitials').textContent = INITIALS[currentGirl];
    document.getElementById('chatName').textContent = g.name;
    renderMessages();
    showPage('chat');
    document.getElementById('chatInput').focus();
}

function getTime() {
    const now = new Date();
    return now.getHours().toString().padStart(2, '0') + ':' + now.getMinutes().toString().padStart(2, '0');
}

function renderMessages() {
    const msgs = chatHistory[currentGirl];
    const container = document.getElementById('messages');
    
    if (msgs.length === 0) {
        container.innerHTML = '<div class="empty-chat">DÉBUT DE LA CONVERSATION</div>';
        return;
    }
    
    container.innerHTML = msgs.map(m => {
        const cls = m.role === 'user' ? 'user' : 'her';
        const text = (m.content || '').replace(/\\[PHOTO:[^\\]]+\\]/g, '').trim();
        const imgHtml = m.image ? `<div class="msg-img" onclick="fullscreenImg('${m.image}')"><img src="${m.image}" alt="Photo"></div>` : '';
        const receipt = m.role === 'user' ? '<span class="read-receipt">✓✓</span>' : '';
        
        return `<div class="msg ${cls}">
            ${text ? `<div class="msg-bubble">${text}</div>` : ''}
            ${imgHtml}
            <div class="msg-meta">${m.time} ${receipt}</div>
        </div>`;
    }).join('');
    
    container.scrollTop = container.scrollHeight;
}

function fullscreenImg(url) {
    currentOverlayPhotos = [url];
    currentOverlayIndex = 0;
    document.getElementById('overlay-img').src = url;
    document.getElementById('overlay-counter').textContent = '1 / 1';
    document.getElementById('img-overlay').style.display = 'flex';
}

function setTyping(isTyping) {
    const el = document.getElementById('typing-indicator');
    if (isTyping) {
        el.innerText = GIRLS[currentGirl].name + ' écrit...';
        el.style.display = 'block';
    } else {
        el.style.display = 'none';
    }
}

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;
    
    playSound('send');
    input.value = '';
    document.getElementById('sendBtn').disabled = true;
    document.getElementById('icebreakers').style.display = 'none';
    clearUnreadMessages(currentGirl);
    
    const lowerText = text.toLowerCase();
    if (['belle', 'jolie', 'adore', 'sexy', 'magnifique', 'charme', 'parfaite', 'canon', 'plait'].some(word => lowerText.includes(word))) {
        affectionLevels[currentGirl] = Math.min(100, affectionLevels[currentGirl] + 5);
    }
    
    // Auto-trigger photo if keywords detected
    let autoRequestPhoto = false;
    if (['photo', 'nude', 'montre', 'voir', 'déshabille', 'nu', 'corps', 'poitrine', 'fesse'].some(word => lowerText.includes(word))) {
        affectionLevels[currentGirl] = Math.min(100, affectionLevels[currentGirl] + 2);
        autoRequestPhoto = true;
    }
    
    localStorage.setItem('affectionLevels', JSON.stringify(affectionLevels));
    
    chatHistory[currentGirl].push({ role: 'user', content: text, time: getTime() });
    saveChatHistory(currentGirl);
    renderMessages();
    
    const typingDelay = 1500 + Math.random() * 2000;
    setTimeout(() => setTyping(true), typingDelay);
    
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                affection: affectionLevels[currentGirl],
                auto_photo: autoRequestPhoto,
                messages: chatHistory[currentGirl].slice(-15).map(m => ({ role: m.role, content: m.content }))
            })
        });
        
        const data = await res.json();
        setTyping(false);
        playSound('message');
        
        let reply = data.reply || "Désolée, j'ai un souci technique...";
        const photoMatch = reply.match(/\\[PHOTO:\\s*([^\\]]+)\\]/i);
        const cleanReply = reply.replace(/\\[PHOTO:[^\\]]+\\]/gi, '').trim();
        
        const msgObj = { role: 'assistant', content: cleanReply, time: getTime() };
        chatHistory[currentGirl].push(msgObj);
        saveChatHistory(currentGirl);
        renderMessages();
        
        if (photoMatch) {
            await generatePhoto(photoMatch[1], msgObj);
        } else if (data.smart_photo) {
            await generatePhoto(data.smart_photo, msgObj);
        }
    } catch (e) {
        setTyping(false);
        chatHistory[currentGirl].push({ role: 'assistant', content: "Désolée, erreur réseau.", time: getTime() });
        saveChatHistory(currentGirl);
        renderMessages();
    }
    
    document.getElementById('sendBtn').disabled = false;
}

async function requestProfilePhoto() {
    startChat();
    const msgObj = { role: 'assistant', content: "Tiens, une photo rien que pour toi...", time: getTime() };
    chatHistory[currentGirl].push(msgObj);
    saveChatHistory(currentGirl);
    renderMessages();
    await generatePhoto("casual selfie, beautiful smile, high quality", msgObj);
}

async function generatePhoto(description, msgObj) {
    try {
        const res = await fetch('/photo', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                affection: affectionLevels[currentGirl],
                description: description
            })
        });
        
        const data = await res.json();
        if (data.image_url) {
            msgObj.image = data.image_url;
            saveReceivedPhoto(currentGirl, data.image_url);
            saveChatHistory(currentGirl);
            renderMessages();
        }
    } catch (e) { console.error('Photo error:', e); }
}

document.getElementById('chatInput').addEventListener('keypress', e => {
    if (e.key === 'Enter') sendMessage();
});

init();
</script>
</body>
</html>'''


@app.route('/')
def home():
    return Response(HTML, mimetype='text/html')


PHOTO_KEYWORDS = {
    'culotte': 'showing panties, lifting skirt, revealing underwear',
    'panties': 'showing panties, lifting skirt, revealing underwear',
    'string': 'showing thong, from behind, bent over',
    'seins': 'topless, showing breasts, nude chest',
    'poitrine': 'topless, showing breasts, cleavage',
    'nichons': 'topless, big breasts, nude',
    'teton': 'topless, nipples visible, breasts',
    'haut': 'removing top, taking off shirt',
    'top': 'removing top, showing bra',
    'soutif': 'showing bra, removing bra, lace bra',
    'soutien': 'showing bra, lace bra, cleavage',
    'pantalon': 'removing pants, showing legs, underwear visible',
    'jupe': 'lifting skirt, showing legs, panties visible',
    'robe': 'removing dress, in underwear',
    'nue': 'fully nude, naked, no clothes',
    'naked': 'fully nude, naked body',
    'tout': 'fully nude, completely naked, showing everything',
    'deshabille': 'undressing, removing clothes, stripping',
    'fesses': 'showing butt, from behind, bent over',
    'cul': 'showing ass, from behind, bent over nude',
    'chatte': 'nude, legs spread, intimate pose',
    'pussy': 'nude, legs spread, showing pussy',
    'sexe': 'nude, intimate pose, explicit',
    'ecarte': 'legs spread, nude, showing pussy',
    'allonge': 'lying in bed, nude, seductive pose',
    'lit': 'in bed, bedroom, intimate',
    'douche': 'in shower, wet, nude',
    'bain': 'in bath, wet body, nude'
}

def detect_photo_request(message):
    msg_lower = message.lower()
    for keyword, photo_desc in PHOTO_KEYWORDS.items():
        if keyword in msg_lower:
            return photo_desc
    photo_triggers = ['montre', 'envoie', 'photo', 'voir', 'vois', 'regarde', 'image']
    if any(trigger in msg_lower for trigger in photo_triggers):
        return 'sexy pose, seductive'
    return None

RUDE_WORDS = ['pute', 'salope', 'connasse', 'chienne', 'garce', 'idiote', 'conne', 'ferme', 'ta gueule', 'nique', 'fuck you', 'bitch', 'whore']
RUSHING_WORDS = ['nude', 'nue', 'seins', 'chatte', 'pussy', 'baise', 'suce', 'levrette', 'sexe']

DEFAULT_PERSONALITY = "Tu es une fille normale, sympa mais pas facile. Tu aimes les mecs drôles et respectueux."

def detect_mood(messages, affection):
    if len(messages) < 2:
        return "neutral"
    
    last_msgs = [m['content'].lower() for m in messages[-5:] if m.get('role') == 'user']
    text = ' '.join(last_msgs)
    
    if any(w in text for w in RUDE_WORDS):
        return "annoyed"
    
    if any(w in text for w in ['belle', 'magnifique', 'adorable', 'mdr', 'haha', 'drole']):
        if affection > 50:
            return "happy"
        return "neutral"
    
    if affection > 70 and any(w in text for w in ['envie', 'chaud', 'excite', 'hot']):
        return "horny"
    
    import random
    if random.random() < 0.1:
        return random.choice(["happy", "neutral", "annoyed"])
    
    return "neutral"

def check_behavior(last_msg, affection, msg_count):
    msg_lower = last_msg.lower()
    
    if any(w in msg_lower for w in RUDE_WORDS):
        return "rude"
    
    if affection < 30 and any(w in msg_lower for w in RUSHING_WORDS):
        return "rushing"
    
    if affection < 20 and any(w in msg_lower for w in ['photo', 'nude', 'montre']):
        return "too_early"
    
    return "ok"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    messages = data.get('messages', [])
    affection = data.get('affection', 20)
    auto_photo = data.get('auto_photo', False)
    
    girl = GIRLS.get(girl_id, GIRLS.get('jade', list(GIRLS.values())[0]))
    msg_count = len(messages)
    
    last_user_msg = messages[-1]['content'] if messages else ""
    smart_photo_desc = detect_photo_request(last_user_msg)
    
    mood = detect_mood(messages, affection)
    behavior = check_behavior(last_user_msg, affection, msg_count)
    
    personality = girl.get('personality', DEFAULT_PERSONALITY)
    
    if behavior == "rude":
        import random
        responses = [
            "Ok bye, j'ai pas besoin de ça",
            "Wow t'es sérieux là? Ciao",
            "Non mais t'es malade toi, je te bloque",
            "Pas besoin d'être vulgaire, bye"
        ]
        return jsonify({"reply": random.choice(responses), "smart_photo": None, "unmatch": True})
    
    if behavior == "rushing":
        import random
        responses = [
            "Wow calme toi, on se connait à peine là",
            "Haha on se calme, on vient de matcher",
            "T'es speed toi mdr, on se connait même pas",
            "Du calme cowboy, on discute d'abord non?"
        ]
        return jsonify({"reply": random.choice(responses), "smart_photo": None})
    
    if behavior == "too_early":
        import random
        responses = [
            "Tu crois quoi? On vient de matcher lol",
            "Haha non merci, faut le mériter ça",
            "Mdr t'es direct toi, peut-être si t'es sage",
            "Je suis pas ce genre de fille... enfin pas tout de suite"
        ]
        return jsonify({"reply": random.choice(responses), "smart_photo": None})
    
    photo_instruction = ""
    if affection < 30:
        photo_instruction = "Tu refuses les photos intimes. Tu peux envoyer un selfie habillé max."
    elif affection < 50:
        photo_instruction = "Tu peux envoyer des photos sexy mais pas nue. [PHOTO: sexy outfit, cleavage]"
    elif affection < 75:
        photo_instruction = "Tu peux envoyer des photos en lingerie. [PHOTO: lingerie, bra]"
    else:
        photo_instruction = "Tu envoies des photos nues sans problème. [PHOTO: nude, topless]"
    
    mood_instruction = ""
    if mood == "happy":
        mood_instruction = "Tu es de bonne humeur, flirty, tu utilises des emojis."
    elif mood == "annoyed":
        mood_instruction = "Tu es agacée. Réponses courtes: 'Ouais', 'Mdr ok', 'Si tu veux'. Tu peux ignorer la question."
    elif mood == "horny":
        mood_instruction = "Tu es excitée. Tu parles de sexe, tu inities le sexting, tu proposes des photos."
    else:
        mood_instruction = "Tu es neutre, tu discutes normalement."
    
    system_content = SYSTEM_PROMPT.replace("{name}", girl['name']).replace("{age}", str(girl['age'])).replace("{affection}", str(affection)).replace("{personality}", personality).replace("{mood}", mood)
    system_content += f"\n\n{mood_instruction}\n{photo_instruction}"
    
    if auto_photo and affection >= 30:
        system_content += "\nL'utilisateur demande une photo. Décris-la puis ajoute [PHOTO: description]."
    elif auto_photo and affection < 30:
        system_content += "\nL'utilisateur demande une photo mais tu ne le connais pas assez. Refuse gentiment."
    
    all_messages = [{"role": "system", "content": system_content}] + messages[-15:]
    
    print(f"[CHAT] Girl: {girl['name']}, Affection: {affection}, Mood: {mood}, Behavior: {behavior}")
    
    import urllib.parse
    
    try:
        full_prompt = f"{system_content}\n\n"
        for m in messages[-10:]:
            role = "User" if m['role'] == 'user' else "Assistant"
            full_prompt += f"{role}: {m['content']}\n"
        full_prompt += "Assistant:"
        
        encoded_prompt = urllib.parse.quote(full_prompt[:3000])
        response = requests.get(
            f'https://text.pollinations.ai/{encoded_prompt}',
            timeout=45
        )
        
        if response.ok and response.text and len(response.text) > 5:
            reply = response.text.strip()
            print(f"[CHAT] Pollinations reply: {reply[:100]}...")
            
            if affection < 30:
                smart_photo_desc = None
            
            return jsonify({"reply": reply, "smart_photo": smart_photo_desc})
    except Exception as e:
        print(f"Pollinations error: {e}")
    
    try:
        response = requests.post(
            'https://api.deepinfra.com/v1/openai/chat/completions',
            json={
                "model": "Sao10K/L3.1-70B-Euryale-v2.3",
                "messages": all_messages,
                "max_tokens": 300,
                "temperature": 0.7
            },
            timeout=45
        )
        
        if response.ok:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            print(f"[CHAT] DeepInfra reply: {reply[:100]}...")
            return jsonify({"reply": reply, "smart_photo": smart_photo_desc if affection >= 30 else None})
        else:
            print(f"DeepInfra status: {response.status_code}, {response.text[:200]}")
    except Exception as e:
        print(f"DeepInfra error: {e}")
    
    import random
    fallbacks = [
        "Désolée je peux pas là, je te reparle plus tard",
        "Attend 2 sec, je reviens",
        "Jsuis occupée là, on se reparle?",
        "Mon tel bug, réessaie"
    ]
    return jsonify({"reply": random.choice(fallbacks), "smart_photo": None})


@app.route('/photo', methods=['POST'])
def photo():
    if not API_KEY:
        return jsonify({"error": "PROMPTCHAN_KEY not set"})
    
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    description = data.get('description', '')
    affection = data.get('affection', 20)
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    
    mood_prompt = ""
    if affection < 30:
        mood_prompt = "wearing elegant classy dress, beautiful, soft lighting"
    elif affection < 50:
        mood_prompt = "wearing tight sexy dress, showing legs, cleavage, seductive look"
    elif affection < 75:
        mood_prompt = "wearing sexy lingerie, lace bra, bedroom setting, seductive pose, intimate"
    else:
        mood_prompt = "nude, topless, naked, bedroom, seductive intimate pose, sensual lighting"

    full_prompt = f"{girl['appearance']}, {mood_prompt}, {description}"
    
    try:
        response = requests.post(
            'https://prod.aicloudnetservices.com/api/external/create',
            headers={
                'Content-Type': 'application/json',
                'x-api-key': API_KEY
            },
            json={
                "style": "Photo XL+ v2",
                "pose": "Default",
                "prompt": full_prompt,
                "quality": "Ultra",
                "expression": "Neutral",
                "age_slider": girl.get('age_slider', girl['age']),
                "creativity": 50,
                "restore_faces": True,
                "seed": -1
            },
            timeout=30
        )
        
        if response.ok:
            result = response.json()
            image_val = result.get('image', result.get('image_url', ''))
            
            if image_val:
                if isinstance(image_val, str) and not image_val.startswith('http') and not image_val.startswith('data:'):
                    image_val = 'https://cdn.promptchan.ai/' + image_val
                return jsonify({"image_url": image_val})
            
        return jsonify({"error": "No image in response"})
            
    except Exception as e:
        print(f"Photo error: {e}")
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
