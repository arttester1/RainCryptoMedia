from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from data.config import DEPOSIT_AMOUNTS

def main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Bot Services", callback_data="bot_services")],
        [InlineKeyboardButton("🛍️ Order Services", callback_data="show_services")],
        [InlineKeyboardButton("💵 Add Funds", callback_data="add_funds")],
        [InlineKeyboardButton("👤 My Account", callback_data="my_account")],
        [InlineKeyboardButton("👥 Referral Program", callback_data="referral_info")]
    ]
    return InlineKeyboardMarkup(keyboard)

def deposit_keyboard():
    keyboard = []
    for amount in DEPOSIT_AMOUNTS:
        keyboard.append([InlineKeyboardButton(f"${amount}", callback_data=f"deposit_{amount}")])
    keyboard.append([InlineKeyboardButton("🔙 Back", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)