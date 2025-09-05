import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMINS = [int(os.getenv('ADMINS'))] if os.getenv('ADMINS') else []

# GetMyLikes API
GETMYLIKES_API_KEY = os.getenv('GETMYLIKES_API_KEY')
GETMYLIKES_API_URL = 'https://getmylikes.com/api/v2'

# NowPayments API
NOWPAYMENTS_API_KEY = os.getenv('NOWPAYMENTS_API_KEY')
NOWPAYMENTS_API_URL = 'https://api.nowpayments.io/v1'

# Markup configuration
MARKUP_PERCENTAGE = 0.5  # 50% markup

# Preset deposit amounts
DEPOSIT_AMOUNTS = [25, 50, 100]

# Database configuration (SQLite for simplicity)
DB_FILE = 'database.db'

# Referral settings
REFERRAL_PERCENTAGE = 0.1  # 10% referral bonus