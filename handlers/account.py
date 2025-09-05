from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import sqlite3

async def my_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user account information"""
    user_id = update.effective_user.id
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Get user balance and referral info
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE referred_by = ?', (user_id,))
    referrals_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(amount) FROM referrals WHERE referrer_id = ?', (user_id,))
    referral_earnings = cursor.fetchone()[0] or 0
    
    conn.close()
    
    balance = user[0] if user else 0
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("👥 My Referrals", callback_data="my_referrals")],
        [InlineKeyboardButton("💵 Add Funds", callback_data="add_funds")],
        [InlineKeyboardButton("📊 Statistics", callback_data="stats")],
        [InlineKeyboardButton("🔙 Back to Main", callback_data="main_menu")]
    ])
    
    await update.message.reply_text(
        f"👤 Your Account\n\n"
        f"💰 Balance: ${balance:.2f}\n"
        f"👥 Referrals: {referrals_count}\n"
        f"🎯 Referral Earnings: ${referral_earnings:.2f}\n\n"
        "Manage your account:",
        reply_markup=keyboard
    )

async def my_referrals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show referral information"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    
    # Get referral link
    cursor.execute('SELECT referral_code FROM users WHERE user_id = ?', (user_id,))
    referral_code = cursor.fetchone()[0]
    
    referral_link = f"https://t.me/your_bot?start={referral_code}"
    
    # Get referral stats
    cursor.execute('SELECT COUNT(*) FROM users WHERE referred_by = ?', (user_id,))
    referrals_count = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(amount) FROM referrals WHERE referrer_id = ?', (user_id,))
    referral_earnings = cursor.fetchone()[0] or 0
    
    conn.close()
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Account", callback_data="my_account")]
    ])
    
    await query.edit_message_text(
        f"👥 Your Referral Program\n\n"
        f"🔗 Your referral link:\n{referral_link}\n\n"
        f"📊 Statistics:\n"
        f"• Total referrals: {referrals_count}\n"
        f"• Total earnings: ${referral_earnings:.2f}\n\n"
        f"Earn 10% of every deposit your referrals make!",
        reply_markup=keyboard
    )