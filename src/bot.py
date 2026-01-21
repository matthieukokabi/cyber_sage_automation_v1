import os
import logging
import requests
import asyncio
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# 1. Chargement des variables d'environnement
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validation des clés
if not TELEGRAM_TOKEN or not MAKE_WEBHOOK_URL or not GEMINI_API_KEY:
    raise ValueError("Les variables d'environnement TELEGRAM_TOKEN, MAKE_WEBHOOK_URL ou GEMINI_API_KEY sont manquantes.")

# Configuration Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. Configuration du Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 3. Fonctions IA
async def generate_content_with_gemini(topic):
    """
    Utilise Gemini pour générer un script et un prompt visuel basés sur le sujet.
    """
    prompt = f"""
    Tu es un expert en création de contenu viral pour YouTube Shorts (Style Cyberpunk/Futuriste).
    Sujet: "{topic}"
    
    Tâche:
    1. Génère un script de narration captivant (max 60 secondes, environ 130-150 mots). Ton: Mystérieux, Tech, Visionnaire.
    2. Génère un prompt visuel détaillé pour Midjourney/Flux décrivant l'ambiance générale de la vidéo.
    
    Réponds UNIQUEMENT au format JSON suivant:
    {{
        "script": "Le texte de la narration ici...",
        "visual_prompt": "Description visuelle détaillée, cyberpunk style, neon lights, high tech..."
    }}
    """
    
    try:
        response = await asyncio.to_thread(model.generate_content, prompt)
        # Nettoyage basique si Gemini renvoie des backticks markdown
        text_response = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(text_response)
    except Exception as e:
        logger.error(f"Erreur Gemini: {e}")
        return None

# 4. Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Répond au message /start.
    """
    user = update.effective_user
    logger.info(f"Commande /start reçue de {user.first_name} (ID: {user.id})")
    await update.message.reply_text(
        "Salutations. Je suis Pip v2 (Gemini-Powered). Connecté au flux. Quel sujet dois-je analyser ?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère les messages, génère le contenu via Gemini, et transmet à Make.com.
    """
    user = update.effective_user
    message_text = update.message.text
    timestamp = datetime.now().isoformat()
    
    logger.info(f"Message reçu de {user.first_name} (ID: {user.id}) : {message_text}")
    
    await update.message.reply_text("🧠 Analyse neuronale en cours (Gemini)...")

    # Génération IA
    ai_content = await generate_content_with_gemini(message_text)
    
    if not ai_content:
        await update.message.reply_text("⚠️ Erreur : Mes circuits neuronaux (Gemini) n'ont pas pu traiter la demande.")
        return

    # Payload enrichi
    payload = {
        "topic": message_text,
        "script": ai_content.get("script"),
        "visual_prompt": ai_content.get("visual_prompt"),
        "user_id": user.id,
        "timestamp": timestamp,
        "settings": {
            "style": "Cinematic Cyberpunk",
            "duration": "60s",
            "platform": "YouTube Shorts",
            "narrative_mode": "Storytelling"
        }
    }

    try:
        # Envoi synchrone via requests
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=30) # Timeout augmenté pour Make
        
        if response.status_code == 200:
            logger.info("Transmission réussie au Webhook Make.")
            await update.message.reply_text(
                f"✅ **Analyse Terminée**\n\n"
                f"📜 **Script Généré**:\n_{ai_content.get('script')[:100]}..._\n\n"
                f"🎨 **Prompt Visuel**:\n_{ai_content.get('visual_prompt')[:100]}..._\n\n"
                f"🚀 Transmission au Core pour production vidéo."
            )
        else:
            logger.error(f"Erreur Webhook Make: {response.status_code} - {response.text}")
            await update.message.reply_text(f"⚠️ Erreur de liaison uplink : {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Exception lors de la connexion à Make: {e}")
        await update.message.reply_text(f"🛑 Erreur critique: {e}")

# 5. Initialisation du Bot
if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        logger.critical("Token Telegram introuvable !")
        exit(1)
        
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    logger.info("Pip v2 (Gemini-Core) est en ligne...")
    application.run_polling()
