import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler

# Import your config
try:
    from data.config import BOT_TOKEN
except ImportError:
    print("Error: Could not import BOT_TOKEN from data.config")
    print("Please make sure your .env file is set up correctly")
    exit(1)

# Import handlers (we'll handle missing ones gracefully)
start_handler = None
help_handler = None

try:
    from handlers.start import start_handler, help_handler
except ImportError:
    print("Warning: handlers.start module not found")

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add basic command handlers
    if start_handler:
        application.add_handler(CommandHandler("start", start_handler))
    else:
        # Fallback start handler
        async def fallback_start(update, context):
            await update.message.reply_text("Welcome! The bot is starting up...")
        application.add_handler(CommandHandler("start", fallback_start))

    if help_handler:
        application.add_handler(CommandHandler("help", help_handler))
    else:
        # Fallback help handler
        async def fallback_help(update, context):
            await update.message.reply_text("Help command not configured yet.")
        application.add_handler(CommandHandler("help", fallback_help))

    # Start the bot
    print("Starting bot...")
    application.run_polling()

if __name__ == "__main__":
    main()