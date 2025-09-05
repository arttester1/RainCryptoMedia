from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
from services.getmylikes import GetMyLikesAPI
import logging

logger = logging.getLogger(__name__)

# Conversation states
SELECT_SERVICE, ENTER_LINK, ENTER_QUANTITY, CONFIRM_ORDER = range(4)

async def show_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show available services with categories"""
    smm_api = GetMyLikesAPI()
    services = smm_api.get_services()
    
    if not services:
        await update.message.reply_text("❌ Unable to load services. Please try again later.")
        return
    
    # Group services by category
    categories = {}
    for service in services:
        category = service.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(service)
    
    # Create category keyboard
    keyboard = []
    for category in categories.keys():
        keyboard.append([InlineKeyboardButton(category, callback_data=f"category_{category}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Main Menu", callback_data="main_menu")])
    
    await update.message.reply_text(
        "📊 Available Services\n\n"
        "Select a category:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_category_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show services in selected category"""
    query = update.callback_query
    await query.answer()
    
    category = query.data.replace('category_', '')
    smm_api = GetMyLikesAPI()
    services = smm_api.get_services()
    
    if not services:
        await query.edit_message_text("❌ Unable to load services. Please try again later.")
        return
    
    category_services = [s for s in services if s.get('category') == category]
    
    keyboard = []
    for service in category_services[:10]:  # Limit to 10 services per page
        btn_text = f"{service['name']} - ${service['rate']}/1000"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"service_{service['id']}")])
    
    keyboard.append([InlineKeyboardButton("🔙 Back to Categories", callback_data="back_categories")])
    
    await query.edit_message_text(
        f"📊 {category} Services\n\n"
        "Select a service:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )