import os
import logging
import requests
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. Chargement des variables d'environnement
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

# Validation des clés
if not TELEGRAM_TOKEN or not MAKE_WEBHOOK_URL:
    raise ValueError("Les variables d'environnement TELEGRAM_TOKEN ou MAKE_WEBHOOK_URL sont manquantes.")

# 2. Configuration du Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 3. Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Répond au message /start.
    """
    user = update.effective_user
    logger.info(f"Commande /start reçue de {user.first_name} (ID: {user.id})")
    await update.message.reply_text(
        "Salutations. Je suis Pip. Connecté au flux. Quel sujet dois-je analyser ?"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Gère les messages texte, loggue l'activité et transmet à Make.com.
    """
    user = update.effective_user
    message_text = update.message.text
    timestamp = datetime.now().isoformat()
    
    logger.info(f"Message reçu de {user.first_name} (ID: {user.id}) : {message_text}")

    # Préparation du payload
    payload = {
        "topic": message_text,
        "user_id": user.id,
        "timestamp": timestamp
    }

    try:
        # Envoi synchrone via requests (Note: Dans un environnement à très fort trafic, privilégier aiohttp/httpx)
        response = requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=10)
        
        if response.status_code == 200:
            logger.info("Transmission réussie au Webhook Make.")
            await update.message.reply_text(f"Transmission du sujet '{message_text}' au Core pour traitement...")
        else:
            logger.error(f"Erreur Webhook Make: {response.status_code} - {response.text}")
            await update.message.reply_text("Erreur de liaison uplink (Code non-200 reçu du Core).")

    except requests.exceptions.RequestException as e:
        logger.error(f"Exception lors de la connexion à Make: {e}")
        await update.message.reply_text("Erreur de liaison uplink (Échec de connexion).")

# 4. Initialisation du Bot
if __name__ == '__main__':
    if not TELEGRAM_TOKEN:
        logger.critical("Token Telegram introuvable !")
        exit(1)
        
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    logger.info("Pip est en ligne et écoute le flux...")
    application.run_polling()
