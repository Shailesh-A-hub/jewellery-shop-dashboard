import google.generativeai as genai
import streamlit as st

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def answer_customer_query(self, query: str, customer_data: dict = None, context_text: str = ""):
        system_prompt = f"""You are a jewelry shop AI assistant. Be helpful and professional."""
        full_prompt = f"{system_prompt}\n\nQuery: {query}"
        response = self.model.generate_content(full_prompt)
        return response.text

def init_gemini_service():
    if "gemini_service" not in st.session_state:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
            if not api_key:
                return None
            st.session_state.gemini_service = GeminiService(api_key)
            return st.session_state.gemini_service
        except:
            return None
    return st.session_state.gemini_service

def get_gemini_response(prompt: str, customer_data: dict = None, context: str = ""):
    service = init_gemini_service()
    if not service:
        return None
    try:
        response = service.answer_customer_query(prompt, customer_data, context)
        return response
    except:
        return None
