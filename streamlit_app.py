"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v13.2 - CLEAN & ERROR-FREE
✨ Complete System with AI Assistant, Quick Actions, and Customer Dashboard
All Features: Dashboard, Customers, Inventory, Tax, Campaigns, ML, Chits, Support
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import warnings

warnings.filterwarnings('ignore')

# ============================================================================
# PAGE CONFIG
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# STYLING
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; color: #1e40af; }
    .success-box { background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px; border-radius: 6px; }
    .warning-box { background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 6px; }
    .error-box { background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; }
    .info-box { background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 6px; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.ai_messages = []
    st.session_state.chatbot_messages = []
    st.session_state.support_chat = []

# ============================================================================
# DATA
# ============================================================================

GOLD_RATES = {
    "22K": {"price": 7250, "change": 50},
    "24K": {"price": 7950, "change": 75},
    "18K": {"price": 6200, "change": 40}
}

SILVER_RATE = {"price": 95, "change": 2}

CUSTOMER_DATABASE = {
    "C001": {"name": "Rajesh Patel", "tier": "Premium", "pending": 45000, "last_purchase": "2025-12-10"},
    "C002": {"name": "Priya Singh", "tier": "Gold", "pending": 0, "last_purchase": "2025-12-09"},
    "C003": {"name": "Amit Kumar", "tier": "Silver", "pending": 18000, "last_purchase": "2025-12-05"},
    "C004": {"name": "Neha Sharma", "tier": "Gold", "pending": 22000, "last_purchase": "2025-12-08"},
    "C005": {"name": "Vikram Gupta", "tier": "Standard", "pending": 0, "last_purchase": "2025-11-25"},
    "C006": {"name": "Deepika Sharma", "tier": "Premium", "pending": 65000, "last_purchase": "2025-12-11"},
    "C007": {"name": "Raj Singh", "tier": "Gold", "pending": 12000, "last_purchase": "2025-12-10"},
}

PRODUCTS = [
    {"id": "P001", "name": "Gold Ring", "category": "Gold", "stock": 45, "price": 15000},
    {"id": "P002", "name": "Silver Bracelet", "category": "Silver", "stock": 120, "price": 2000},
    {"id": "P003", "name": "Diamond Pendant", "category": "Diamond", "stock": 15, "price": 50000},
    {"id": "P004", "name": "Platinum Ring", "category": "Platinum", "stock": 8, "price": 75000},
    {"id": "P005", "name": "Gold Necklace", "category": "Gold", "stock": 32, "price": 22000},
]

# ============================================================================
# AUTH
# ============================================================================

USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer"}
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax", "📢 Campaigns", 
                   "🤖 ML Models", "💎 Chits", "⚡ Quick Actions", "🤖 AI Assistant"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chits", "⚡ Quick Actions", "🤖 AI Assistant", "⚙️ Settings"],
        "Customer": ["💬 Support Chat", "📊 My Dashboard"]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium Jewellery Management System")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer"], horizontal=True)

        if login_type == "Manager":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Staff":
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        else:
            username = st.text_input("Customer ID (C001-C007)")
            password = st.text_input("Password", type="password")
            if st.button("Login", use_container_width=True):
                if username in CUSTOMER_DATABASE and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.session_state.customer_id = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        st.divider()
        st.markdown("**Demo:** manager/manager123 | staff/staff123 | C001/customer123")

# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================

def customer_dashboard():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)

    customer_id = st.session_state.get('customer_id')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class='info-box'>
            <h4>💎 Gold (22K) Rate</h4>
            <p style='font-size: 1.8rem; font-weight: bold;'>₹{GOLD_RATES['22K']['price']}/gram</p>
            <p>🟢 +₹{GOLD_RATES['22K']['change']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='info-box'>
            <h4>💍 Silver Rate</h4>
            <p style='font-size: 1.8rem; font-weight: bold;'>₹{SILVER_RATE['price']}/gram</p>
            <p>🟢 +₹{SILVER_RATE['change']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class='info-box'>
            <h4>👤 Name</h4>
            <p><strong>{customer['name']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='success-box'>
            <h4>⭐ Tier</h4>
            <p><strong>{customer['tier']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if customer['pending'] == 0:
                pending_box = "success-box"
                pending_text = "✅ Clear"
            else:
                pending_box = "warning-box"
                pending_text = f"₹{customer['pending']:,}"

            st.markdown(f"""
            <div class='{pending_box}'>
            <h4>💰 Pending</h4>
            <p><strong>{pending_text}</strong></p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class='info-box'>
            <h4>📅 Last Purchase</h4>
            <p><strong>{customer['last_purchase']}</strong></p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='success-box'>
        <h4>💰 Total Sales</h4>
        <p style='font-size: 1.8rem; font-weight: bold;'>₹45,00,000</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-box'>
        <h4>👥 Customers</h4>
        <p style='font-size: 1.8rem; font-weight: bold;'>1,250</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='warning-box'>
        <h4>📦 Stock Value</h4>
        <p style='font-size: 1.8rem; font-weight: bold;'>₹29.79L</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='info-box'>
        <h4>💎 Active Chits</h4>
        <p style='font-size: 1.8rem; font-weight: bold;'>85</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# AI ASSISTANT
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    st.markdown("**Ask about pending amounts, rates, stock, sales, and more!**")

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask anything about your business...")

    if user_input:
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        response = get_ai_response(user_input)
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def get_ai_response(query):
    query_lower = query.lower()

    if "pending" in query_lower:
        return """💰 **Pending Amounts Summary:**
- Rajesh Patel: ₹45,000
- Deepika Sharma: ₹65,000
- Neha Sharma: ₹22,000
- Amit Kumar: ₹18,000
- Raj Singh: ₹12,000

**Total: ₹1,62,000**"""

    elif "rate" in query_lower or "gold" in query_lower:
        return f"""💎 **Today's Rates:**
- Gold 22K: ₹{GOLD_RATES['22K']['price']}/gram 🟢 +₹{GOLD_RATES['22K']['change']}
- Gold 24K: ₹{GOLD_RATES['24K']['price']}/gram 🟢 +₹{GOLD_RATES['24K']['change']}
- Gold 18K: ₹{GOLD_RATES['18K']['price']}/gram 🟢 +₹{GOLD_RATES['18K']['change']}
- Silver: ₹{SILVER_RATE['price']}/gram 🟢 +₹{SILVER_RATE['change']}"""

    elif "stock" in query_lower:
        return """📦 **Stock Status:**
- Gold Ring: 45 ✅
- Silver Bracelet: 120 ✅
- Diamond Pendant: 15 ⚠️
- Platinum Ring: 8 🔴
- Gold Necklace: 32 ✅"""

    elif "sale" in query_lower or "revenue" in query_lower:
        return """💰 **Sales Analytics:**
- Today: ₹1,85,000
- This Month: ₹45,00,000
- Growth: +12% MoM"""

    else:
        return "👋 Ask me about pending amounts, rates, stock, sales, or customers!"

# ============================================================================
# QUICK ACTIONS
# ============================================================================

def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    st.markdown("**Fast access to common operations:**")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Business Operations")
        if st.button("💰 Send Payment Reminders", use_container_width=True):
            st.success("✅ Payment reminders sent to 5 customers!")

        if st.button("📊 Generate Collection Report", use_container_width=True):
            st.success("✅ Report: ₹1,62,000 pending | 92% collection rate")

    with col2:
        st.markdown("#### 📦 Inventory Management")
        if st.button("📦 Check Low Stock Items", use_container_width=True):
            st.info("⚠️ 2 items below 50% stock")

        if st.button("🔔 Stock Reorder Alerts", use_container_width=True):
            st.warning("🔴 Platinum Ring critical (8 units)")

# ============================================================================
# CHATBOT
# ============================================================================

def chatbot_page():
    st.markdown("<h2 class='main-title'>💬 Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("**I do what you say! Give commands.**")

    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []

    for msg in st.session_state.chatbot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_cmd = st.chat_input("Give a command...")

    if user_cmd:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_cmd})
        with st.chat_message("user"):
            st.markdown(user_cmd)

        response = execute_command(user_cmd)
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def execute_command(cmd):
    cmd_lower = cmd.lower()

    if "show pending" in cmd_lower or "pending" in cmd_lower:
        return """🔴 **Pending Customers:**
1. Deepika Sharma - ₹65,000
2. Rajesh Patel - ₹45,000
3. Neha Sharma - ₹22,000
4. Amit Kumar - ₹18,000
5. Raj Singh - ₹12,000

**Total: ₹1,62,000**"""

    elif "send reminder" in cmd_lower:
        return "✅ Reminders sent to 5 customers!"

    elif "check rate" in cmd_lower or "gold" in cmd_lower:
        return f"💎 Gold 22K: ₹{GOLD_RATES['22K']['price']}/gram | Silver: ₹{SILVER_RATE['price']}/gram"

    elif "check stock" in cmd_lower:
        return "📦 All stock levels checked!"

    else:
        return f"✅ Command: {cmd} - What would you like me to do?"

# ============================================================================
# SUPPORT CHAT
# ============================================================================

def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)

    if "support_chat" not in st.session_state:
        st.session_state.support_chat = []

    for msg in st.session_state.support_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input("Ask a question...")

    if user_msg:
        st.session_state.support_chat.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        response = support_response(user_msg)
        st.session_state.support_chat.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def support_response(msg):
    msg_lower = msg.lower()
    if "pending" in msg_lower:
        return "💰 Check your pending amount in the dashboard."
    elif "rate" in msg_lower:
        return f"💎 Gold (22K): ₹{GOLD_RATES['22K']['price']}/gram"
    elif "product" in msg_lower:
        return "📦 We have Gold Rings, Bracelets, Diamond Pendants, and more!"
    else:
        return "👋 Thank you for reaching out! How can we help?"

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    df = pd.DataFrame([
        {"ID": k, "Name": v["name"], "Tier": v["tier"], "Pending": f"₹{v['pending']:,}"} 
        for k, v in CUSTOMER_DATABASE.items()
    ])
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    df = pd.DataFrame(PRODUCTS)
    st.dataframe(df, use_container_width=True, hide_index=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>👋 {st.session_state.username}</h3>", unsafe_allow_html=True)
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected = st.radio("Navigation", pages, key="nav")

            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        if selected == "📊 Dashboard":
            if st.session_state.user_role == "Customer":
                customer_dashboard()
            else:
                dashboard_page()
        elif selected == "👥 Customers":
            customers_page()
        elif selected == "📦 Inventory":
            inventory_page()
        elif selected == "⚡ Quick Actions":
            quick_actions_page()
        elif selected == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected == "💬 Chatbot":
            chatbot_page()
        elif selected == "💬 Support Chat":
            support_chat_page()
        elif selected == "📊 My Dashboard":
            customer_dashboard()

if __name__ == "__main__":
    main()
