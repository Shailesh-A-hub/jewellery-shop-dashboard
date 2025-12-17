import requests
import re
import streamlit as st
from datetime import datetime
from typing import List, Dict

class WhatsAppService:
    def __init__(self, api_token: str, phone_id: str, business_account_id: str):
        self.api_token = api_token
        self.phone_id = phone_id
        self.business_account_id = business_account_id
        self.api_url = f"https://graph.instagram.com/v18.0"
        self.headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }
    
    def validate_phone_number(self, phone: str) -> bool:
        pattern = r'^(\+91|91|0)?[6-9]\d{9}$'
        phone_clean = phone.replace("-", "").replace(" ", "")
        return bool(re.match(pattern, phone_clean))
    
    def format_phone_number(self, phone: str) -> str:
        phone_clean = phone.replace("+", "").replace("-", "").replace(" ", "")
        if not phone_clean.startswith("91") and len(phone_clean) == 10:
            phone_clean = "91" + phone_clean
        elif phone_clean.startswith("0"):
            phone_clean = "91" + phone_clean[1:]
        return phone_clean
    
    def send_text_message(self, to_phone: str, message: str) -> Dict:
        if not self.validate_phone_number(to_phone):
            return {"success": False, "error": f"Invalid phone: {to_phone}"}
        
        phone_number = self.format_phone_number(to_phone)
        payload = {
            "messaging_product": "whatsapp",
            "to": phone_number,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(
                f"{self.api_url}/{self.phone_id}/messages",
                json=payload,
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                return {"success": True, "phone": phone_number}
            else:
                return {"success": False, "error": "Send failed"}
        except Exception as e:
            return {"success": False, "error": str(e)}

def init_whatsapp_service():
    if "whatsapp_service" not in st.session_state:
        try:
            api_token = st.secrets.get("WHATSAPP_API_TOKEN")
            phone_id = st.secrets.get("WHATSAPP_PHONE_ID")
            business_account_id = st.secrets.get("WHATSAPP_BUSINESS_ACCOUNT_ID")
            if not all([api_token, phone_id, business_account_id]):
                return None
            st.session_state.whatsapp_service = WhatsAppService(api_token, phone_id, business_account_id)
            return st.session_state.whatsapp_service
        except:
            return None
    return st.session_state.whatsapp_service

def send_whatsapp_message(phone: str, message: str) -> Dict:
    service = init_whatsapp_service()
    if not service:
        return {"success": False, "error": "Service not initialized"}
    try:
        result = service.send_text_message(phone, message)
        return result
    except Exception as e:
        return {"success": False, "error": str(e)}
