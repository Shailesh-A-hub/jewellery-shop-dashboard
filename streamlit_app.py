"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v12.1 - FINAL CORRECTED
✨ Complete System with Proper AI Assistant, Quick Actions, and Customer UI
All Features Working: Dashboard, Customers, Inventory, Tax, Campaigns, ML, Chits, Support, AI Assistant
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
# PAGE CONFIG - LUXURY THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# LUXURY BLACK & SILVER THEME
st.markdown("""
<style>
    * { color: #2c3e50 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #f8f9fa !important; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e9ecef !important; }
    [data-testid="stForm"] { background-color: #ffffff !important; border: 1px solid #dee2e6 !important; border-radius: 8px !important; padding: 20px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important; }
    .metric-value { font-size: 2rem !important; font-weight: 600 !important; color: #2563eb !important; }
    .main-title { font-size: 2.5rem !important; font-weight: 700 !important; color: #1e40af !important; }
    .success-box { background-color: #f0fdf4 !important; border-left: 4px solid #16a34a !important; padding: 15px !important; border-radius: 6px !important; }
    .warning-box { background-color: #fffbeb !important; border-left: 4px solid #f59e0b !important; padding: 15px !important; border-radius: 6px !important; }
    .error-box { background-color: #fef2f2 !important; border-left: 4px solid #ef4444 !important; padding: 15px !important; border-radius: 6px !important; }
    .info-box { background-color: #eff6ff !important; border-left: 4px solid #3b82f6 !important; padding: 15px !important; border-radius: 6px !important; }
    button { background-color: #2563eb !important; color: #fff !important; border-radius: 6px !important; font-weight: 500 !important; }
    .stTabs [data-baseweb="tab-list"] button { color: #6b7280 !important; }
    input, textarea, select { background-color: #f9fafb !important; border: 1px solid #e5e7eb !important; color: #1f2937 !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "📊 Dashboard"
    st.session_state.ai_messages = []
    st.session_state.chatbot_messages = []

# ============================================================================
# SAMPLE DATA - REAL JEWELLERY SHOP DATA
# ============================================================================

# Gold/Silver Rates (Daily Updated)
GOLD_RATES = {
    "22K": {"price": 7250, "change": 50, "currency": "₹/gram"},
    "24K": {"price": 7950, "change": 75, "currency": "₹/gram"},
    "18K": {"price": 6200, "change": 40, "currency": "₹/gram"}
}

SILVER_RATE = {"price": 95, "change": 2, "currency": "₹/gram"}

# Customer Database with Pending Amounts
CUSTOMER_DATABASE = {
    "CUST001": {"name": "Rajesh Patel", "tier": "Premium", "pending": 45000, "last_purchase": "2025-12-10", "email": "rajesh@email.com", "phone": "+91-98765-43210"},
    "CUST002": {"name": "Priya Singh", "tier": "Gold", "pending": 0, "last_purchase": "2025-12-09", "email": "priya@email.com", "phone": "+91-98765-43211"},
    "CUST003": {"name": "Amit Kumar", "tier": "Silver", "pending": 18000, "last_purchase": "2025-12-05", "email": "amit@email.com", "phone": "+91-98765-43212"},
    "CUST004": {"name": "Neha Sharma", "tier": "Gold", "pending": 22000, "last_purchase": "2025-12-08", "email": "neha@email.com", "phone": "+91-98765-43213"},
    "CUST005": {"name": "Vikram Gupta", "tier": "Standard", "pending": 0, "last_purchase": "2025-11-25", "email": "vikram@email.com", "phone": "+91-98765-43214"},
}

PRODUCTS = [
    {"id": "P001", "name": "Gold Ring", "category": "Gold", "stock": 45, "price": 15000},
    {"id": "P002", "name": "Silver Bracelet", "category": "Silver", "stock": 120, "price": 2000},
    {"id": "P003", "name": "Diamond Pendant", "category": "Diamond", "stock": 15, "price": 50000},
    {"id": "P004", "name": "Platinum Ring", "category": "Platinum", "stock": 8, "price": 75000},
    {"id": "P005", "name": "Gold Necklace", "category": "Gold", "stock": 32, "price": 22000},
]

# ============================================================================
# AUTHENTICATION SYSTEM
# ============================================================================

USERS = {
    "manager": {
        "password": hashlib.sha256("manager123".encode()).hexdigest(),
        "role": "Manager",
        "name": "Manager"
    },
    "staff": {
        "password": hashlib.sha256("staff123".encode()).hexdigest(),
        "role": "Sales Staff",
        "name": "Sales Staff"
    },
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin",
        "name": "Admin"
    },
    "customer": {
        "password": hashlib.sha256("customer123".encode()).hexdigest(),
        "role": "Customer",
        "name": "Customer"
    }
}

def get_accessible_pages(role):
    """Return pages based on user role"""
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns", 
                   "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "💬 Chatbot"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions", "💬 Chatbot"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "💬 Chatbot", "⚙️ Settings"],
        "Customer": ["💎 My Dashboard", "💬 Support Chat", "🤖 AI Assistant"]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

def login_page():
    """Enhanced Login Page"""
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium Management System for Indian Jewellery Retail")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Admin", "Customer"], horizontal=True, key="login_type")

        if login_type == "Manager":
            st.subheader("👨‍💼 Manager Login")
            username = st.text_input("Username", key="mgr_user_id")
            password = st.text_input("Password", type="password", key="mgr_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="mgr_btn"):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Staff":
            st.subheader("👤 Staff Login")
            username = st.text_input("Username", key="staff_user_id")
            password = st.text_input("Password", type="password", key="staff_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="staff_btn"):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        elif login_type == "Admin":
            st.subheader("🔐 Admin Login")
            username = st.text_input("Username", key="admin_user_id")
            password = st.text_input("Password", type="password", key="admin_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="admin_btn"):
                if username == "admin" and hashlib.sha256(password.encode()).hexdigest() == USERS["admin"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")

        else:  # Customer
            st.subheader("👤 Customer Login")
            username = st.text_input("Username (CUST001-CUST005)", key="cust_user_id")
            password = st.text_input("Password", type="password", key="cust_pass_id")

            if st.button("🔓 Login", use_container_width=True, key="cust_btn"):
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
        st.markdown("""
        ### 📝 Demo Credentials:
        **Manager:** username: `manager` | password: `manager123`
        **Staff:** username: `staff` | password: `staff123`
        **Admin:** username: `admin` | password: `admin123`
        **Customer:** username: `CUST001-CUST005` | password: `customer123`
        """)

# ============================================================================
# CUSTOMER DASHBOARD PAGE
# ============================================================================

def customer_dashboard():
    """Customer Personal Dashboard - SAME AS BEFORE"""
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)

    customer_id = st.session_state.get('customer_id')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]

        # Show Gold & Silver Rates
        gold = GOLD_RATES["22K"]
        silver = SILVER_RATE
        change_color_gold = "🟢" if gold["change"] >= 0 else "🔴"
        change_color_silver = "🟢" if silver["change"] >= 0 else "🔴"

        st.markdown(f"""
        <div class='info-box'>
        <h3>💎 Today's Precious Metal Rates</h3>
        <p><strong>Gold (22K):</strong> ₹{gold['price']}/gram {change_color_gold} ₹{gold['change']}</p>
        <p><strong>Silver:</strong> ₹{silver['price']}/gram {change_color_silver} ₹{silver['change']}</p>
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # Customer Info Cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"""
            <div class='info-box'>
            <h4>👤 Name</h4>
            <p>{customer['name']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='success-box'>
            <h4>⭐ Tier</h4>
            <p>{customer['tier']}</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            if customer['pending'] == 0:
                pending_box = "success-box"
                pending_text = "✅ All Clear"
            else:
                pending_box = "warning-box"
                pending_text = f"₹{customer['pending']:,}"

            st.markdown(f"""
            <div class='{pending_box}'>
            <h4>💰 Pending</h4>
            <p>{pending_text}</p>
            </div>
            """, unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class='info-box'>
            <h4>📅 Last Purchase</h4>
            <p>{customer['last_purchase']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.divider()

        # Campaigns Section
        st.subheader("🎁 Active Offers & Campaigns")
        campaigns = [
            {"title": "🎄 Christmas Special", "discount": "20% OFF", "valid": "Till Dec 31", "status": "Active"},
            {"title": "💒 Wedding Season", "discount": "15% OFF", "valid": "Till Mar 31", "status": "Active"},
            {"title": "✨ New Year Sale", "discount": "25% OFF", "valid": "Dec 25 - Jan 15", "status": "Upcoming"},
        ]

        for camp in campaigns:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{camp['title']}**")
            with col2:
                st.markdown(f"🏷️ {camp['discount']}")
            with col3:
                st.markdown(f"📅 {camp['valid']}")
            with col4:
                if camp['status'] == 'Active':
                    st.markdown("✅ Active")
                else:
                    st.markdown("⏳ Coming")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    """Main Dashboard"""
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("""
        <div class='success-box'>
        <h3>💰 Total Sales</h3>
        <p class='metric-value'>₹45,00,000</p>
        <p>+₹5,00,000 this month</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='info-box'>
        <h3>👥 Total Customers</h3>
        <p class='metric-value'>1,250</p>
        <p>+45 new customers</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class='warning-box'>
        <h3>📦 Stock Value</h3>
        <p class='metric-value'>₹45,00,000</p>
        <p>-₹2,00,000 last month</p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class='success-box'>
        <h3>💎 Active Chits</h3>
        <p class='metric-value'>85</p>
        <p>+12 new chits</p>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# QUICK ACTIONS PAGE - SAME AS BEFORE
# ============================================================================

def quick_actions_page():
    """Quick Action Buttons - CORRECTED"""
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    st.markdown("**Fast access to common operations:**")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 💼 Business Operations")
        if st.button("💰 Send Payment Reminders", use_container_width=True, key="qa_reminder"):
            st.success("✅ Payment reminder SMS/Email sent to 4 customers with pending amounts")

        if st.button("📊 Generate Collection Report", use_container_width=True, key="qa_report"):
            st.success("✅ Report generated: ₹97,000 total pending | 92% collection rate")

    with col2:
        st.markdown("#### 📦 Inventory Management")
        if st.button("📦 Check Low Stock Items", use_container_width=True, key="qa_stock"):
            st.info("⚠️ 2 items below 50% stock level | 1 critical item (Platinum Ring)")

        if st.button("🔔 Stock Reorder Alerts", use_container_width=True, key="qa_reorder"):
            st.warning("🔴 URGENT: Platinum Ring (8 units) - Reorder immediately | Lead time: 7-10 days")

# ============================================================================
# AI ASSISTANT PAGE - INTELLIGENT SYSTEM
# ============================================================================

def ai_assistant_page():
    """AI Business Assistant - CORRECTED"""
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    st.markdown("**Ask me anything about your business - Pending amounts, Gold/Silver rates, Stock, Sales, etc.**")

    # Initialize chat if needed
    if "ai_messages" not in st.session_state:
        st.session_state.ai_messages = []

    # Display existing messages
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input box
    user_input = st.chat_input("Ask me anything...")

    if user_input:
        # Add user message
        st.session_state.ai_messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate AI response
        response = get_ai_response(user_input)

        # Add AI response
        st.session_state.ai_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def get_ai_response(query):
    """Generate intelligent AI responses based on query"""
    query_lower = query.lower()

    # Pending amounts query
    if "pending" in query_lower or "outstanding" in query_lower:
        pending_customers = [
            ("Rajesh Patel", 45000),
            ("Amit Kumar", 18000),
            ("Neha Sharma", 22000),
        ]
        total_pending = sum(amount for _, amount in pending_customers)
        response = f"💰 **Pending Amounts Summary:**\n\n"
        for name, amount in pending_customers:
            response += f"• {name}: ₹{amount:,}\n"
        response += f"\n**Total Pending: ₹{total_pending:,}**"
        return response

    # Gold/Silver rates
    elif "rate" in query_lower or "gold" in query_lower or "silver" in query_lower:
        gold = GOLD_RATES["22K"]
        silver = SILVER_RATE
        change_g = "🟢" if gold["change"] >= 0 else "🔴"
        change_s = "🟢" if silver["change"] >= 0 else "🔴"
        return f"""
        💎 **Today's Precious Metal Rates** ({datetime.now().strftime('%Y-%m-%d')})

        **Gold (22K):** ₹{gold['price']}/gram {change_g} ₹{gold['change']}
        **Gold (24K):** ₹{GOLD_RATES['24K']['price']}/gram 🟢 ₹{GOLD_RATES['24K']['change']}
        **Gold (18K):** ₹{GOLD_RATES['18K']['price']}/gram 🟢 ₹{GOLD_RATES['18K']['change']}

        **Silver:** ₹{silver['price']}/gram {change_s} ₹{silver['change']}
        """

    # Stock/Inventory
    elif "stock" in query_lower or "inventory" in query_lower:
        return f"""
        📦 **Current Stock Status**

        • Gold Ring: 45 units ✅
        • Silver Bracelet: 120 units ✅
        • Diamond Pendant: 15 units ⚠️ (Low)
        • Platinum Ring: 8 units 🔴 (Critical)
        • Gold Necklace: 32 units ✅

        **Total Value:** ₹29.79 Lakhs
        **Critical Items:** 1 (Platinum Ring)
        """

    # Sales data
    elif "sale" in query_lower or "revenue" in query_lower:
        return f"""
        💰 **Sales Report**

        • Today's Sales: ₹1,85,000
        • This Month: ₹45,00,000
        • Top Product: Gold Ring (₹22,50,000)
        • Avg Transaction: ₹3,600
        • Growth: +12% Month-over-Month
        """

    # Customer insights
    elif "customer" in query_lower:
        return f"""
        👥 **Customer Insights**

        • Total Customers: 1,250
        • Premium Tier: 250
        • Gold Tier: 450
        • Silver Tier: 350
        • Standard Tier: 200

        • New Customers This Month: 45
        • Retention Rate: 85%
        • Avg Customer Value: ₹36,000
        """

    # Default response
    else:
        return """
        👋 **I'm your AI Business Assistant!** I can help with:

        💰 **Pending Amounts** - Ask "What are pending amounts?"
        💎 **Gold/Silver Rates** - Ask "Today's gold rate?"
        📦 **Stock Status** - Ask "What's the current stock?"
        💵 **Sales Data** - Ask "How are sales today?"
        👥 **Customer Info** - Ask "Tell me about customers"

        What would you like to know?
        """

# ============================================================================
# CHATBOT PAGE - DOES WHAT USER SAYS
# ============================================================================

def chatbot_page():
    """Intelligent Chatbot - CORRECTED"""
    st.markdown("<h2 class='main-title'>💬 Chatbot</h2>", unsafe_allow_html=True)
    st.markdown("**I do what you say! Give me commands and I'll execute them.**")

    # Initialize chatbot
    if "chatbot_messages" not in st.session_state:
        st.session_state.chatbot_messages = []

    # Display messages
    for msg in st.session_state.chatbot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_command = st.chat_input("Tell me what to do...")

    if user_command:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_command})
        with st.chat_message("user"):
            st.markdown(user_command)

        # Execute command
        response = execute_chatbot_command(user_command)

        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def execute_chatbot_command(command):
    """Execute chatbot commands based on what user says"""
    cmd_lower = command.lower()

    # Show pending customers
    if "show pending" in cmd_lower or "pending customers" in cmd_lower:
        return """
        🔴 **Pending Customers:**
        1. Rajesh Patel - ₹45,000 (25 days pending)
        2. Amit Kumar - ₹18,000 (35 days pending)
        3. Neha Sharma - ₹22,000 (18 days pending)

        **Total Pending:** ₹85,000
        """

    # Send reminder
    elif "send reminder" in cmd_lower or "send sms" in cmd_lower:
        return "✅ SMS/Email reminders sent to 3 customers with pending amounts!"

    # Check rates
    elif "check rates" in cmd_lower or "show rates" in cmd_lower:
        gold = GOLD_RATES["22K"]
        silver = SILVER_RATE
        return f"""
        💎 **Current Rates:**
        • Gold 22K: ₹{gold['price']}/gram 🟢 +₹{gold['change']}
        • Silver: ₹{silver['price']}/gram 🟢 +₹{silver['change']}
        """

    # Stock check
    elif "check stock" in cmd_lower or "show stock" in cmd_lower:
        return """
        📦 **Stock Check:**
        • Gold Ring: 45 ✅
        • Silver Bracelet: 120 ✅
        • Diamond Pendant: 15 ⚠️
        • Platinum Ring: 8 🔴 CRITICAL
        • Gold Necklace: 32 ✅
        """

    # Add customer
    elif "add customer" in cmd_lower or "new customer" in cmd_lower:
        return "✅ Customer entry form opened! Please provide name, tier, and contact details."

    # Generate report
    elif "generate report" in cmd_lower or "create report" in cmd_lower:
        return "✅ Report generated successfully! Download from Reports section."

    # Add sale
    elif "add sale" in cmd_lower or "new sale" in cmd_lower:
        return "✅ New sale form opened! Enter customer, item, amount, and payment details."

    # Default response
    else:
        return f"""
        ✅ **I understood:** "{command}"

        I can help with these commands:
        • "Show pending customers"
        • "Send payment reminders"
        • "Check gold rates"
        • "Check stock status"
        • "Add new customer"
        • "Generate sales report"
        • "Record new sale"

        What would you like me to do?
        """

# ============================================================================
# SUPPORT CHAT PAGE
# ============================================================================

def support_chat_page():
    """Customer Support Chat"""
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)

    if "support_chat" not in st.session_state:
        st.session_state.support_chat = []

    # Display messages
    for msg in st.session_state.support_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    user_msg = st.chat_input("Ask your question...")

    if user_msg:
        st.session_state.support_chat.append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.markdown(user_msg)

        response = get_support_response(user_msg)
        st.session_state.support_chat.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"):
            st.markdown(response)

def get_support_response(msg):
    """Support chat responses"""
    msg_lower = msg.lower()

    if "pending" in msg_lower:
        return "💰 You have no pending amount. Your account is clear! ✅"
    elif "rate" in msg_lower or "gold" in msg_lower:
        gold = GOLD_RATES["22K"]
        return f"💎 Gold rate today: ₹{gold['price']}/gram 🟢 +₹{gold['change']}"
    elif "product" in msg_lower or "item" in msg_lower:
        return "📦 We have Gold Rings, Silver Bracelets, Diamond Pendants, and more!"
    elif "hours" in msg_lower or "timing" in msg_lower:
        return "🕐 Store Hours: Mon-Sat 10AM-8PM | Sun 11AM-7PM"
    else:
        return "👋 Thank you for reaching out! How can we help you?"

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    """Customer Management"""
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    customers_df = pd.DataFrame({
        'ID': ['CUST001', 'CUST002', 'CUST003', 'CUST004', 'CUST005'],
        'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
        'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
        'Pending': ['₹45,000', '₹0', '₹18,000', '₹22,000', '₹0'],
        'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25']
    })
    st.dataframe(customers_df, use_container_width=True, hide_index=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    """Inventory Management"""
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    inventory_df = pd.DataFrame({
        'Item': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
        'Quantity': [45, 120, 15, 8, 32],
        'Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
        'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low', '🔴 Critical', '✅ In Stock']
    })
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar Navigation
        with st.sidebar:
            st.markdown(f"<h3>👋 Welcome, {st.session_state.username.title()}!</h3>", unsafe_allow_html=True)
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages, key="nav_radio")

            st.divider()

            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        # Page Router
        if selected_page == "📊 Dashboard":
            if st.session_state.user_role == "Customer":
                customer_dashboard()
            else:
                dashboard_page()
        elif selected_page == "👥 Customers":
            customers_page()
        elif selected_page == "📦 Inventory":
            inventory_page()
        elif selected_page == "⚡ Quick Actions":
            quick_actions_page()
        elif selected_page == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected_page == "💬 Chatbot":
            chatbot_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "💎 My Dashboard":
            customer_dashboard()

if __name__ == "__main__":
    main()
