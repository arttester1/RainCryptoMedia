import requests
import logging
from data.config import NOWPAYMENTS_API_KEY, NOWPAYMENTS_API_URL

logger = logging.getLogger(__name__)

class NowPaymentsAPI:
    def __init__(self):
        self.api_key = NOWPAYMENTS_API_KEY
        self.base_url = NOWPAYMENTS_API_URL
        self.headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def create_invoice(self, amount, order_id, user_id):
        """Create payment invoice"""
        payload = {
            "price_amount": amount,
            "price_currency": "usd",
            "order_id": f"smm_{order_id}_{user_id}",
            "order_description": f"SMM Services Order #{order_id}",
            "ipn_callback_url": "https://your-domain.com/nowpayments-webhook",
            "success_url": "https://t.me/your_bot?start=success",
            "cancel_url": "https://t.me/your_bot?start=cancel"
        }
        
        try:
            response = requests.post(f"{self.base_url}/invoice", json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating invoice: {e}")
            return None
    
    def get_payment_status(self, payment_id):
        """Check payment status"""
        try:
            response = requests.get(f"{self.base_url}/payment/{payment_id}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error checking payment status: {e}")
            return None
    
    def create_payment(self, amount, user_id, deposit_id):
        """Create direct payment"""
        payload = {
            "price_amount": amount,
            "price_currency": "usd",
            "pay_currency": "usdt",  # Can be changed based on user selection
            "order_id": f"deposit_{deposit_id}_{user_id}",
            "order_description": f"Deposit #{deposit_id}",
            "ipn_callback_url": "https://your-domain.com/nowpayments-webhook"
        }
        
        try:
            response = requests.post(f"{self.base_url}/payment", json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating payment: {e}")
            return None