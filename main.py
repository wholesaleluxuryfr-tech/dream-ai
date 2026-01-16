import os
import json
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

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
        "body_type": "alternative"
    }
}

HTML = '''<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Dream AI</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: #0a0a0c; color: #ffffff; min-height: 100vh; -webkit-tap-highlight-color: transparent; }
        
        .page { display: none; min-height: 100vh; overflow-x: hidden; }
        .page.active { display: flex; flex-direction: column; }
        
        /* LOGIN PAGE */
        .login-page { justify-content: center; align-items: center; padding: 2rem; }
        .login-box { max-width: 400px; width: 100%; text-align: center; }
        .login-logo { font-size: 3rem; font-weight: 800; color: #e91e63; margin-bottom: 0.5rem; }
        .login-subtitle { color: #888; font-size: 1rem; margin-bottom: 2rem; }
        .login-form { display: flex; flex-direction: column; gap: 1rem; }
        .login-input { padding: 1rem 1.5rem; background: #12121a; border: 1px solid #1a1a1f; border-radius: 15px; color: white; font-size: 1rem; outline: none; }
        .login-input:focus { border-color: #e91e63; }
        .login-btn { padding: 1.1rem; background: #e91e63; border: none; border-radius: 15px; color: white; font-size: 1rem; font-weight: 700; cursor: pointer; margin-top: 1rem; }
        
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
        .swipe-btn { width: 70px; height: 70px; border-radius: 50%; border: none; font-size: 2rem; cursor: pointer; transition: transform 0.2s; }
        .swipe-btn:active { transform: scale(0.9); }
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
        .girl-card { background: #12121a; border-radius: 20px; overflow: hidden; cursor: pointer; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease; position: relative; border: 1px solid rgba(255, 255, 255, 0.05); }
        .girl-card:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.5); }
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
        .btn-premium { width: 100%; padding: 1.1rem; border: none; border-radius: 15px; font-size: 1rem; font-weight: 700; cursor: pointer; transition: transform 0.2s, opacity 0.2s; text-align: center; text-decoration: none; }
        .btn-chat { background: #e91e63; color: #ffffff; box-shadow: 0 5px 15px rgba(233, 30, 99, 0.3); }
        .btn-photo { background: #12121a; color: #ffffff; border: 1px solid rgba(255, 255, 255, 0.1); }
        .btn-premium:active { transform: scale(0.98); }
        
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
        .send-btn { width: 50px; height: 50px; border-radius: 50%; background: #e91e63; border: none; color: #ffffff; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 10px rgba(233, 30, 99, 0.3); transition: transform 0.2s; }
        .send-btn:active { transform: scale(0.9); }
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

<!-- MAIN PAGE (Swipe + Matches) -->
<div class="page" id="pageMain">
    <div class="header">
        <div class="header-row">
            <div class="logo">DREAM AI</div>
            <div class="user-name" id="headerUserName"></div>
        </div>
    </div>
    <div class="nav-tabs">
        <button class="nav-tab active" id="tabSwipe" onclick="switchTab('swipe')">Découvrir</button>
        <button class="nav-tab" id="tabMatches" onclick="switchTab('matches')">Matchs</button>
    </div>
    
    <!-- SWIPE VIEW -->
    <div id="swipeView">
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
            <button class="swipe-btn swipe-btn-like" onclick="swipeRight()">♥</button>
        </div>
    </div>
    
    <!-- MATCHES VIEW -->
    <div id="matchesView" style="display:none;">
        <div class="gallery">
            <h2>Tes Matchs</h2>
            <div class="girls-grid" id="matchesGrid"></div>
            <div id="noMatches" style="text-align:center;color:#666;padding:3rem;display:none;">
                <p>Pas encore de matchs</p>
                <p style="font-size:0.8rem;margin-top:0.5rem;">Continue à swiper pour en trouver</p>
            </div>
        </div>
    </div>
</div>

<!-- PROFILE PAGE -->
<div class="page" id="pageProfile">
    <div class="profile">
        <div class="back-btn" onclick="showPage('main')">←</div>
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
        <div class="back-btn" onclick="showPage('profile')">←</div>
        <div class="chat-avatar-circle" id="chatInitials"></div>
        <div class="chat-info">
            <div class="chat-name" id="chatName"></div>
            <div class="chat-status"><span class="status-dot"></span> Online</div>
        </div>
    </div>
    <div class="messages" id="messages"></div>
    <div class="input-area">
        <div id="typing-indicator" class="typing-indicator"></div>
        <div class="input-row">
            <input type="text" class="chat-input" id="chatInput" placeholder="Écris un message...">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">➤</button>
        </div>
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

let currentGirl = null;
let chatHistory = {};
let affectionLevels = JSON.parse(localStorage.getItem('affectionLevels') || '{}');
let profilePhotos = JSON.parse(localStorage.getItem('profilePhotos') || '{}');
let currentOverlayPhotos = [];
let currentOverlayIndex = 0;

let user = JSON.parse(localStorage.getItem('dreamUser') || 'null');
let matches = JSON.parse(localStorage.getItem('dreamMatches') || '[]');
let passed = JSON.parse(localStorage.getItem('dreamPassed') || '[]');
let swipeQueue = [];
let currentSwipeGirl = null;

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
    { type: 'selfie', getPrompt: (aff) => `face closeup selfie, smartphone front camera angle, natural lighting, casual look, ${getRandomBg('home')}, authentic amateur photo style` },
    { type: 'outdoor', getPrompt: (aff) => aff > 50 ? `full body shot, wearing bikini or short dress, ${getRandomBg('outdoor')}, natural daylight, sexy but classy` : `full body outdoor shot, casual summer outfit, ${getRandomBg('day')}, natural daylight` },
    { type: 'nightout', getPrompt: (aff) => `dressed up for night out, tight dress showing curves, ${getRandomBg('night')}, glamorous makeup, seductive pose` },
    { type: 'intimate', getPrompt: (aff) => aff > 75 ? `nude in ${getRandomBg('home')}, intimate bedroom setting, sensual pose, naked body visible` : aff > 40 ? `wearing sexy lingerie, ${getRandomBg('home')}, seductive look, intimate setting` : `wearing elegant dress, ${getRandomBg('home')}, soft bedroom lighting, alluring smile` }
];

function checkLogin() {
    if (user) {
        document.getElementById('headerUserName').textContent = user.name;
        showPage('main');
        initSwipe();
    }
}

function login() {
    const name = document.getElementById('userName').value.trim();
    const age = parseInt(document.getElementById('userAge').value);
    if (!name || !age || age < 18) {
        alert('Entre ton prénom et ton âge (18+)');
        return;
    }
    user = { name, age };
    localStorage.setItem('dreamUser', JSON.stringify(user));
    document.getElementById('headerUserName').textContent = name;
    showPage('main');
    initSwipe();
}

function initSwipe() {
    swipeQueue = Object.keys(GIRLS).filter(id => !matches.includes(id) && !passed.includes(id));
    swipeQueue = swipeQueue.sort(() => Math.random() - 0.5);
    Object.keys(GIRLS).forEach(id => { 
        if (!chatHistory[id]) chatHistory[id] = []; 
        if (affectionLevels[id] === undefined) affectionLevels[id] = 20;
    });
    localStorage.setItem('affectionLevels', JSON.stringify(affectionLevels));
    showNextCard();
    renderMatches();
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

function switchTab(tab) {
    document.getElementById('tabSwipe').classList.toggle('active', tab === 'swipe');
    document.getElementById('tabMatches').classList.toggle('active', tab === 'matches');
    document.getElementById('swipeView').style.display = tab === 'swipe' ? 'block' : 'none';
    document.getElementById('matchesView').style.display = tab === 'matches' ? 'block' : 'none';
    if (tab === 'matches') renderMatches();
}

function init() {
    checkLogin();
}

function showPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const pageId = 'page' + page.charAt(0).toUpperCase() + page.slice(1);
    const pageEl = document.getElementById(pageId);
    if (pageEl) pageEl.classList.add('active');
    if (page === 'main') {
        renderMatches();
        switchTab('swipe');
    }
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
    
    input.value = '';
    document.getElementById('sendBtn').disabled = true;
    
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
    renderMessages();
    
    setTimeout(() => setTyping(true), 1000);
    
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                girl: currentGirl,
                affection: affectionLevels[currentGirl],
                auto_photo: autoRequestPhoto,
                messages: chatHistory[currentGirl].map(m => ({ role: m.role, content: m.content }))
            })
        });
        
        const data = await res.json();
        setTyping(false);
        
        let reply = data.reply || "Désolée, j'ai un souci technique...";
        const photoMatch = reply.match(/\\[PHOTO:\\s*([^\\]]+)\\]/i);
        const cleanReply = reply.replace(/\\[PHOTO:[^\\]]+\\]/gi, '').trim();
        
        const msgObj = { role: 'assistant', content: cleanReply, time: getTime() };
        chatHistory[currentGirl].push(msgObj);
        renderMessages();
        
        if (photoMatch) {
            await generatePhoto(photoMatch[1], msgObj);
        } else if (data.smart_photo) {
            await generatePhoto(data.smart_photo, msgObj);
        }
    } catch (e) {
        setTyping(false);
        chatHistory[currentGirl].push({ role: 'assistant', content: "Désolée, erreur réseau.", time: getTime() });
        renderMessages();
    }
    
    document.getElementById('sendBtn').disabled = false;
}

async function requestProfilePhoto() {
    startChat();
    const msgObj = { role: 'assistant', content: "Tiens, une photo rien que pour toi...", time: getTime() };
    chatHistory[currentGirl].push(msgObj);
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
                "temperature": 0.95
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
