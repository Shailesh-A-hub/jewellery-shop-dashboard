# 💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM - WITH GEMINI + WHATSAPP
# streamlit_app.v6.py - Ultimate Integrated Version

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import warnings
import requests
import json

# Try importing our new services (graceful fallback if not available)
try:
    from gemini_service import init_gemini_service, get_gemini_response
except ImportError:
    st.warning("⚠️ Gemini service not available. Install gemini_service.py")
    init_gemini_service = None
    get_gemini_response = None

try:
    from whatsapp_service import init_whatsapp_service, send_whatsapp_message
except ImportError:
    st.warning("⚠️ WhatsApp service not available. Install whatsapp_service.py")
    init_whatsapp_service = None
    send_whatsapp_message = None

warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# ============================================
# THEME & STYLING
# ============================================
st.markdown("""
<style>
    .main { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); }
    .stTabs [data-baseweb="tab-list"] { background-color: rgba(255, 215, 0, 0.1); }
    .stMetric { background: rgba(255, 215, 0, 0.05); padding: 10px; border-radius: 8px; }
    h1, h2, h3 { color: #FFD700; }
</style>
""", unsafe_allow_html=True)

# ============================================
# SESSION STATE INITIALIZATION
# ============================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []
    st.session_state.ai_chat_history = []
    st.session_state.whatsapp_sent_messages = []

# ============================================
# MARKET DATA
# ============================================
TODAY_RATES = {
    "gold": {
        "current": 7850,
        "previous": 7800,
        "change": 50,
        "change_percent": 0.64,
        "currency": "₹",
        "unit": "per gram"
    },
    "silver": {
        "current": 95,
        "previous": 92,
        "change": 3,
        "change_percent": 3.26,
        "currency": "₹",
        "unit": "per gram"
    },
}

# ============================================
# CUSTOMER DATA
# ============================================
CUSTOMER_DATA = {
    "customer": {
        "name": "Rajesh Sharma",
        "id": "CUST001",
        "email": "rajesh.sharma@email.com",
        "phone": "+91-98765-43210",
        "joining_date": "2023-03-15",
        "tier": "Gold",
        "loyalty_points": 850,
        "total_purchases": 12,
        "total_spent": 500000,
        "pending_amount": 45000,
        "last_purchase": "2025-12-08",
    }
}

CUSTOMER_PURCHASES = [
    {"date": "2025-12-08", "item": "Gold Ring", "purity": "22K", "weight": "5.2g", "amount": 45000, "status": "Delivered"},
    {"date": "2025-11-25", "item": "Silver Bracelet", "purity": "92.5%", "weight": "45g", "amount": 8500, "status": "Delivered"},
    {"date": "2025-11-15", "item": "Gold Necklace", "purity": "18K", "weight": "12.5g", "amount": 85000, "status": "Delivered"},
    {"date": "2025-10-30", "item": "Diamond Pendant", "purity": "Diamond", "weight": "0.5ct", "amount": 120000, "status": "Delivered"},
    {"date": "2025-10-10", "item": "Gold Earrings", "purity": "22K", "weight": "3.5g", "amount": 28000, "status": "Delivered"},
]

PENDING_PAYMENTS = [
    {"item": "Gold Bangles (Wedding Set)", "amount": 45000, "due_date": "2025-12-15", "status": "Pending Payment"},
]

CAMPAIGN_NOTIFICATIONS = [
    {"title": "🎄 Christmas Special Offer", "discount": "20% OFF", "description": "Get 20% discount on all gold items", "valid": "Till Dec 31, 2025", "status": "Active"},
    {"title": "💒 Wedding Season Sale", "discount": "15% OFF", "description": "Special discount on bridal collections", "valid": "Till Mar 31, 2026", "status": "Active"},
    {"title": "✨ New Year New Look", "discount": "25% OFF", "description": "Exclusive offers on selected items", "valid": "Dec 25 - Jan 15", "status": "Upcoming"},
    {"title": "🎁 Loyalty Rewards Program", "discount": "Extra Points", "description": "Earn 5X loyalty points on purchases", "valid": "Ongoing", "status": "Active"},
]

STAFF_MEMBERS = {
    "ram": {"name": "Ram Kumar", "position": "Sales Executive", "pending": "₹15,000"},
    "priya": {"name": "Priya Singh", "position": "Manager", "pending": "₹8,500"},
    "amit": {"name": "Amit Verma", "position": "Sales Associate", "pending": "₹12,000"},
    "neha": {"name": "Neha Sharma", "position": "Cashier", "pending": "₹5,500"},
}

USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager", "name": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff", "name": "Sales Staff"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer", "name": "Customer"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin", "name": "Admin"},
}

# ============================================
# DATA LOADERS
# ============================================
def load_mock_customers(seed=42):
    np.random.seed(seed)
    customers = []
    names = ["Rajesh Kumar", "Priya Singh", "Amit Patel", "Deepika Sharma", "Vikram Gupta",
             "Neha Verma", "Sanjay Pillai", "Anjali Nair", "Rohit Singh", "Pooja Reddy"]
    tiers = ["VIP", "Regular", "Dormant"]
    for i, name in enumerate(names * 6):
        tier_idx = np.random.randint(0, 3)
        customers.append({
            "id": i + 1,
            "name": f"{name}_{i+1}",
            "phone": f"98{np.random.randint(1000000, 9999999)}",
            "email": f"customer{i+1}@example.com",
            "total_spent": np.random.uniform(50000, 500000),
            "last_visit": (datetime.now() - timedelta(days=int(np.random.randint(1, 200)))).date(),
            "pending_amount": np.random.uniform(0, 100000),
            "tier": tiers[tier_idx],
        })
    return pd.DataFrame(customers)

def load_mock_transactions(seed=42):
    np.random.seed(seed)
    transactions = []
    descriptions = ["Gold Ring", "Diamond", "Bracelet", "Necklace", "Earrings"]
    for i in range(200):
        desc_idx = np.random.randint(0, len(descriptions))
        transactions.append({
            "id": i + 1,
            "customer_id": np.random.randint(1, 61),
            "date": (datetime.now() - timedelta(days=int(np.random.randint(1, 90)))).date(),
            "amount": np.random.uniform(10000, 100000),
            "payment_received": np.random.uniform(5000, 100000),
            "gst": np.random.uniform(500, 5000),
            "description": descriptions[desc_idx],
        })
    return pd.DataFrame(transactions)

def load_mock_inventory(seed=42):
    np.random.seed(seed)
    products = [
        ("Gold Ring - Traditional", "Rings", 22000, 35000),
        ("Diamond Ring - Solitaire", "Rings", 50000, 85000),
        ("Gold Bracelet - 22K", "Bracelets", 15000, 25000),
        ("Diamond Necklace - 18K", "Necklaces", 30000, 55000),
        ("Gold Earrings - Pair", "Earrings", 8000, 15000),
        ("Silver Ring - Oxidized", "Rings", 2000, 5000),
    ]
    inventory = []
    today = datetime.now().date()
    for _ in range(30):
        prod_idx = np.random.randint(0, len(products))
        prod_name, category, cost, price = products[prod_idx]
        stock_date = (datetime.now() - timedelta(days=int(np.random.randint(1, 180)))).date()
        days_in_stock = (today - stock_date).days
        inventory.append({
            "id": len(inventory) + 1,
            "product_name": prod_name,
            "category": category,
            "quantity": int(np.random.randint(1, 20)),
            "cost_price": cost,
            "selling_price": price,
            "margin_percent": ((price - cost) / price) * 100,
            "stock_date": stock_date,
            "days_in_stock": days_in_stock,
        })
    return pd.DataFrame(inventory)

# ============================================
# PAGE NAVIGATION
# ============================================
def get_accessible_pages(role):
    pages = {
        "Manager": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "👨💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot",
            "💬 Gemini + WhatsApp",  # NEW PAGE
            "🤖 ML Models",
            "⚙️ Advanced Settings",
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "💾 Sales Record",
            "🎁 Loyalty Program",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Chatbot",
            "💬 Gemini + WhatsApp",  # NEW PAGE
            "👨💼 Staff Dashboard",
        ],
        "Customer": [
            "💎 My Dashboard",
            "🛍️ My Purchases",
            "💎 My Chits",
            "🎁 Offers & Rewards",
            "📊 My Summary",
            "💬 Support Chat",
        ],
        "Admin": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "👨💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot",
            "💬 Gemini + WhatsApp",  # NEW PAGE
            "🤖 ML Models",
            "⚙️ Advanced Settings",
            "⚙️ Settings",
        ],
    }
    return pages.get(role, [])

# ============================================
# LOGIN PAGE
# ============================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 style='text-align: center; color: #FFD700;'>💎 Jewellery Shop AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("---")

        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Login 🔓", use_container_width=True):
                if username in USERS:
                    hashed_password = hashlib.sha256(password.encode()).hexdigest()
                    if USERS[username]["password"] == hashed_password:
                        st.session_state.authenticated = True
                        st.session_state.user_role = USERS[username]["role"]
                        st.session_state.username = username
                        st.success("✅ Login Successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid password")
                else:
                    st.error("❌ Username not found")

        with col2:
            st.info("📝 Demo Credentials:\nUsername: manager\nPassword: manager123")

        st.markdown("---")
        st.markdown("## 📈 Live Market Rates")
        gold = TODAY_RATES["gold"]
        silver = TODAY_RATES["silver"]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Gold Rate (22K)", f"₹{gold['current']}/g", f"+{gold['change']} ({gold['change_percent']:.2f}%)")
        with col2:
            st.metric("Silver Rate", f"₹{silver['current']}/g", f"+{silver['change']} ({silver['change_percent']:.2f}%)")

# ============================================
# GEMINI + WHATSAPP PAGE
# ============================================
def render_gemini_whatsapp_hub():
    """Integrated Gemini + WhatsApp communication hub"""
    
    st.markdown("# 💬 Gemini + WhatsApp Communication Hub")
    st.markdown("AI-Powered Customer Communication Platform")
    st.markdown("---")

    # Check services availability
    gemini_available = init_gemini_service is not None
    whatsapp_available = init_whatsapp_service is not None

    if not gemini_available or not whatsapp_available:
        st.warning("⚠️ Please ensure gemini_service.py and whatsapp_service.py are installed")
        st.info("Follow the setup guide: INTEGRATION_SETUP_GUIDE.md")
        return

    # Initialize services
    gemini_service = init_gemini_service()
    whatsapp_service = init_whatsapp_service()

    # Tab selection
    tab1, tab2, tab3, tab4 = st.tabs([
        "🤖 AI Chat",
        "💬 WhatsApp",
        "📢 Campaigns",
        "📊 Analytics"
    ])

    # ============================================
    # TAB 1: AI CHAT
    # ============================================
    with tab1:
        st.subheader("🤖 AI Assistant Chat")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.write("Chat with our AI-powered jewelry expert powered by Gemini")
        
        with col2:
            customer_select = st.selectbox(
                "Select Customer (Optional)",
                ["None", "Rajesh Sharma", "Priya Singh", "Amit Patel"],
                key="ai_customer"
            )

        # Customer data
        customer_data = None
        if customer_select != "None":
            customer_data = {
                "name": customer_select,
                "id": "CUST001",
                "tier": "Gold",
                "total_spent": 500000,
                "loyalty_points": 850,
                "last_purchase": "2025-12-08",
                "pending_amount": 45000
            }

        # Chat display
        st.write("**Chat History:**")
        chat_container = st.container(height=350, border=True)
        
        with chat_container:
            for msg in st.session_state.ai_chat_history[-10:]:  # Last 10 messages
                if msg["role"] == "user":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**🤖 AI:** {msg['content']}")
                st.divider()

        # Input
        col1, col2 = st.columns([4, 1])
        with col1:
            user_input = st.text_input(
                "Ask anything about jewelry!",
                placeholder="e.g., What's the current gold rate? Recommend me a necklace",
                key="ai_input"
            )
        
        with col2:
            send_button = st.button("Send 📤", key="ai_send")

        if send_button and user_input:
            st.session_state.ai_chat_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": datetime.now().isoformat()
            })

            with st.spinner("AI is thinking..."):
                ai_response = get_gemini_response(
                    user_input,
                    customer_data=customer_data,
                    context="Jewelry shop AI assistant"
                )

            if ai_response:
                st.session_state.ai_chat_history.append({
                    "role": "assistant",
                    "content": ai_response,
                    "timestamp": datetime.now().isoformat()
                })
                st.rerun()
            else:
                st.error("Failed to get response")

        # Quick actions
        st.subheader("Quick Actions")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("💍 Recommendations", key="qa_rec"):
                if gemini_service:
                    recs = gemini_service.get_product_recommendations(customer_data or {"name": "Guest", "tier": "Regular"})
                    st.session_state.ai_chat_history.append({"role": "assistant", "content": f"**Recommendations:**\n{recs}", "timestamp": datetime.now().isoformat()})
                    st.rerun()

        with col2:
            if st.button("💰 Gold Rate", key="qa_rate"):
                if gemini_service:
                    resp = get_gemini_response("What is today's gold price?", context=f"Gold: ₹{TODAY_RATES['gold']['current']}/g")
                    st.session_state.ai_chat_history.append({"role": "assistant", "content": resp, "timestamp": datetime.now().isoformat()})
                    st.rerun()

        with col3:
            if st.button("🎁 View Offers", key="qa_offers"):
                offers = "**Current Offers:**\n🎄 Christmas: 20% OFF\n💒 Wedding: 15% OFF\n✨ New Year: 25% OFF"
                st.session_state.ai_chat_history.append({"role": "assistant", "content": offers, "timestamp": datetime.now().isoformat()})
                st.rerun()

    # ============================================
    # TAB 2: WHATSAPP
    # ============================================
    with tab2:
        st.subheader("💬 Send WhatsApp Message")

        col1, col2 = st.columns(2)

        with col1:
            customer_name = st.selectbox(
                "Select Customer",
                ["Rajesh Sharma", "Priya Singh", "Amit Patel", "Manual Entry"],
                key="wa_customer"
            )

        with col2:
            if customer_name == "Manual Entry":
                phone = st.text_input("Phone Number", placeholder="+91-98765-43210", key="wa_phone_manual")
            else:
                phone_map = {"Rajesh Sharma": "+91-98765-43210", "Priya Singh": "+91-87654-32109", "Amit Patel": "+91-76543-21098"}
                phone = phone_map.get(customer_name, "")
                st.text_input("Phone Number", value=phone, disabled=True, key="wa_phone")

        st.write("**Message Type:**")
        msg_type = st.radio(
            "Choose type",
            ["Custom", "Order Confirmation", "Payment Reminder", "Delivery Update", "Promotional"],
            horizontal=True,
            key="wa_msg_type"
        )

        # Message templates
        if msg_type == "Custom":
            message = st.text_area("Your Message", height=120, key="wa_custom")
        
        elif msg_type == "Order Confirmation":
            col1, col2 = st.columns(2)
            with col1:
                order_id = st.text_input("Order ID", "ORD-001")
                item = st.text_input("Item", "Gold Ring")
            with col2:
                amount = st.number_input("Amount", 50000)
                delivery = st.date_input("Delivery Date")
            
            message = f"🎉 Order Confirmed!\n📦 {item}\n💰 ₹{amount:,}\n📅 Delivery: {delivery}\n\nThank you! 💎"

        elif msg_type == "Payment Reminder":
            col1, col2 = st.columns(2)
            with col1:
                item = st.text_input("Item", "Gold Bracelet")
                amount = st.number_input("Pending Amount", 45000)
            with col2:
                due_date = st.date_input("Due Date")
            
            message = f"💳 Payment Reminder\n💰 ₹{amount:,} pending\n📝 {item}\n📅 Due: {due_date}\n\nThank you! 🙏"

        elif msg_type == "Delivery Update":
            col1, col2 = st.columns(2)
            with col1:
                order_id = st.text_input("Order ID", "ORD-001")
                status = st.selectbox("Status", ["In Transit", "Out for Delivery", "Delivered"])
            with col2:
                delivery_date = st.date_input("Expected Delivery")
            
            message = f"📦 Delivery Update\n🏷️ {order_id}\n📍 {status}\n📅 {delivery_date}\n\nExciting! 💎"

        elif msg_type == "Promotional":
            col1, col2 = st.columns(2)
            with col1:
                offer_title = st.text_input("Offer", "Christmas Special")
                discount = st.text_input("Discount", "20% OFF")
            with col2:
                description = st.text_input("Description", "On all gold")
                valid = st.date_input("Valid Till")
            
            message = f"✨ {offer_title}!\n🎁 {discount}\n📝 {description}\n✅ Till {valid}\n\nDon't miss! 💎"

        st.text_area("Preview", message, height=100, disabled=True, key="wa_preview")

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("Send WhatsApp ✓", key="wa_send"):
                if not phone:
                    st.error("Enter phone number")
                elif not message:
                    st.error("Enter message")
                else:
                    with st.spinner("Sending..."):
                        result = send_whatsapp_message(phone, message) if send_whatsapp_message else {"success": False}
                    
                    if result.get("success"):
                        st.success(f"✅ Message sent to {phone}!")
                        st.session_state.whatsapp_sent_messages.append({"phone": phone, "message": message, "time": datetime.now()})
                        st.balloons()
                    else:
                        st.error(f"❌ Failed: {result.get('error')}")

        with col2:
            if st.button("Test Number", key="wa_test"):
                if phone and whatsapp_service:
                    is_valid = whatsapp_service.validate_phone_number(phone)
                    if is_valid:
                        st.success(f"✅ Valid: {phone}")
                    else:
                        st.error(f"❌ Invalid: {phone}")

    # ============================================
    # TAB 3: CAMPAIGNS
    # ============================================
    with tab3:
        st.subheader("📢 Bulk Campaign Manager")

        campaign_type = st.selectbox(
            "Campaign Type",
            ["Promotional", "Payment Reminder", "Loyalty Rewards", "New Launch"],
            key="campaign_type"
        )

        col1, col2 = st.columns(2)

        with col1:
            target = st.multiselect(
                "Target Segment",
                ["VIP", "Regular", "Dormant", "High Spenders"],
                default=["VIP"]
            )

        with col2:
            message = st.text_area(
                "Campaign Message",
                height=150,
                placeholder="Use {name}, {amount} placeholders",
                key="campaign_msg"
            )

        col1, col2, col3 = st.columns(3)

        with col1:
            recipients = st.number_input("Recipients", min_value=1, value=50)

        with col2:
            delay = st.number_input("Delay (seconds)", min_value=0, max_value=10, value=2)

        with col3:
            send_time = st.time_input("Send Time (Optional)")

        st.info(f"📊 Will send to ~{recipients} customers in {target}")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Preview 👀", key="campaign_preview"):
                st.markdown("**Campaign Preview:**")
                st.write(message)

        with col2:
            if st.button("Launch 🚀", key="campaign_launch"):
                with st.spinner(f"Launching to {recipients} customers..."):
                    st.success(f"✅ Campaign launched!")
                    st.balloons()

    # ============================================
    # TAB 4: ANALYTICS
    # ============================================
    with tab4:
        st.subheader("📊 Communication Analytics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Messages", 1247)

        with col2:
            st.metric("Delivered", "1,195 (95.8%)")

        with col3:
            st.metric("Failed", "52 (4.2%)")

        with col4:
            st.metric("Avg Response", "2.3 min")

        st.divider()

        st.subheader("Message History")

        history_data = {
            "Time": ["14:30", "14:15", "13:45", "13:20"],
            "Customer": ["Rajesh", "Priya", "Amit", "Neha"],
            "Type": ["Order", "Payment", "Promo", "Delivery"],
            "Phone": ["+91-9876543210", "+91-9876543211", "+91-9876543212", "+91-9876543213"],
            "Status": ["✅ Delivered", "✅ Delivered", "⏳ Pending", "✅ Delivered"]
        }

        df = pd.DataFrame(history_data)
        st.dataframe(df, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Message Types")
            types_df = pd.DataFrame({"Type": ["Order", "Payment", "Promo", "Delivery"], "Count": [320, 280, 450, 197]})
            st.bar_chart(types_df.set_index("Type"))

        with col2:
            st.subheader("Daily Volume")
            daily_df = pd.DataFrame({"Date": ["Dec 13", "Dec 14", "Dec 15", "Dec 16", "Dec 17"], "Count": [180, 220, 195, 280, 372]})
            st.line_chart(daily_df.set_index("Date"))

# ============================================
# DASHBOARD PAGE
# ============================================
def dashboard_page():
    """Main dashboard with key metrics"""
    
    st.markdown("# 📊 Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Customers", "1,247", "+12%")
    with col2:
        st.metric("Total Revenue", "₹45.2L", "+8%")
    with col3:
        st.metric("Pending Payments", "₹12.5L", "-5%")
    with col4:
        st.metric("Active Campaigns", "4", "+1")

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Sales Trend")
        sales_data = pd.DataFrame({
            "Date": ["Dec 1", "Dec 5", "Dec 10", "Dec 15", "Dec 17"],
            "Sales": [45000, 52000, 48000, 61000, 58000]
        })
        st.line_chart(sales_data.set_index("Date"))

    with col2:
        st.subheader("Customer Tiers")
        tier_data = pd.DataFrame({
            "Tier": ["VIP", "Regular", "Dormant"],
            "Count": [250, 700, 297]
        })
        st.bar_chart(tier_data.set_index("Tier"))

# ============================================
# MAIN APP
# ============================================
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar
        st.sidebar.markdown(f"### Welcome, {st.session_state.username}! 👋")
        st.sidebar.markdown(f"**Role:** {st.session_state.user_role}")
        st.sidebar.divider()

        # Get available pages
        pages = get_accessible_pages(st.session_state.user_role)
        selected_page = st.sidebar.radio("Navigate", pages, key="page_nav")

        # Page routing
        if selected_page == "📊 Dashboard":
            dashboard_page()
        
        elif selected_page == "💬 Gemini + WhatsApp":
            render_gemini_whatsapp_hub()
        
        elif selected_page == "🤖 AI Assistant":
            st.markdown("# 🤖 AI Assistant")
            st.info("Use Gemini + WhatsApp hub for integrated AI conversations!")
        
        elif selected_page == "💬 Chatbot":
            st.markdown("# 💬 Chatbot")
            st.info("Use Gemini + WhatsApp hub for customer support!")
        
        else:
            st.markdown(f"# {selected_page}")
            st.info("Page content coming soon...")

        # Logout
        st.sidebar.divider()
        if st.sidebar.button("Logout 🚪", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

if __name__ == "__main__":
    main()
