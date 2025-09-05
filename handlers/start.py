from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3
import secrets

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    # Connect to database
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Check if user exists
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    existing_user = cursor.fetchone()

    if not existing_user:
        # Generate referral code
        referral_code = secrets.token_hex(4).upper()

        # Check if referral parameter exists
        referred_by = None
        if context.args and len(context.args) > 0:
            ref_code = context.args[0]
            cursor.execute('SELECT user_id FROM users WHERE referral_code = ?', (ref_code,))
            referrer = cursor.fetchone()
            if referrer:
                referred_by = referrer[0]

        # Create new user
        cursor.execute('''
            INSERT INTO users (user_id, username, first_name, last_name, referral_code, referred_by)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, user.username, user.first_name, user.last_name, referral_code, referred_by))

        conn.commit()

    conn.close()

    # Send welcome message
    await update.message.reply_text(
        "👋 Welcome to RainBooster SMM Services!\n\n"
        "We provide high-quality social media marketing services.\n"
        "Use /help to see available commands."
    )

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message\n"
        "/myaccount - View your account"
    )