from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from keyboards.inline import main_menu_keyboard, deposit_keyboard
import sqlite3

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    try:
        if data == "bot_services":
            await query.edit_message_text(
                "🤖 Bot Services\n\n"
                "Here are our available bots:\n\n"
                "• @YourFirstBot - Description\n"
                "• @YourSecondBot - Description\n"
                "• @YourThirdBot - Description\n\n"
                "Click the usernames to open them!",
                reply_markup=main_menu_keyboard(),
                disable_web_page_preview=True
            )
        
        elif data == "show_services":
            # This should integrate with GetMyLikes API
            try:
                from services.getmylikes import GetMyLikesAPI
                smm_api = GetMyLikesAPI()
                services = smm_api.get_services()
                
                if services:
                    service_list = "\n".join([f"• {s['name']} - ${s['rate']}" for s in services[:5]])
                    await query.edit_message_text(
                        f"🛍️ Available Services\n\n{service_list}\n\n"
                        "Use /order to place an order",
                        reply_markup=main_menu_keyboard()
                    )
                else:
                    await query.edit_message_text(
                        "❌ Unable to load services. Please try again later.",
                        reply_markup=main_menu_keyboard()
                    )
            except ImportError:
                await query.edit_message_text(
                    "🛍️ Order Services\n\n"
                    "Service catalog integration coming soon...",
                    reply_markup=main_menu_keyboard()
                )
        
        elif data == "add_funds":
            keyboard = deposit_keyboard()
            await query.edit_message_text(
                "💵 Add Funds\n\n"
                "Select deposit amount:\n"
                "• $25 - Basic package\n"
                "• $50 - Standard package\n"
                "• $100 - Premium package",
                reply_markup=keyboard
            )
        
        elif data.startswith("deposit_"):
            amount = data.replace("deposit_", "")
            # This should integrate with NowPayments API
            try:
                from services.nowpayments import NowPaymentsAPI
                payments_api = NowPaymentsAPI()
                # payment = payments_api.create_payment(amount, user_id, ...)
                
                await query.edit_message_text(
                    f"💳 Deposit ${amount}\n\n"
                    f"Payment gateway: NowPayments.io\n"
                    f"Amount: ${amount} USD\n\n"
                    "Please send the exact amount to:\n"
                    "Crypto address will be shown here\n\n"
                    "⏰ Payment expires in 30 minutes",
                    reply_markup=main_menu_keyboard()
                )
            except ImportError:
                await query.edit_message_text(
                    f"💳 Deposit ${amount}\n\n"
                    "NowPayments integration coming soon...\n"
                    "You can manually deposit to our wallet.",
                    reply_markup=main_menu_keyboard()
                )
        
        elif data == "my_account":
            user_id = query.from_user.id
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            balance = user[0] if user else 0.0
            conn.close()
            
            await query.edit_message_text(
                f"👤 My Account\n\n💰 Balance: ${balance}",
                reply_markup=main_menu_keyboard()
            )
        
        elif data == "referral_info":
            user_id = query.from_user.id
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            
            # Get referral code
            cursor.execute('SELECT referral_code FROM users WHERE user_id = ?', (user_id,))
            referral_code = cursor.fetchone()[0]
            referral_link = f"https://t.me/your_bot_username?start={referral_code}"
            
            # Get referral stats
            cursor.execute('SELECT COUNT(*) FROM users WHERE referred_by = ?', (user_id,))
            referral_count = cursor.fetchone()[0]
            
            cursor.execute('SELECT SUM(amount) FROM referrals WHERE referrer_id = ?', (user_id,))
            referral_earnings = cursor.fetchone()[0] or 0
            
            conn.close()
            
            await query.edit_message_text(
                f"👥 Referral Program\n\n"
                f"🔗 Your referral link:\n{referral_link}\n\n"
                f"📊 Stats:\n"
                f"• Referrals: {referral_count}\n"
                f"• Earnings: ${referral_earnings}\n\n"
                f"Earn 10% of every deposit your referrals make!",
                reply_markup=main_menu_keyboard()
            )
        
        elif data == "main_menu":
            await query.edit_message_text(
                "👋 Welcome back!\nChoose an option:",
                reply_markup=main_menu_keyboard()
            )
    
    except Exception as e:
        print(f"Error handling callback: {e}")
        # Fallback: send a new message instead of editing
        await query.message.reply_text(
            "Something went wrong. Please try again.",
            reply_markup=main_menu_keyboard()
        )