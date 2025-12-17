"""
WhatsApp Business API Service for Jewelry Shop Dashboard
Handles message sending, receiving, and campaign management
"""

import requests
import json
import streamlit as st
from datetime import datetime
from typing import List, Dict, Optional
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WhatsAppService:
    def __init__(self, api_token: str, phone_id: str, business_account_id: str):
        """Initialize WhatsApp Business API service"""
        self.api_token = api_token
        self.phone_id = phone_id
        self.business_account_id = business_account_id
        self.api_url = f"https://graph.instagram.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def validate_phone_number(self, phone: str) -> bool:
        """Validate Indian phone number format"""
        import re
        # Accept formats: +919876543210, 919876543210, 9876543210
        pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
        phone_clean = phone.replace("-", "").replace(" ", "")
        return bool(re.match(pattern, phone_clean))
    
    def format_phone_number(self, phone: str) -> str:
        """Convert phone number to WhatsApp format (91xxxxxxxxxx)"""
        phone_clean = phone.replace("+", "").replace("-", "").replace(" ", "")
        if not phone_clean.startswith("91") and len(phone_clean) == 10:
            phone_clean = "91" + phone_clean
        elif phone_clean.startswith("0"):
            phone_clean = "91" + phone_clean[1:]
        return phone_clean
    
    def send_text_message(self, to_phone: str, message: str) -> Dict:
        """Send text message via WhatsApp"""
        
        if not self.validate_phone_number(to_phone):
            return {
                "success": False,
                "error": f"Invalid phone number format: {to_phone}",
                "timestamp": datetime.now().isoformat()
            }
        
        phone_number = self.format_phone_number(to_phone)
        
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number,
            "type": "text",
            "text": {
                "preview_url": True,
                "body": message
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_id}/messages",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Message sent successfully to {phone_number}")
                return {
                    "success": True,
                    "message_id": result.get("messages", [{}])[0].get("id"),
                    "phone": phone_number,
                    "timestamp": datetime.now().isoformat()
                }
            else:
                error_data = response.json()
                logger.error(f"Failed to send message: {error_data}")
                return {
                    "success": False,
                    "error": error_data.get("error", {}).get("message", "Unknown error"),
                    "phone": phone_number,
                    "timestamp": datetime.now().isoformat()
                }
        
        except Exception as e:
            logger.error(f"Exception sending message: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "phone": phone_number,
                "timestamp": datetime.now().isoformat()
            }
    
    def send_template_message(self, to_phone: str, template_name: str, parameters: List[str]) -> Dict:
        """Send pre-approved template message"""
        
        if not self.validate_phone_number(to_phone):
            return {"success": False, "error": "Invalid phone number"}
        
        phone_number = self.format_phone_number(to_phone)
        
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "template",
            "template": {
                "name": template_name,
                "language": {
                    "code": "en_US"
                },
                "components": [
                    {
                        "type": "body",
                        "parameters": [{"type": "text", "text": param} for param in parameters]
                    }
                ]
            }
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_id}/messages",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Template message sent"}
            else:
                return {"success": False, "error": response.json()}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def send_bulk_messages(self, phone_list: List[str], message: str, delay: int = 1) -> List[Dict]:
        """Send bulk messages with rate limiting"""
        
        import time
        results = []
        
        for phone in phone_list:
            result = self.send_text_message(phone, message)
            results.append(result)
            
            # Rate limiting (delay between messages)
            if delay > 0:
                time.sleep(delay)
        
        return results
    
    def send_order_confirmation(self, customer_data: Dict) -> Dict:
        """Send order confirmation message"""
        
        message = f"""🎉 Order Confirmed!

Hi {customer_data.get('name', 'Valued Customer')},

Your jewelry order has been confirmed!

Order Details:
📦 Item: {customer_data.get('item', 'Your Order')}
💰 Amount: ₹{customer_data.get('amount', 0):,}
📅 Order ID: {customer_data.get('order_id', 'N/A')}

Expected Delivery: {customer_data.get('expected_delivery', '3-5 business days')}

Thank you for shopping with us! 💎"""
        
        return self.send_text_message(customer_data['phone'], message)
    
    def send_payment_reminder(self, customer_data: Dict) -> Dict:
        """Send payment reminder"""
        
        message = f"""💳 Payment Reminder

Hi {customer_data.get('name', 'Valued Customer')},

This is a friendly reminder for your pending payment.

Details:
💰 Amount Due: ₹{customer_data.get('pending_amount', 0):,}
📝 Item: {customer_data.get('item', 'Your Order')}
📅 Due Date: {customer_data.get('due_date', 'ASAP')}

Please make the payment at your earliest convenience.

Thank you! 🙏"""
        
        return self.send_text_message(customer_data['phone'], message)
    
    def send_delivery_update(self, customer_data: Dict) -> Dict:
        """Send delivery status update"""
        
        message = f"""📦 Delivery Update

Hi {customer_data.get('name', 'Valued Customer')},

Your order is on the way! 🚚

Order Details:
🏷️ Order ID: {customer_data.get('order_id', 'N/A')}
📍 Current Status: {customer_data.get('status', 'In Transit')}
📅 Expected Delivery: {customer_data.get('expected_delivery', 'Tomorrow')}

Tracking: {customer_data.get('tracking_link', 'Contact us for details')}

We're excited for you to receive your beautiful jewelry! 💎"""
        
        return self.send_text_message(customer_data['phone'], message)
    
    def send_promotional_offer(self, customer_data: Dict, campaign_data: Dict) -> Dict:
        """Send promotional campaign message"""
        
        message = f"""✨ Special Offer Just For You! ✨

Hi {customer_data.get('name', 'Valued Customer')},

{campaign_data.get('title', 'Exciting Offer')}

🎁 Get {campaign_data.get('discount', 'Special Discount')}
📝 {campaign_data.get('description', 'On selected items')}

✅ Valid Till: {campaign_data.get('valid_till', 'Limited Time')}

Don't miss out! Visit us today or reply for more details.

Shop Now: {campaign_data.get('link', 'www.jewelshop.com')} 💎"""
        
        return self.send_text_message(customer_data['phone'], message)
    
    def send_loyalty_reward(self, customer_data: Dict, points: int, reward_details: str) -> Dict:
        """Send loyalty reward notification"""
        
        message = f"""🎉 Loyalty Reward Earned! 🎉

Hi {customer_data.get('name', 'Valued Customer')},

You've earned {points} loyalty points on your recent purchase!

🌟 Your Total Points: {customer_data.get('total_points', 0)}
🎁 Reward: {reward_details}

Redeem your points at your next purchase!

Thank you for being our valued customer! 💎"""
        
        return self.send_text_message(customer_data['phone'], message)
    
    def setup_webhook(self, webhook_url: str) -> Dict:
        """Setup webhook for incoming messages"""
        
        payload = {
            "messaging_product": "whatsapp",
            "url": webhook_url,
            "subscribe_to": ["message_status_update", "messages"]
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.business_account_id}/subscribed_apps",
                json=payload,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return {"success": True, "message": "Webhook setup successful"}
            else:
                return {"success": False, "error": response.json()}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def verify_webhook_token(self, verify_token: str, challenge_token: str, incoming_token: str) -> Optional[str]:
        """Verify webhook token for incoming requests"""
        if verify_token == incoming_token:
            return challenge_token
        return None


# Streamlit Helper Functions
def init_whatsapp_service():
    """Initialize WhatsApp service in Streamlit session"""
    if "whatsapp_service" not in st.session_state:
        try:
            api_token = st.secrets.get("WHATSAPP_API_TOKEN")
            phone_id = st.secrets.get("WHATSAPP_PHONE_ID")
            business_account_id = st.secrets.get("WHATSAPP_BUSINESS_ACCOUNT_ID")
            
            if not all([api_token, phone_id, business_account_id]):
                st.error("WhatsApp credentials not found in secrets")
                return None
            
            st.session_state.whatsapp_service = WhatsAppService(
                api_token, phone_id, business_account_id
            )
            return st.session_state.whatsapp_service
        
        except Exception as e:
            st.error(f"Error initializing WhatsApp service: {str(e)}")
            return None
    
    return st.session_state.whatsapp_service


def send_whatsapp_message(phone: str, message: str) -> Dict:
    """Send WhatsApp message with error handling"""
    service = init_whatsapp_service()
    
    if not service:
        return {"success": False, "error": "WhatsApp service not initialized"}
    
    try:
        result = service.send_text_message(phone, message)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
