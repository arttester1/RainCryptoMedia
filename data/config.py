from dotenv import load_dotenv
from pathlib import Path
import os

# Force load from the correct absolute path
env_path = Path(__file__).resolve().parent.parent / ".env"
print("🔍 Forcing .env load from:", env_path)
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env", override=True)

print("🔍 DEBUG inside config.py:")
print("BOT_TOKEN =", os.getenv("BOT_TOKEN"))
print("ADMINS =", os.getenv("ADMINS"))


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