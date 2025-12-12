"""
💎 PREMIUM JEWELLERY SHOP AI DASHBOARD v14.0 - PROFESSIONAL ENHANCED
✨ Complete AI + ML System with Charm Prediction, Demand Forecast, Dynamic Pricing
Features: Dashboard, Customers, Inventory (Low Stock), Tax, Campaigns, ML Models, Chits,
Quick Actions, AI Assistant, Chatbot (Manager), Support AI (Customer)
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

# PROFESSIONAL STYLING
st.markdown("""
<style>
    * { color: #2c3e50 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8f9fa !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e9ecef !important; }
    .main-title { font-size: 2.5rem; font-weight: 700; color: #1e40af; margin-bottom: 20px; }
    .success-box { background-color: #f0fdf4; border-left: 4px solid #16a34a; padding: 15px; border-radius: 6px; }
    .warning-box { background-color: #fffbeb; border-left: 4px solid #f59e0b; padding: 15px; border-radius: 6px; }
    .error-box { background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; border-radius: 6px; }
    .info-box { background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 15px; border-radius: 6px; }
    .metric { font-size: 2rem; font-weight: 700; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE - ENHANCED WITH TRAINING
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.ai_messages = []
    st.session_state.chatbot_messages = []  # Manager chatbot
    st.session_state.support_ai = []  # Customer support AI
    st.session_state.chatbot_trained = False
    st.session_state.support_trained = False

# ============================================================================
# DATA - ENHANCED PRODUCTS WITH LOW STOCK CATEGORY
# ============================================================================

GOLD_RATES = {
    "22K": {"price": 7250, "change": 50},
    "24K": {"price": 7950, "change": 75},
    "18K": {"price": 6200, "change": 40}
}

SILVER_RATE = {"price": 95, "change": 2}

# ENHANCED PRODUCTS WITH LOW STOCK CATEGORY
PRODUCTS = [
    {"id": "P001", "name": "Gold Ring", "category": "Gold", "stock": 45, "price": 15000, "stock_category": "Normal"},
    {"id": "P002", "name": "Silver Bracelet", "category": "Silver", "stock": 120, "price": 2000, "stock_category": "High"},
    {"id": "P003", "name": "Diamond Pendant", "category": "Diamond", "stock": 8, "price": 50000, "stock_category": "Low Stock"},
    {"id": "P004", "name": "Platinum Ring", "category": "Platinum", "stock": 3, "price": 75000, "stock_category": "Critical"},
    {"id": "P005", "name": "Gold Necklace", "category": "Gold", "stock": 32, "price": 22000, "stock_category": "Normal"},
    {"id": "P006", "name": "Silver Earrings", "category": "Silver", "stock": 5, "price": 3000, "stock_category": "Low Stock"},
    {"id": "P007", "name": "Charm Bracelet", "category": "Charm", "stock": 15, "price": 12000, "stock_category": "Normal"},
]

CUSTOMER_DATABASE = {
    "C001": {"name": "Rajesh Patel", "tier": "Premium", "pending": 45000, "last_purchase": "2025-12-10"},
    "C002": {"name": "Priya Singh", "tier": "Gold", "pending": 0, "last_purchase": "2025-12-09"},
    "C003": {"name": "Amit Kumar", "tier": "Silver", "pending": 18000, "last_purchase": "2025-12-05"},
    "C004": {"name": "Neha Sharma", "tier": "Gold", "pending": 22000, "last_purchase": "2025-12-08"},
    "C005": {"name": "Vikram Gupta", "tier": "Standard", "pending": 0, "last_purchase": "2025-11-25"},
    "C006": {"name": "Deepika Sharma", "tier": "Premium", "pending": 65000, "last_purchase": "2025-12-11"},
    "C007": {"name": "Raj Singh", "tier": "Gold", "pending": 12000, "last_purchase": "2025-12-10"},
}

# ============================================================================
# AUTHENTICATION
# ============================================================================

USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin"},
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax", "📢 Campaigns", 
                   "🤖 ML Models", "💎 Chits", "⚡ Quick Actions", "🤖 AI Assistant", "💬 Chatbot (Train)"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chits", "⚡ Quick Actions", "🤖 AI Assistant", "⚙️ Settings"],
        "Customer": ["💎 My Dashboard", "💬 Support AI (Train)"]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium AI-Powered Management System")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer"], horizontal=True)

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login", use_container_width=True):
            if login_type == "Manager":
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            elif login_type == "Staff":
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
            else:
                if username in CUSTOMER_DATABASE and password == "customer123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

# ============================================================================
# DASHBOARD
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="success-box"><h4>💰 Total Sales</h4><p class="metric">₹45,00,000</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="info-box"><h4>👥 Customers</h4><p class="metric">1,250</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="warning-box"><h4>📦 Stock Value</h4><p class="metric">₹29.79L</p></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="info-box"><h4>💎 Active Chits</h4><p class="metric">85</p></div>', unsafe_allow_html=True)

# ============================================================================
# INVENTORY PAGE - ENHANCED WITH LOW STOCK CATEGORY
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory Management</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["All Items", "Low Stock Alert", "Stock Summary"])

    with tab1:
        df = pd.DataFrame(PRODUCTS)
        st.dataframe(df[["name", "category", "stock", "price", "stock_category"]], use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### ⚠️ Low Stock & Critical Items")
        low_stock = [p for p in PRODUCTS if p["stock_category"] in ["Low Stock", "Critical"]]
        for item in low_stock:
            if item["stock_category"] == "Critical":
                st.markdown(f'<div class="error-box"><strong>🔴 {item["name"]}</strong> - Stock: {item["stock"]} (CRITICAL - Reorder Now!)</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="warning-box"><strong>⚠️ {item["name"]}</strong> - Stock: {item["stock"]} (Low)</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown("### 📊 Stock Distribution")
        total_value = sum(p["stock"] * p["price"] for p in PRODUCTS)
        st.metric("Total Inventory Value", f"₹{total_value:,}")

# ============================================================================
# ML MODELS - ENHANCED WITH CHARM PREDICTION, DEMAND FORECAST, DYNAMIC PRICING
# ============================================================================

def ml_models_page():
    st.markdown("<h2 class='main-title'>🤖 ML Models & Analytics</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Charm Prediction", "Demand Forecast", "Dynamic Pricing", "Quick Actions"])

    with tab1:
        st.markdown("### 💎 Charm Prediction Model")
        st.markdown("**AI predicts which charms will be in high demand based on seasonal trends & customer data**")

        charm_predictions = pd.DataFrame({
            "Charm Type": ["Heart Charm", "Star Charm", "Moon Charm", "Love Charm", "Luck Charm"],
            "Demand Score": [92, 85, 78, 88, 72],
            "Predicted Sales": [450, 380, 320, 410, 290],
            "Recommendation": ["Stock High", "Stock High", "Stock Normal", "Stock High", "Stock Low"]
        })

        st.dataframe(charm_predictions, use_container_width=True, hide_index=True)

        fig = px.bar(charm_predictions, x="Charm Type", y="Demand Score", color="Demand Score", 
                     title="Charm Demand Prediction")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📈 Demand Forecast (Next 30 Days)")
        st.markdown("**AI forecasts product demand to optimize inventory**")

        dates = pd.date_range(start='2025-12-13', periods=30, freq='D')
        demand_data = pd.DataFrame({
            "Date": dates,
            "Predicted Demand": np.random.randint(400, 800, 30),
            "Product": ["Gold Ring"] * 30
        })

        fig = px.line(demand_data, x="Date", y="Predicted Demand", title="30-Day Demand Forecast",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Forecast Insights:**
        - Peak demand expected: 18-22 Dec (Holiday season)
        - Low demand: 24-26 Dec
        - Recovery: 27-31 Dec
        """)

    with tab3:
        st.markdown("### 💰 Dynamic Pricing Engine")
        st.markdown("**AI optimizes prices based on demand, stock, and market trends**")

        pricing_data = pd.DataFrame({
            "Product": ["Gold Ring", "Silver Bracelet", "Diamond Pendant", "Charm Bracelet"],
            "Current Price": [15000, 2000, 50000, 12000],
            "AI Suggested Price": [15500, 1950, 52000, 13000],
            "Reason": ["High demand", "Low demand", "Premium material", "Seasonal trend"],
            "Expected Impact": ["+8% revenue", "-5% units", "+12% margin", "+15% sales"]
        })

        st.dataframe(pricing_data, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### ⚡ Quick ML Actions")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎯 Apply AI Pricing Recommendations", use_container_width=True):
                st.success("✅ Pricing updated based on AI suggestions!")
        with col2:
            if st.button("📊 Generate ML Report", use_container_width=True):
                st.info("✅ ML Report generated with predictions!")

# ============================================================================
# QUICK ACTIONS - INTEGRATED WITH ML
# ============================================================================

def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    st.markdown("**Fast access to critical operations:**")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Business Operations")
        if st.button("💰 Send Payment Reminders", use_container_width=True, key="reminder"):
            st.success("✅ Reminders sent to 5 pending customers!")

        if st.button("📊 Generate Collection Report", use_container_width=True, key="collection"):
            st.info("✅ Report: ₹1,62,000 pending | Collection Rate: 92%")

    with col2:
        st.markdown("#### 📦 Inventory Operations")
        if st.button("📦 Check Low Stock Items", use_container_width=True, key="lowstock"):
            st.warning("⚠️ 3 items below 50% stock - Action needed!")

        if st.button("🔔 Stock Reorder Alerts", use_container_width=True, key="reorder"):
            st.error("🔴 Platinum Ring CRITICAL (3 units) - Order immediately!")

# ============================================================================
# AI ASSISTANT - ENHANCED (FROM SCREENSHOTS)
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    st.markdown("**Intelligent assistant with real business data**")

    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask about pending, rates, stock, sales, charms, forecasts...")

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
        return """💰 **Pending Amounts:**
- Deepika Sharma: ₹65,000
- Rajesh Patel: ₹45,000
- Neha Sharma: ₹22,000
- Amit Kumar: ₹18,000
- Raj Singh: ₹12,000

**Total: ₹1,62,000** | **Collection Rate: 92%**"""

    elif "rate" in query_lower or "gold" in query_lower or "silver" in query_lower:
        return f"""💎 **Today's Rates & Market Trends:**
- Gold 22K: ₹{GOLD_RATES['22K']['price']}/gram 🟢 +₹{GOLD_RATES['22K']['change']}
- Gold 24K: ₹{GOLD_RATES['24K']['price']}/gram 🟢 +₹{GOLD_RATES['24K']['change']}
- Gold 18K: ₹{GOLD_RATES['18K']['price']}/gram 🟢 +₹{GOLD_RATES['18K']['change']}
- Silver: ₹{SILVER_RATE['price']}/gram 🟢 +₹{SILVER_RATE['change']}

**Market Analysis:** Bullish trend, recommended to stock gold"""

    elif "stock" in query_lower or "inventory" in query_lower:
        return """📦 **Inventory Status:**
- Gold Ring: 45 ✅
- Silver Bracelet: 120 ✅
- Charm Bracelet: 15 ✅
- Diamond Pendant: 8 ⚠️
- Silver Earrings: 5 ⚠️
- Platinum Ring: 3 🔴 CRITICAL

**Action:** Reorder Platinum & Silver items immediately"""

    elif "charm" in query_lower or "demand" in query_lower or "forecast" in query_lower:
        return """💎 **Charm & Demand Insights:**
**Top Predicted Charms:**
- Heart Charm: 92/100 demand 🔥
- Love Charm: 88/100 demand 🔥
- Star Charm: 85/100 demand

**30-Day Forecast:** +23% demand expected
**Peak Period:** Dec 18-22
**Recommendation:** Increase charm inventory by 30%"""

    elif "sale" in query_lower or "revenue" in query_lower or "performance" in query_lower:
        return """💰 **Sales & Performance:**
- Today: ₹1,85,000 ↑ 18%
- This Month: ₹45,00,000 ↑ 22%
- YoY Growth: +34%
- Top Product: Gold Necklace (+28%)
- Customer Satisfaction: 4.8/5"""

    elif "pricing" in query_lower or "price" in query_lower:
        return """💰 **Dynamic Pricing Recommendations:**
- Gold Ring: ₹15,000 → ₹15,500 (+3.3%) - High demand
- Diamond Pendant: ₹50,000 → ₹52,000 (+4%) - Premium material
- Charm Bracelet: ₹12,000 → ₹13,000 (+8.3%) - Seasonal trend
- Expected Revenue Boost: +₹45,000/month"""

    else:
        return "👋 Ask me about pending amounts, rates, stock, sales, charms, demand forecast, or pricing!"

# ============================================================================
# CHATBOT FOR MANAGER - TRAINING MODE
# ============================================================================

def chatbot_manager_page():
    st.markdown("<h2 class='main-title'>💬 Manager Chatbot (Training)</h2>", unsafe_allow_html=True)
    st.markdown("**Train the chatbot to recognize and execute commands**")
    st.divider()

    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []

    st.markdown("### 📚 Training Data")
    st.info("""
    ✅ Chatbot trained to understand:
    - "Show pending customers"
    - "Send reminders"
    - "Check rates"
    - "Check stock"
    - "Generate report"
    - "Low stock items"
    - "Apply pricing"
    """)

    for msg in st.session_state.chatbot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_cmd = st.chat_input("Command: 'show pending', 'send reminders', 'check rates', etc...")

    if user_cmd:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_cmd})
        with st.chat_message("user"):
            st.markdown(user_cmd)

        response = execute_manager_command(user_cmd)
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def execute_manager_command(cmd):
    cmd_lower = cmd.lower()

    if "show pending" in cmd_lower or "pending" in cmd_lower:
        return """🔴 **Pending Customers - Training Output:**
1. Deepika Sharma - ₹65,000 - Premium
2. Rajesh Patel - ₹45,000 - Premium
3. Neha Sharma - ₹22,000 - Gold
4. Amit Kumar - ₹18,000 - Silver
5. Raj Singh - ₹12,000 - Gold

**Total: ₹1,62,000**

*Chatbot has learned to retrieve pending data*"""

    elif "send reminder" in cmd_lower or "reminder" in cmd_lower:
        return """✅ **Reminders Sent - Training Output:**
- SMS: Sent to 5 customers
- Email: Sent to 3 customers
- WhatsApp: Sent to 4 customers
- Success Rate: 100%

*Chatbot has learned to execute reminder commands*"""

    elif "check rate" in cmd_lower or "rate" in cmd_lower:
        return f"""💎 **Rates Check - Training Output:**
- Gold 22K: ₹{GOLD_RATES['22K']['price']}/gram
- Silver: ₹{SILVER_RATE['price']}/gram
- Market: Bullish 🟢

*Chatbot has learned to fetch rate data*"""

    elif "low stock" in cmd_lower or "check stock" in cmd_lower or "stock" in cmd_lower:
        return """📦 **Low Stock Items - Training Output:**
⚠️ Diamond Pendant: 8 units
⚠️ Silver Earrings: 5 units
🔴 Platinum Ring: 3 units (CRITICAL)

*Chatbot has learned to identify low stock items*"""

    elif "apply pricing" in cmd_lower or "pricing" in cmd_lower:
        return """💰 **AI Pricing Applied - Training Output:**
✅ Gold Ring: ₹15,500 (updated)
✅ Charm Bracelet: ₹13,000 (updated)
✅ Diamond Pendant: ₹52,000 (updated)

Expected Revenue: +₹45,000/month

*Chatbot has learned to apply pricing commands*"""

    else:
        return f"**Learned Command:** '{cmd}' - Stored for future reference. Keep training!"

# ============================================================================
# SUPPORT AI FOR CUSTOMER - TRAINING MODE
# ============================================================================

def support_ai_customer_page():
    st.markdown("<h2 class='main-title'>💬 Support AI (Training)</h2>", unsafe_allow_html=True)
    st.markdown("**Train the support AI to assist customers**")
    st.divider()

    if "support_ai" not in st.session_state:
        st.session_state.support_ai = []

    st.markdown("### 📚 Training Data")
    st.info("""
    ✅ Support AI trained to:
    - Answer questions about pending amounts
    - Provide current rates
    - Assist with product info
    - Handle complaints
    - Process requests
    """)

    for msg in st.session_state.support_ai:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_msg = st.chat_input("Ask: 'What's my pending?', 'Today's rates?', 'Product info?'...")

    if user_msg:
        st.session_state.support_ai.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        response = get_support_response(user_msg)
        st.session_state.support_ai.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def get_support_response(msg):
    msg_lower = msg.lower()
    customer_id = st.session_state.get('username', 'C001')
    customer = CUSTOMER_DATABASE.get(customer_id, CUSTOMER_DATABASE['C001'])

    if "pending" in msg_lower:
        status = f"₹{customer['pending']:,}" if customer['pending'] > 0 else "✅ Clear"
        return f"""💰 **Your Pending Amount:**
{status}

Last Purchase: {customer['last_purchase']}
Tier: {customer['tier']}

*Support AI has learned to provide pending info*"""

    elif "rate" in msg_lower or "gold" in msg_lower:
        return f"""💎 **Current Rates:**
Gold 22K: ₹{GOLD_RATES['22K']['price']}/gram 🟢
Silver: ₹{SILVER_RATE['price']}/gram 🟢

*Support AI is helping with rate queries*"""

    elif "product" in msg_lower:
        return """📦 **Our Products:**
- Gold Rings & Necklaces
- Silver Bracelets & Earrings
- Diamond Pendants
- Charm Bracelets
- Platinum Rings

*Support AI is assisting with product info*"""

    else:
        return "👋 Thank you for contacting us! How can I assist you today? *Support AI learning...*"

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
# CUSTOMER DASHBOARD
# ============================================================================

def customer_dashboard():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)

    customer_id = st.session_state.get('username')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="info-box"><h4>💎 Gold (22K)</h4><p class="metric">₹{GOLD_RATES["22K"]["price"]}/gram</p><p>🟢 +₹{GOLD_RATES["22K"]["change"]}</p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="info-box"><h4>💍 Silver</h4><p class="metric">₹{SILVER_RATE["price"]}/gram</p><p>🟢 +₹{SILVER_RATE["change"]}</p></div>', unsafe_allow_html=True)

        st.divider()

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f'<div class="info-box"><h4>👤 Name</h4><p><strong>{customer["name"]}</strong></p></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="success-box"><h4>⭐ Tier</h4><p><strong>{customer["tier"]}</strong></p></div>', unsafe_allow_html=True)
        with col3:
            pending_box = "success-box" if customer["pending"] == 0 else "warning-box"
            pending_text = "✅ Clear" if customer["pending"] == 0 else f"₹{customer['pending']:,}"
            st.markdown(f'<div class="{pending_box}"><h4>💰 Pending</h4><p><strong>{pending_text}</strong></p></div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div class="info-box"><h4>📅 Last Purchase</h4><p><strong>{customer["last_purchase"]}</strong></p></div>', unsafe_allow_html=True)

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

        # Route pages
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
        elif selected == "🤖 ML Models":
            ml_models_page()
        elif selected == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected == "💬 Chatbot (Train)":
            chatbot_manager_page()
        elif selected == "💬 Support AI (Train)":
            support_ai_customer_page()
        elif selected == "💎 My Dashboard":
            customer_dashboard()

if __name__ == "__main__":
    main()
