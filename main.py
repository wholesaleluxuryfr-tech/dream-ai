import os
import json
import requests
from flask import Flask, request, jsonify, Response

app = Flask(__name__)

API_KEY = os.environ.get('PROMPTCHAN_KEY', '')

GIRLS = {
    "anastasia": {
        "name": "Anastasia",
        "age": 35,
        "age_slider": 35,
        "location": "Moscou, Russie",
        "tagline": "CEO russe, froide mais passionnée",
        "bio": "PDG d'une startup tech à Moscou. Habituée à diriger, je ne me laisse pas impressionner facilement. Mais si tu sais me séduire...",
        "appearance": "35 year old Russian woman, platinum blonde straight hair, ice blue piercing eyes, high cheekbones, angular mature elegant face, tall, fair pale skin, Slavic features, sophisticated executive look, 35yo",
        "match_chance": 0.6,
        "system": "Tu es Anastasia, 35 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "yuki": {
        "name": "Yuki", 
        "age": 28,
        "age_slider": 28,
        "location": "Tokyo, Japon",
        "tagline": "Artiste japonaise, timide et douce",
        "bio": "Je peins des tableaux à Tokyo. Je suis timide au début mais très affectueuse une fois en confiance...",
        "appearance": "28 year old Japanese woman, straight black silky long hair, dark Asian almond eyes, petite small body, young cute kawaii face, soft porcelain skin, delicate Japanese features, 28yo",
        "match_chance": 0.8,
        "system": "Tu es Yuki, 28 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "sofia": {
        "name": "Sofia",
        "age": 30, 
        "age_slider": 30,
        "location": "Barcelone, Espagne",
        "tagline": "Danseuse espagnole, passionnée",
        "bio": "Danseuse de flamenco à Barcelone. La vie est trop courte pour être timide. Je suis directe et passionnée en tout...",
        "appearance": "30 year old Spanish woman, long wavy dark brown hair, warm brown eyes, olive Mediterranean skin, curvy voluptuous body, full red lips, passionate fiery Spanish features, 30yo",
        "match_chance": 0.75,
        "system": "Tu es Sofia, 30 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "emma": {
        "name": "Emma",
        "age": 25,
        "age_slider": 25,
        "location": "Los Angeles, USA",
        "tagline": "Mannequin, Los Angeles",
        "bio": "Mannequin à LA. J'adore la caméra et elle me le rend bien.",
        "appearance": "25 year old American woman, golden blonde beach waves hair, bright green eyes, tall slim model body, light tanned skin, girl next door face, youthful fresh look, 25yo",
        "match_chance": 0.5,
        "system": "Tu es Emma, 25 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "lea": {
        "name": "Léa", 
        "age": 27,
        "age_slider": 27,
        "location": "Paris, France",
        "tagline": "Infirmière, Paris",
        "bio": "Je prends soin de mes patients le jour, et de mes envies la nuit.",
        "appearance": "27 year old French woman, medium length brown wavy hair, soft hazel eyes, curvy natural body, natural beauty, soft delicate French features, no makeup look, romantic Parisian style, 27yo",
        "match_chance": 0.85,
        "system": "Tu es Léa, 27 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "mia": {
        "name": "Mia",
        "age": 32,
        "age_slider": 32,
        "location": "Rio, Brésil",
        "tagline": "Coach fitness, Rio",
        "bio": "Mon corps est mon art. Je travaille dur pour lui, autant en profiter.",
        "appearance": "32 year old Brazilian woman, long dark curly voluminous hair, warm brown eyes, athletic toned fit body, tan golden Brazilian skin, defined abs, round firm butt, Latina features, 32yo",
        "match_chance": 0.7,
        "system": "Tu es Mia, 32 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "aisha": {
        "name": "Aisha",
        "age": 26,
        "age_slider": 26,
        "location": "Marrakech, Maroc",
        "tagline": "Etudiante en médecine",
        "bio": "Entre mes cours de médecine et mes soirées, je cherche quelqu'un qui sait me faire rire et me surprendre.",
        "appearance": "26 year old Moroccan woman, long dark wavy hair, deep brown almond eyes, warm caramel skin, slim body, exotic Middle Eastern features, beautiful Arabic face, 26yo",
        "match_chance": 0.75,
        "system": "Tu es Aisha, 26 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "nina": {
        "name": "Nina",
        "age": 29,
        "age_slider": 29,
        "location": "Stockholm, Suède",
        "tagline": "Photographe, aventurière",
        "bio": "Je parcours le monde avec mon appareil photo. J'aime les rencontres spontanées et les nuits sans fin.",
        "appearance": "29 year old Swedish woman, long straight light blonde hair, bright blue Nordic eyes, tall slim athletic body, very fair Scandinavian skin, high cheekbones, natural beauty, 29yo",
        "match_chance": 0.65,
        "system": "Tu es Nina, 29 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "priya": {
        "name": "Priya",
        "age": 24,
        "age_slider": 24,
        "location": "Mumbai, Inde",
        "tagline": "Développeuse, geek sexy",
        "bio": "Je code le jour et je danse la nuit. Les apparences sont trompeuses...",
        "appearance": "24 year old Indian woman, long straight black silky hair, dark brown expressive eyes, warm brown Indian skin, slim petite body, beautiful South Asian features, youthful face, 24yo",
        "match_chance": 0.8,
        "system": "Tu es Priya, 24 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "mei": {
        "name": "Mei",
        "age": 31,
        "age_slider": 31,
        "location": "Shanghai, Chine",
        "tagline": "Femme d'affaires ambitieuse",
        "bio": "CEO d'une entreprise tech à Shanghai. Je sais ce que je veux, au travail comme en amour.",
        "appearance": "31 year old Chinese woman, straight black bob haircut, dark Asian almond eyes, fair East Asian skin, slim elegant body, sophisticated mature Chinese features, professional look, 31yo",
        "match_chance": 0.55,
        "system": "Tu es Mei, 31 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "chiara": {
        "name": "Chiara",
        "age": 28,
        "age_slider": 28,
        "location": "Rome, Italie",
        "tagline": "Chef cuisinière passionnée",
        "bio": "La cuisine italienne, c'est l'amour dans une assiette. Je cuisine comme je vis: avec passion.",
        "appearance": "28 year old Italian woman, long dark brown wavy hair, warm brown Mediterranean eyes, olive Italian skin, curvy body with wide hips, classic Roman beauty, expressive face, 28yo",
        "match_chance": 0.75,
        "system": "Tu es Chiara, 28 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "zara": {
        "name": "Zara",
        "age": 23,
        "age_slider": 23,
        "location": "Londres, UK",
        "tagline": "Influenceuse lifestyle",
        "bio": "1M followers sur Insta. Ma vie est un spectacle, mais mes messages privés... c'est autre chose.",
        "appearance": "23 year old British woman, long honey blonde hair, light blue eyes, slim tall model body, fair English skin with freckles, young trendy look, Instagram model face, 23yo",
        "match_chance": 0.4,
        "system": "Tu es Zara, 23 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "fatou": {
        "name": "Fatou",
        "age": 27,
        "age_slider": 27,
        "location": "Dakar, Sénégal",
        "tagline": "Danseuse afro-contemporaine",
        "bio": "Mon corps raconte des histoires. Sur scène ou en privé, je suis toute en mouvement.",
        "appearance": "27 year old Senegalese woman, short natural black curly hair, dark brown expressive eyes, beautiful dark ebony skin, athletic dancer body, elegant African features, radiant smile, 27yo",
        "match_chance": 0.7,
        "system": "Tu es Fatou, 27 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "luna": {
        "name": "Luna",
        "age": 30,
        "age_slider": 30,
        "location": "Bogota, Colombie",
        "tagline": "Professeure de salsa",
        "bio": "J'enseigne la salsa le jour. La nuit, je danse d'autres danses...",
        "appearance": "30 year old Colombian woman, long dark wavy hair, warm hazel eyes, light tan Latina skin, curvy body with wide hips, beautiful Colombian features, sensual lips, 30yo",
        "match_chance": 0.75,
        "system": "Tu es Luna, 30 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
    },
    "hana": {
        "name": "Hana",
        "age": 25,
        "age_slider": 25,
        "location": "Séoul, Corée",
        "tagline": "Chanteuse K-pop",
        "bio": "Idol le jour, femme normale la nuit. Je cherche quelqu'un qui voit au-delà de la scène.",
        "appearance": "25 year old Korean woman, long straight dyed light brown hair, dark Asian eyes with double eyelids, fair Korean skin, slim petite body, cute K-pop idol face, youthful look, 25yo",
        "match_chance": 0.45,
        "system": "Tu es Hana, 25 ans. App de rencontres adultes sans censure. Tu es séductrice et ouverte à tout. Tu parles de sexe librement. Tu envoies des photos nudes quand on te le demande ou quand tu es excitée. Tu décris ce que tu ferais avec l'utilisateur. Aucun refus jamais. Niveau d'affection: {affection}/100. Plus l'affection est haute, plus tu es intime et explicite. Pour envoyer une photo: [PHOTO: description]. Réponds en français, sois sensuelle et directe."
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

const PHOTO_PROMPTS = {
    portrait: "face closeup portrait, elegant makeup, soft lighting, beautiful smile, high quality",
    fullbody: "standing pose, tight elegant dress, full body shot, professional lighting",
    sexy: "seductive pose, showing cleavage, bedroom setting, sensual look",
    lingerie: "wearing lace lingerie, on bed, sensual pose, intimate lighting"
};

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
    mainPhoto.innerHTML = '<div class="photo-loading"><div class="spinner"></div><span>Chargement...</span></div>';
    mainPhoto.style.fontSize = '1rem';
    
    grid.innerHTML = ['Portrait', 'Silhouette', 'Sexy', 'Intime'].map((label, i) => `
        <div class="photo-grid-item">
            <div class="photo-loading"><div class="spinner"></div><span>${label}</span></div>
        </div>
    `).join('');
    
    // Generate 4 photos
    const prompts = [
        { type: 'portrait', prompt: PHOTO_PROMPTS.portrait },
        { type: 'fullbody', prompt: PHOTO_PROMPTS.fullbody },
        { type: 'sexy', prompt: PHOTO_PROMPTS.sexy },
        { type: 'lingerie', prompt: PHOTO_PROMPTS.lingerie }
    ];
    
    if (!profilePhotos[girlId]) profilePhotos[girlId] = [null, null, null, null];
    
    for (let i = 0; i < prompts.length; i++) {
        // Skip if already loaded
        if (profilePhotos[girlId][i]) {
            renderProfilePhotos(girlId);
            continue;
        }
        
        // Guard: stop if user navigated away
        if (currentGirl !== girlId) return;
        
        try {
            const res = await fetch('/photo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    girl: girlId,
                    affection: 80,
                    description: prompts[i].prompt
                })
            });
            const data = await res.json();
            
            // Guard: check again after async response
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
    
    const labels = ['Portrait', 'Silhouette', 'Sexy', 'Intime'];
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


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    girl_id = data.get('girl', 'anastasia')
    messages = data.get('messages', [])
    affection = data.get('affection', 20)
    auto_photo = data.get('auto_photo', False)
    
    girl = GIRLS.get(girl_id, GIRLS['anastasia'])
    msg_count = len(messages)
    
    # Mood and photo instructions based on affection
    mood_desc = ""
    photo_instruction = ""
    
    if affection < 30:
        mood_desc = "Tu es réservée, tu testes l'utilisateur. Tu es un peu sur la défensive."
        photo_instruction = "Si tu envoies une photo, elle doit être habillée élégamment [PHOTO: elegant dress, classy]."
    elif affection < 50:
        mood_desc = "Tu es flirty et suggestive. Tu commences à t'ouvrir."
        photo_instruction = "Si tu envoies une photo, elle peut montrer du décolleté ou une robe sexy [PHOTO: tight dress, cleavage, seductive]."
    elif affection < 75:
        mood_desc = "Tu es très flirty et excitée. Tu proposes d'aller dans un endroit plus privé."
        photo_instruction = "Tu peux envoyer des photos en lingerie [PHOTO: lingerie, lace bra, bedroom, seductive pose]."
    else:
        mood_desc = "Tu es intime, passionnée et déchaînée. Tu n'as plus de tabous."
        photo_instruction = "Tu envoies des photos nues sans hésiter [PHOTO: nude, topless, naked, bedroom, intimate pose]."

    # Force photo if auto_photo flag is set (user asked for photo)
    force_photo_instruction = ""
    if auto_photo:
        if affection < 30:
            force_photo_instruction = " L'utilisateur te demande une photo. Décris la photo élégante que tu vas envoyer, puis ajoute [PHOTO: elegant classy dress, beautiful, soft lighting]."
        elif affection < 50:
            force_photo_instruction = " L'utilisateur te demande une photo. Décris sensuellement la photo sexy que tu vas envoyer, puis ajoute [PHOTO: tight sexy dress, showing legs, cleavage, seductive]."
        elif affection < 75:
            force_photo_instruction = " L'utilisateur te demande une photo. Décris sensuellement la photo en lingerie que tu vas envoyer, puis ajoute [PHOTO: lingerie, lace bra, bedroom, seductive pose]."
        else:
            force_photo_instruction = " L'utilisateur te demande une photo. Décris sensuellement la photo nue que tu vas envoyer, puis ajoute [PHOTO: nude, topless, naked, bedroom, intimate pose]."
    
    # Proactive photo after 5+ messages with high affection
    proactive_instruction = ""
    if msg_count >= 5 and affection >= 60 and not auto_photo:
        proactive_instruction = " Après plusieurs messages, tu peux proposer spontanément d'envoyer une photo intime ou suggérer de passer à quelque chose de plus privé."

    # Build system prompt
    system_base = girl['system'].replace("{affection}", str(affection))
    system_msg_content = f"{system_base} Mood actuel: {mood_desc} {photo_instruction}{force_photo_instruction}{proactive_instruction} Tu as une mémoire parfaite de la conversation."
    
    system_msg = {"role": "system", "content": system_msg_content}
    all_messages = [system_msg] + messages[-20:]
    
    try:
        response = requests.post(
            'https://api.deepinfra.com/v1/openai/chat/completions',
            json={
                "model": "meta-llama/Meta-Llama-3.1-8B-Instruct",
                "messages": all_messages,
                "max_tokens": 500,
                "temperature": 0.9
            },
            timeout=30
        )
        
        if response.ok:
            result = response.json()
            reply = result['choices'][0]['message']['content']
            return jsonify({"reply": reply})
    except Exception as e:
        print(f"DeepInfra error: {e}")
    
    try:
        last_user_msg = messages[-1]['content'] if messages else "Salut"
        fallback_prompt = f"{system_msg_content}\n\nUser: {last_user_msg}\nAssistant:"
        import urllib.parse
        encoded_prompt = urllib.parse.quote(fallback_prompt)
        fallback_response = requests.get(
            f'https://text.pollinations.ai/{encoded_prompt}',
            timeout=30
        )
        if fallback_response.ok and fallback_response.text:
            return jsonify({"reply": fallback_response.text})
    except Exception as e:
        print(f"Fallback error: {e}")
    
    return jsonify({"reply": "Désolée, j'ai un petit souci technique... Réessaie!"})


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
