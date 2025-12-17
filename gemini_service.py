"""
Gemini AI Service for Jewelry Shop Dashboard
Handles AI conversations, product recommendations, and customer support
"""

import google.generativeai as genai
import streamlit as st
from datetime import datetime
import json

class GeminiService:
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key"""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat_history = []
        
    def create_system_prompt(self, customer_name: str = None, customer_data: dict = None, gold_rate: float = 7850, silver_rate: float = 95):
        """Create context-aware system prompt"""
        
        customer_context = ""
        if customer_data:
            customer_context = f"""
Customer Information:
- Name: {customer_data.get('name', 'Unknown')}
- ID: {customer_data.get('id', 'N/A')}
- Tier: {customer_data.get('tier', 'Regular')}
- Total Spent: ₹{customer_data.get('total_spent', 0):,}
- Loyalty Points: {customer_data.get('loyalty_points', 0)}
- Last Purchase: {customer_data.get('last_purchase', 'Never')}
- Pending Payment: ₹{customer_data.get('pending_amount', 0):,}
"""
        
        system_prompt = f"""You are an expert AI assistant for a premium jewelry shop. You are helpful, professional, and knowledgeable about jewelry.

Current Market Rates:
- Gold (22K): ₹{gold_rate}/gram
- Silver (92.5%): ₹{silver_rate}/gram

{customer_context}

Your responsibilities:
1. Answer questions about products, prices, and purity
2. Provide personalized recommendations based on customer history
3. Help with order status and payment inquiries
4. Offer styling and jewelry care tips
5. Promote relevant offers and loyalty programs
6. Be professional and courteous
7. Escalate complex issues to human staff if needed

Always provide accurate information and maintain the shop's professional image."""
        
        return system_prompt
    
    def get_product_recommendations(self, customer_data: dict, purchase_history: list = None):
        """Get AI-powered product recommendations"""
        
        prompt = f"""Based on the customer profile below, recommend 3-4 jewelry products:

Customer Profile:
- Name: {customer_data.get('name')}
- Tier: {customer_data.get('tier')}
- Total Spent: ₹{customer_data.get('total_spent', 0):,}
- Previous Purchases: {len(purchase_history) if purchase_history else 0} items

Previous Purchase Types: {', '.join([p.get('item', '') for p in purchase_history[:5]]) if purchase_history else 'No history'}

Provide recommendations in this format:
1. Product Name - Reason why this suits them
2. Product Name - Reason why this suits them
etc.

Be specific and personalized."""

        response = self.model.generate_content(prompt)
        return response.text
    
    def answer_customer_query(self, query: str, customer_data: dict = None, context_text: str = ""):
        """Answer customer queries using Gemini"""
        
        system_prompt = self.create_system_prompt(customer_data=customer_data)
        
        full_prompt = f"""{system_prompt}

Additional Context: {context_text}

Customer Query: {query}

Please provide a helpful and accurate response."""
        
        response = self.model.generate_content(full_prompt)
        return response.text
    
    def generate_order_status_message(self, order_data: dict):
        """Generate personalized order status message"""
        
        prompt = f"""Write a friendly order status update message for this customer:

Order Details:
- Item: {order_data.get('item', 'N/A')}
- Amount: ₹{order_data.get('amount', 0):,}
- Status: {order_data.get('status', 'Processing')}
- Expected Delivery: {order_data.get('expected_delivery', 'Soon')}

Make it warm, professional, and include relevant details. Keep it under 100 words."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_payment_reminder(self, payment_data: dict):
        """Generate professional payment reminder message"""
        
        prompt = f"""Write a polite payment reminder message:

Payment Details:
- Customer: {payment_data.get('customer_name', 'Valued Customer')}
- Item: {payment_data.get('item', 'Your Order')}
- Amount Due: ₹{payment_data.get('amount', 0):,}
- Due Date: {payment_data.get('due_date', 'Soon')}

Be courteous and professional. Keep it under 80 words."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def create_marketing_message(self, campaign_data: dict):
        """Generate marketing campaign messages"""
        
        prompt = f"""Create an engaging marketing message for this promotion:

Campaign: {campaign_data.get('title', 'Promotion')}
Discount: {campaign_data.get('discount', 'Special')}
Description: {campaign_data.get('description', '')}
Valid Till: {campaign_data.get('valid_till', 'Limited Time')}

Make it catchy, engaging, and include a call-to-action. Keep it under 100 words."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def analyze_customer_sentiment(self, message: str):
        """Analyze sentiment of customer message"""
        
        prompt = f"""Analyze the sentiment of this customer message and provide:
1. Sentiment (Positive, Negative, Neutral)
2. Confidence level (0-100%)
3. Key emotion detected
4. Recommended response tone

Customer Message: "{message}"

Provide response in JSON format."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def generate_summary_report(self, messages: list):
        """Generate summary from multiple messages"""
        
        messages_text = "\n".join([f"- {msg}" for msg in messages])
        
        prompt = f"""Summarize these customer interactions:

{messages_text}

Provide:
1. Main topics discussed
2. Customer concerns (if any)
3. Action items
4. Overall sentiment
5. Recommended follow-up

Keep summary concise (100-150 words)."""
        
        response = self.model.generate_content(prompt)
        return response.text
    
    def multi_turn_chat(self, messages_history: list):
        """Enable multi-turn conversation with context"""
        
        conversation = ""
        for msg in messages_history[-10:]:  # Last 10 messages for context
            conversation += f"{msg['role']}: {msg['content']}\n"
        
        system_prompt = self.create_system_prompt()
        
        full_prompt = f"""{system_prompt}

Previous Conversation:
{conversation}

Respond naturally to continue the conversation."""
        
        response = self.model.generate_content(full_prompt)
        return response.text


# Streamlit Helper Functions
def init_gemini_service():
    """Initialize Gemini service in Streamlit session"""
    if "gemini_service" not in st.session_state:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("Gemini API key not found. Please add it to secrets.")
                return None
            
            st.session_state.gemini_service = GeminiService(api_key)
            return st.session_state.gemini_service
        except Exception as e:
            st.error(f"Error initializing Gemini: {str(e)}")
            return None
    
    return st.session_state.gemini_service


def get_gemini_response(prompt: str, customer_data: dict = None, context: str = ""):
    """Get response from Gemini with error handling"""
    service = init_gemini_service()
    
    if not service:
        return None
    
    try:
        response = service.answer_customer_query(prompt, customer_data, context)
        return response
    except Exception as e:
        st.error(f"Error getting Gemini response: {str(e)}")
        return None


def save_chat_history(role: str, messages: list, customer_id: str = None):
    """Save chat history to session state"""
    if "chat_histories" not in st.session_state:
        st.session_state.chat_histories = {}
    
    key = f"{role}_{customer_id}" if customer_id else role
    st.session_state.chat_histories[key] = messages
