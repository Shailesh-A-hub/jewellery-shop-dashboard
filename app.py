import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import warnings

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None

# ... rest of your code



import google.generativeai as genai
import streamlit as st
import time

class GeminiService:
    def __init__(self, api_key: str):
        """Initialize Gemini service with API key"""
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        except Exception as e:
            st.error(f"Failed to initialize Gemini: {str(e)}")
            self.model = None
    
    def answer_customer_query(self, query: str, customer_data: dict = None, context_text: str = ""):
        """Answer customer queries using Gemini with error handling"""
        
        if not self.model:
            return "Error: Gemini not initialized properly"
        
        try:
            system_prompt = """You are an expert AI assistant for a premium jewelry shop. 
Be helpful, professional, and knowledgeable about jewelry, jewelry care, and customer service.
Current context: You are assisting with customer queries about jewelry products, prices, and care."""
            
            if customer_data:
                system_prompt += f"\n\nCustomer: {customer_data.get('name', 'Customer')}"
            
            # Combine prompts
            full_message = f"{system_prompt}\n\nCustomer Question: {query}"
            
            # Generate response with timeout
            response = self.model.generate_content(
                full_message,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=500,
                    temperature=0.7
                )
            )
            
            if response and response.text:
                return response.text
            else:
                return "I apologize, I couldn't generate a response. Please try again."
        
        except Exception as e:
            error_msg = str(e)
            if "API key" in error_msg or "authentication" in error_msg.lower():
                return f"Error: API key issue - {error_msg}"
            elif "quota" in error_msg.lower():
                return "Error: API quota exceeded. Please try again later."
            else:
                return f"Error getting response: {error_msg}"

def init_gemini_service():
    """Initialize Gemini service in Streamlit session"""
    if "gemini_service" not in st.session_state:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                st.error("❌ GEMINI_API_KEY not found in Streamlit secrets!")
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
        return "Error: Gemini service not available. Please check your API key."
    
    try:
        response = service.answer_customer_query(prompt, customer_data, context)
        return response
    except Exception as e:
        return f"Error: {str(e)}"
