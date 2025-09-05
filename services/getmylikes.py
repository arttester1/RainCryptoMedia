import requests
import logging
from data.config import GETMYLIKES_API_KEY, GETMYLIKES_API_URL

logger = logging.getLogger(__name__)

class GetMyLikesAPI:
    def __init__(self):
        self.api_key = GETMYLIKES_API_KEY
        self.base_url = GETMYLIKES_API_URL
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
    
    def get_services(self):
        """Get all available services with 50% markup"""
        try:
            response = requests.get(f"{self.base_url}/services", headers=self.headers, timeout=10)
            response.raise_for_status()
            services = response.json()
            
            # Apply 50% markup
            for service in services:
                original_price = float(service.get('rate', 0))
                service['original_rate'] = original_price
                service['rate'] = round(original_price * 1.5, 2)  # 50% markup
            
            return services
        except Exception as e:
            logger.error(f"Error fetching services: {e}")
            return None
    
    def create_order(self, service_id, quantity, link):
        """Create new order"""
        payload = {
            "service": service_id,
            "quantity": quantity,
            "link": link
        }
        
        try:
            response = requests.post(f"{self.base_url}/order", json=payload, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            return None
    
    def get_order_status(self, order_id):
        """Check order status"""
        try:
            response = requests.get(f"{self.base_url}/order/{order_id}", headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error checking order status: {e}")
            return None