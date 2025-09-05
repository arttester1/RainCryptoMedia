from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters
import sqlite3
import logging
from data.config import DEPOSIT_AMOUNTS
from services.nowpayments import NowPaymentsAPI
from keyboards.inline import deposit_keyboard, main_menu_keyboard

logger = logging.getLogger(__name__)

# Conversation states
SELECTING_AMOUNT, CONFIRMING_DEPOSIT = range(2)

async def add_funds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Initiate deposit process"""
    keyboard = deposit_keyboard()
    await update.message.reply_text(
        "💵 Select deposit amount:",
        reply_markup=keyboard
    )
    return SELECTING_AMOUNT

async def deposit_amount_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle deposit amount selection"""
    query = update.callback_query
    await query.answer()
    
    amount = float(query.data.replace('deposit_', ''))
    context.user_data['deposit_amount'] = amount
    
    # Store the selected amount in user data to prevent changes
    user_id = query.from_user.id
    context.user_data[f'deposit_{user_id}'] = amount
    
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Confirm", callback_data=f"confirm_deposit_{amount}")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_deposit")]
    ])
    
    await query.edit_message_text(
        f"💳 You selected: ${amount}\n\n"
        "Please confirm to proceed with payment:",
        reply_markup=keyboard
    )
    return CONFIRMING_DEPOSIT

async def confirm_deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create NowPayments invoice"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    amount = context.user_data.get(f'deposit_{user_id}')
    
    if not amount:
        await query.edit_message_text("❌ Session expired. Please start over.")
        return ConversationHandler.END
    
    # Create payment with NowPayments
    nowpayments = NowPaymentsAPI()
    payment = nowpayments.create_payment(amount, user_id, f"dep_{user_id}")
    
    if payment and 'payment_url' in payment:
        # Save payment info to database
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO deposits (user_id, amount, payment_id, status)
            VALUES (?, ?, ?, 'pending')
        ''', (user_id, amount, payment.get('payment_id')))
        conn.commit()
        conn.close()
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💰 Pay Now", url=payment['payment_url'])],
            [InlineKeyboardButton("✅ Check Payment", callback_data=f"check_deposit_{payment['payment_id']}")]
        ])
        
        await query.edit_message_text(
            f"✅ Payment created!\n\n"
            f"Amount: ${amount}\n"
            f"Payment ID: {payment['payment_id']}\n\n"
            "Click the button below to complete your payment:",
            reply_markup=keyboard
        )
    else:
        await query.edit_message_text("❌ Failed to create payment. Please try again.")
    
    return ConversationHandler.END

async def check_deposit_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check deposit payment status"""
    query = update.callback_query
    await query.answer()
    
    payment_id = query.data.replace('check_deposit_', '')
    nowpayments = NowPaymentsAPI()
    status = nowpayments.get_payment_status(payment_id)
    
    if status and status.get('payment_status') == 'finished':
        # Update database and add funds to user balance
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT user_id, amount FROM deposits WHERE payment_id = ?', (payment_id,))
        deposit = cursor.fetchone()
        
        if deposit:
            user_id, amount = deposit
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
            cursor.execute('UPDATE deposits SET status = ? WHERE payment_id = ?', ('completed', payment_id))
            conn.commit()
            
            await query.edit_message_text(
                f"✅ Payment completed!\n"
                f"${amount} has been added to your balance."
            )
        conn.close()
    else:
        await query.edit_message_text("⏳ Payment still processing or failed. Please try again later.")