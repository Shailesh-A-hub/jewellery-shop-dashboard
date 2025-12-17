# streamlit_app.v5.py - merged final file (v5 + v4 features)
# 💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM - MERGED VERSION

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

# -------------------------------
# THEME (same as your v5)
# -------------------------------
st.markdown(
    """
<style>
    * {
        color: #e8e8e8 !important;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
    }

    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 2px solid #c0c0c0 !important;
    }

    [data-testid="stForm"] {
        background-color: #1a1a1a !important;
        border: 2px solid #404040 !important;
        border-radius: 12px !important;
        padding: 20px !important;
    }

    [role="radiogroup"] {
        background-color: transparent !important;
    }

    .main {
        background-color: #0f0f0f !important;
    }

    .main-title { 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: #c0c0c0 !important;
        text-shadow: 2px 2px 8px rgba(192, 192, 192, 0.3);
        letter-spacing: 2px;
    }

    .metric-box {
        background: linear-gradient(135deg, #1a1a1a 0%, #252525 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        text-align: center !important;
        color: #e8e8e8 !important;
        box-shadow: 0 8px 32px rgba(192, 192, 192, 0.1) !important;
    }

    .chart-box {
        background-color: #1a1a1a !important;
        border: 1px solid #404040 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }

    .info-box { 
        background: linear-gradient(135deg, #1a3a3a 0%, #1a2a3a 100%) !important;
        border-left: 4px solid #c0c0c0 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
    }

    .success-box {
        background: linear-gradient(135deg, #1a3a1a 0%, #1a2a1a 100%) !important;
        border-left: 4px solid #7cb342 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
    }

    .warning-box {
        background: linear-gradient(135deg, #3a3a1a 0%, #2a2a1a 100%) !important;
        border-left: 4px solid #fbc02d !important;
        padding: 15px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
    }

    .ai-response {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        margin: 12px 0 !important;
        color: #e8e8e8 !important;
        box-shadow: 0 4px 16px rgba(192, 192, 192, 0.08) !important;
    }

    .gold-box {
        background: linear-gradient(135deg, #3a2a1a 0%, #2a1a0a 100%) !important;
        border: 2px solid #ffd700 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        color: #ffd700 !important;
        box-shadow: 0 4px 16px rgba(255, 215, 0, 0.15) !important;
        text-align: center !important;
    }

    .silver-box {
        background: linear-gradient(135deg, #2a2a3a 0%, #1a1a2a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 20px !important;
        color: #c0c0c0 !important;
        box-shadow: 0 4px 16px rgba(192, 192, 192, 0.15) !important;
        text-align: center !important;
    }

    .campaign-notification {
        background: linear-gradient(135deg, #3a2a1a 0%, #2a1f0a 100%) !important;
        border-left: 5px solid #ffd700 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        color: #e8e8e8 !important;
        margin: 10px 0 !important;
        box-shadow: 0 4px 12px rgba(255, 215, 0, 0.1) !important;
    }

    .button-primary {
        background: linear-gradient(135deg, #c0c0c0 0%, #a8a8a8 100%) !important;
        color: #0f0f0f !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 12px rgba(192, 192, 192, 0.2) !important;
    }

    .button-secondary {
        background: linear-gradient(135deg, #2a2a2a 0%, #1a1a1a 100%) !important;
        color: #e8e8e8 !important;
        border: 1px solid #c0c0c0 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
    }

    div[data-testid="stVerticalBlock"] > div {
        color: #e8e8e8 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #c0c0c0 !important;
        letter-spacing: 1px;
    }

    [data-testid="stMetricValue"] {
        color: #c0c0c0 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }

    [data-testid="stMetricLabel"] {
        color: #a8a8a8 !important;
    }

    [data-testid="stDataFrame"] {
        background-color: #1a1a1a !important;
    }

    [role="tablist"] {
        border-bottom: 2px solid #404040 !important;
    }

    [role="tab"] {
        color: #a8a8a8 !important;
        border-bottom: 2px solid transparent !important;
    }

    [role="tab"][aria-selected="true"] {
        color: #c0c0c0 !important;
        border-bottom: 2px solid #c0c0c0 !important;
    }

    input, textarea, select {
        background-color: #1a1a1a !important;
        border: 1px solid #404040 !important;
        color: #e8e8e8 !important;
        border-radius: 6px !important;
    }

    input:focus, textarea:focus, select:focus {
        border: 2px solid #c0c0c0 !important;
        box-shadow: 0 0 8px rgba(192, 192, 192, 0.2) !important;
    }
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------
# SESSION STATE
# -------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []

# -------------------------------
# LIVE MARKET DATA
# -------------------------------
TODAY_RATES = {
    "gold": {"current": 7850, "previous": 7800, "change": 50, "change_percent": 0.64, "currency": "₹", "unit": "per gram"},
    "silver": {"current": 95, "previous": 92, "change": 3, "change_percent": 3.26, "currency": "₹", "unit": "per gram"},
}

# -------------------------------
# CUSTOMER DATA (single sample) - keep as-is
# -------------------------------
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

# -------------------------------
# Mock data loaders (v4 features)
# -------------------------------
def load_mock_customers(seed=42):
    np.random.seed(seed)
    customers = []
    names = ["Rajesh Kumar", "Priya Singh", "Amit Patel", "Deepika Sharma", "Vikram Gupta", "Neha Verma", "Sanjay Pillai", "Anjali Nair", "Rohit Singh", "Pooja Reddy", "Arjun Rao", "Divya Joshi"]
    tiers = ["VIP", "Regular", "Dormant"]
    for i, name in enumerate(names * 5):
        tier_idx = np.random.randint(0, 3)
        customers.append({
            "id": i + 1,
            "name": f"{name}_{i+1}",
            "phone": f"98{np.random.randint(1000000,9999999)}",
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

def load_mock_chit_schedule(seed=42):
    np.random.seed(seed)
    chits = []
    chit_groups = ["Group A", "Group B", "Group C"]
    payout_amounts = [100000, 150000, 200000]
    for i in range(10):
        group_idx = np.random.randint(0, len(chit_groups))
        payout_idx = np.random.randint(0, len(payout_amounts))
        chits.append({
            "id": i + 1,
            "customer_id": np.random.randint(1, 61),
            "chit_group": chit_groups[group_idx],
            "payout_date": (datetime.now() + timedelta(days=int(np.random.randint(5, 60)))).date(),
            "payout_amount": payout_amounts[payout_idx],
            "expected_spending": np.random.uniform(50000, 150000),
        })
    return pd.DataFrame(chits)

# -------------------------------
# Extended pages & functions (v4 -> v5 merge)
# -------------------------------
def get_accessible_pages(role):
    pages = {
        "Manager": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot",
            "🤖 ML Models",
            "💎 Chit Management",
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
            "🔎 Integrated Chatbot",
            "👨‍💼 Staff Dashboard",
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
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Smart Commands",
            "💬 Chatbot",
            "🔎 Integrated Chatbot",
            "🤖 ML Models",
            "💎 Chit Management",
            "⚙️ Advanced Settings",
            "⚙️ Settings",
        ],
    }
    return pages.get(role, [])

# -------------------------------
# Login page (same as v5)
# -------------------------------
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("### Premium Management System for Indian Jewellery Retail")
        st.divider()

        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer", "Admin"], horizontal=True, key="login_type")
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
        elif login_type == "Customer":
            st.subheader("🛍️ Customer Login")
            username = st.text_input("Username", key="cust_user_id")
            password = st.text_input("Password", type="password", key="cust_pass_id")
            if st.button("🔓 Login", use_container_width=True, key="cust_btn"):
                if username == "customer" and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        else:
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
        st.divider()
        st.markdown(
            """
        ### 📝 Demo Credentials:
        **Manager:** username: `manager` | password: `manager123`  
        **Staff:** username: `staff` | password: `staff123`  
        **Customer:** username: `customer` | password: `customer123`  
        **Admin:** username: `admin` | password: `admin123`
        """
        )

# -------------------------------
# Customer Dashboard (v5)
# -------------------------------
def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)
    customer = CUSTOMER_DATA["customer"]
    st.markdown(
        f"""
    <div class='info-box'>
    <strong>👋 Welcome, {customer['name']}!</strong><br>
    <strong>Member Since:</strong> {customer['joining_date']} | 
    <strong>Status:</strong> {customer['tier']} Tier | 
    <strong>Loyalty Points:</strong> ⭐ {customer['loyalty_points']}
    </div>
    """,
        unsafe_allow_html=True,
    )
    st.divider()

    st.subheader("💰 Today's Live Market Rates")
    col1, col2 = st.columns(2)
    with col1:
        gold = TODAY_RATES["gold"]
        change_color = "🟢" if gold["change"] >= 0 else "🔴"
        st.markdown(
            f"""
        <div class='gold-box'>
            <h3>💛 GOLD</h3>
            <h2>₹{gold['current']}/{gold['unit']}</h2>
            <p>{change_color} {gold['currency']}{gold['change']} ({gold['change_percent']:.2f}%)</p>
            <small>Previous: ₹{gold['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col2:
        silver = TODAY_RATES["silver"]
        change_color = "🟢" if silver["change"] >= 0 else "🔴"
        st.markdown(
            f"""
        <div class='silver-box'>
            <h3>🤍 SILVER</h3>
            <h2>₹{silver['current']}/{silver['unit']}</h2>
            <p>{change_color} {silver['currency']}{silver['change']} ({silver['change_percent']:.2f}%)</p>
            <small>Previous: ₹{silver['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """,
            unsafe_allow_html=True,
        )
    st.divider()

    st.subheader("📊 Your Account Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Spent", f"₹{customer['total_spent']:,}", f"₹{customer['total_spent']//12:,.0f}/year")
    with col2:
        st.metric("🛍️ Purchases", f"{customer['total_purchases']}", f"Last: {customer['last_purchase']}")
    with col3:
        st.metric("⭐ Loyalty Points", f"{customer['loyalty_points']}", "100pts = ₹50")
    with col4:
        st.metric("💎 Your Tier", customer["tier"], "Premium Member")

    st.divider()
    st.subheader("🛍️ Your Purchase History")
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    purchases_df = purchases_df[["date", "item", "purity", "weight", "amount", "status"]]
    purchases_df.columns = ["Date", "Item", "Purity", "Weight", "Amount (₹)", "Status"]
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Purchases", f"{len(CUSTOMER_PURCHASES)}", "items")
    with col2:
        total_amount = sum([p["amount"] for p in CUSTOMER_PURCHASES])
        st.metric("Total Amount", f"₹{total_amount:,}", "all purchases")
    with col3:
        avg_amount = total_amount // len(CUSTOMER_PURCHASES)
        st.metric("Average Purchase", f"₹{avg_amount:,}", "per transaction")

    st.divider()
    st.subheader("⚠️ Pending Payments")
    if PENDING_PAYMENTS:
        for payment in PENDING_PAYMENTS:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"**Item:** {payment['item']}")
            with col2:
                st.markdown(f"**Amount:** ₹{payment['amount']:,}")
            with col3:
                st.markdown(f"**Due Date:** {payment['due_date']}")
            with col4:
                st.markdown(f"**Status:** 🔴 {payment['status']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💳 Pay Now", use_container_width=True, key=f"pay_{payment['item']}"):
                    st.success(f"✅ Payment of ₹{payment['amount']:,} processed successfully!")
            with col2:
                if st.button("📅 Schedule Payment", use_container_width=True, key=f"schedule_{payment['item']}"):
                    st.info("📅 Payment scheduled for " + payment["due_date"])
            st.divider()
    else:
        st.success("✅ No pending payments! You're all caught up!")

    st.divider()
    st.subheader("🎯 Active Campaign Notifications")
    st.markdown(
        """
    <div class='info-box'>
    <strong>🎉 You have 4 active offers & campaigns!</strong><br>
    Browse the latest deals tailored for Gold tier members like you.
    </div>
    """,
        unsafe_allow_html=True,
    )
    for campaign in CAMPAIGN_NOTIFICATIONS:
        st.markdown(
            f"""
        <div class='campaign-notification'>
            <h4>{campaign['title']}</h4>
            <strong style='color: #ffd700; font-size: 1.2rem;'>{campaign['discount']}</strong><br>
            📝 {campaign['description']}<br>
            ⏰ <small>Valid: {campaign['valid']}</small> | 
            <strong style='color: #7cb342;'>✅ {campaign['status']}</strong>
        </div>
        """,
            unsafe_allow_html=True,
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🔖 Learn More", use_container_width=True, key=f"learn_{campaign['title']}"):
                st.info(f"📌 {campaign['title']}: {campaign['description']}")
        with col2:
            if st.button(f"🛍️ Shop Now", use_container_width=True, key=f"shop_{campaign['title']}"):
                st.success("✅ Redirecting to shop... (in app)")
        st.divider()

# -------------------------------
# Dashboard page (v5)
# -------------------------------
def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    dates = pd.date_range(start="2025-11-01", end="2025-12-11", freq="D")
    sales_data = np.random.randint(50000, 200000, len(dates))
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Sales", f"₹{sum(sales_data):,}", "+₹5,000")
    with col2:
        st.metric("👥 Total Customers", "1,250", "+45")
    with col3:
        st.metric("📦 Stock Value", "₹45,00,000", "-₹2,00,000")
    with col4:
        st.metric("💎 Active Chits", "85", "+12")
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📈 Sales Trend (Nov-Dec 2025)")
        fig = px.line(x=dates, y=sales_data, title="Daily Sales Trend")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Sales (₹)")
        fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ["Gold", "Silver", "Diamond", "Platinum"]
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Product Sales by Category")
        fig.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    st.divider()
    st.subheader("📋 Recent Transactions")
    transactions_df = pd.DataFrame({
        "Transaction ID": ["TXN001", "TXN002", "TXN003", "TXN004", "TXN005"],
        "Customer": ["Rajesh Patel", "Priya Singh", "Amit Kumar", "Neha Sharma", "Vikram Gupta"],
        "Amount": ["₹45,000", "₹32,000", "₹18,000", "₹22,000", "₹8,000"],
        "Date": ["2025-12-10", "2025-12-09", "2025-12-08", "2025-12-07", "2025-12-06"],
        "Status": ["✅ Completed", "✅ Completed", "⏳ Pending", "✅ Completed", "✅ Completed"],
    })
    st.dataframe(transactions_df, use_container_width=True, hide_index=True)

# -------------------------------
# Customers page (v5)
# -------------------------------
def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    # -----------------------------
    # Load customer data
    # -----------------------------
    customers_df = load_mock_customers()

    # 🔧 FIX: Ensure last_visit is datetime
    customers_df["last_visit"] = pd.to_datetime(customers_df["last_visit"])

    # -----------------------------
    # Tabs (like your screenshot)
    # -----------------------------
    tab_all, tab_risk, tab_vip, tab_pending = st.tabs(
        ["All Customers", "At Risk", "VIP Management", "Pending Customers"]
    )

    # -----------------------------
    # Search & Filter Row
    # -----------------------------
    col1, col2 = st.columns([3, 1])

    with col1:
        search = st.text_input("🔍 Search by name or phone", placeholder="Type name or phone...")

    with col2:
        tier_filter = st.selectbox("Filter by Tier", ["All", "VIP", "Regular", "Dormant"])

    # -----------------------------
    # Apply Filters
    # -----------------------------
    filtered_df = customers_df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["name"].str.contains(search, case=False)
            | filtered_df["phone"].str.contains(search, case=False)
        ]

    if tier_filter != "All":
        filtered_df = filtered_df[filtered_df["tier"] == tier_filter]

    # -----------------------------
    # KPI METRICS (Top Row)
    # -----------------------------
    total_found = len(filtered_df)
    total_pending = int(filtered_df["pending_amount"].sum())
    total_spent = int(filtered_df["total_spent"].sum())

    k1, k2, k3 = st.columns(3)
    with k1:
        st.metric("Total Found", total_found)
    with k2:
        st.metric("Total Pending", f"₹{total_pending:,.0f}")
    with k3:
        st.metric("Total Spent", f"₹{total_spent:,.0f}")

    st.divider()

    # =============================
    # TAB 1: ALL CUSTOMERS
    # =============================
    with tab_all:
        display_df = filtered_df[
            ["name", "phone", "email", "total_spent", "pending_amount", "tier"]
        ].copy()

        display_df["total_spent"] = display_df["total_spent"].apply(lambda x: f"₹{x:,.0f}")
        display_df["pending_amount"] = display_df["pending_amount"].apply(lambda x: f"₹{x:,.0f}")

        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # =============================
    # TAB 2: AT RISK (FIXED)
    # =============================
    with tab_risk:
        customers_df["days_since_visit"] = (
            datetime.now() - customers_df["last_visit"]
        ).dt.days

        risk_df = customers_df[
            (customers_df["pending_amount"] > 50000)
            | (customers_df["days_since_visit"] > 120)
        ].copy()

        st.warning(f"⚠️ {len(risk_df)} customers at risk")

        st.dataframe(
            risk_df[
                ["name", "phone", "pending_amount", "last_visit", "tier"]
            ],
            use_container_width=True,
            hide_index=True,
        )

    # =============================
    # TAB 3: VIP MANAGEMENT
    # =============================
    with tab_vip:
        vip_df = customers_df[customers_df["tier"] == "VIP"].copy()

        st.success(f"⭐ VIP Customers: {len(vip_df)}")

        st.dataframe(
            vip_df[
                ["name", "phone", "total_spent", "pending_amount", "last_visit"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        if st.button("🎁 Send VIP Offer"):
            st.success("VIP offers sent successfully!")

    # =============================
    # TAB 4: PENDING CUSTOMERS
    # =============================
    with tab_pending:
        pending_df = customers_df[customers_df["pending_amount"] > 0].copy()

        st.info(f"💰 Customers with pending payments: {len(pending_df)}")

        st.dataframe(
            pending_df[
                ["name", "phone", "pending_amount", "tier", "last_visit"]
            ],
            use_container_width=True,
            hide_index=True,
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("📩 Send Payment Reminder"):
                st.success("Payment reminders sent!")
        with col2:
            if st.button("⬇️ Export Pending CSV"):
                csv = pending_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download pending_customers.csv",
                    data=csv,
                    file_name="pending_customers.csv",
                    mime="text/csv",
                )


# -------------------------------
# Inventory page (v5)
# -------------------------------
def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)
    inventory_df = pd.DataFrame({
        "Item Code": ["GLD001", "SLV002", "DMD003", "PLT004", "GLD005"],
        "Item Name": ["Gold Ring", "Silver Bracelet", "Diamond Pendant", "Platinum Ring", "Gold Necklace"],
        "Category": ["Gold", "Silver", "Diamond", "Platinum", "Gold"],
        "Quantity": [45, 120, 15, 8, 32],
        "Unit Price": ["₹15,000", "₹2,000", "₹50,000", "₹75,000", "₹22,000"],
        "Status": ["✅ In Stock", "✅ In Stock", "⚠️ Low Stock", "🔴 Critical", "✅ In Stock"],
    })
    st.subheader("Current Inventory")
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Stock by Category")
        stock_data = pd.DataFrame({"Category": ["Gold", "Silver", "Diamond", "Platinum"], "Items": [45, 120, 15, 8]})
        fig = px.bar(stock_data, x="Category", y="Items", title="Items by Category", color="Category")
        fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader("💰 Inventory Value by Category")
        value_data = pd.DataFrame({"Category": ["Gold", "Silver", "Diamond", "Platinum"], "Value": [675000, 240000, 750000, 600000]})
        fig = px.pie(value_data, values="Value", names="Category", title="Inventory Value")
        fig.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)

# -------------------------------
# Tax & Compliance (v5)
# -------------------------------
def tax_compliance_page():
    st.markdown("<h2 class='main-title'>💰 Tax & Compliance</h2>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊 Tax Summary", "📋 GST Details", "📑 Reports"])
    with tab1:
        st.subheader("Tax Overview")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📅 Current Period", "Q4 2025", "Oct-Dec")
        with col2:
            st.metric("💵 Taxable Income", "₹25,00,000", "+₹3,00,000")
        with col3:
            st.metric("🏦 Tax Liability", "₹3,75,000", "18%")
        with col4:
            st.metric("✅ Paid", "₹2,50,000", "67%")
    with tab2:
        st.subheader("GST Compliance")
        gst_df = pd.DataFrame({
            "Month": ["October", "November", "December"],
            "Sales": ["₹15,00,000", "₹18,00,000", "₹22,00,000"],
            "GST Rate": ["18%", "18%", "18%"],
            "GST Amount": ["₹2,70,000", "₹3,24,000", "₹3,96,000"],
            "Status": ["✅ Filed", "✅ Filed", "⏳ Pending"],
        })
        st.dataframe(gst_df, use_container_width=True, hide_index=True)
    with tab3:
        st.subheader("Generate Tax Reports")
        report_type = st.selectbox("Select Report Type", ["Monthly Summary", "Quarterly Filing", "Annual Return"])
        if st.button("📥 Generate Report"):
            st.success(f"✅ {report_type} generated successfully!")

# -------------------------------
# Campaigns page (v5)
# -------------------------------
def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)

    tab_create, tab_active, tab_reports = st.tabs(
        ["Create Campaign", "Active Campaigns", "Campaign Reports"]
    )

    # ==========================
    # CREATE CAMPAIGN
    # ==========================
    with tab_create:
        st.subheader("Create New Campaign")

        # Campaign basic info
        st.text_input("Campaign Name", placeholder="e.g. Diwali 2025")

        st.selectbox(
            "Campaign Type",
            ["Payment Reminder", "Festival Offer", "VIP Exclusive", "Clearance Sale"]
        )

        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date")
        with col2:
            end_date = st.date_input("End Date")

        st.divider()

        # Target audience
        st.markdown("### Target Audience")
        col1, col2, col3 = st.columns(3)
        with col1:
            target_vip = st.checkbox("Target VIP Customers", value=True)
        with col2:
            target_regular = st.checkbox("Target Regular Customers", value=True)
        with col3:
            target_dormant = st.checkbox("Target Dormant Customers")

        st.divider()

        # Message content
        st.markdown("### Message Content")
        message = st.text_area(
            "Campaign Message",
            height=120,
            value="Hi there! 👋\n\nWe have an exciting offer for you.\n\nCome visit us today!"
        )

        col1, col2 = st.columns(2)
        with col1:
            discount = st.slider("Discount Percentage", 0, 50, 10)
        with col2:
            min_purchase = st.number_input(
                "Minimum Purchase Amount",
                min_value=0,
                step=1000,
                value=10000
            )

        st.divider()

        # Channels
        st.markdown("### Channel")
        col1, col2, col3 = st.columns(3)
        with col1:
            ch_whatsapp = st.checkbox("WhatsApp", value=True)
        with col2:
            ch_email = st.checkbox("Email")
        with col3:
            ch_sms = st.checkbox("SMS")

        st.divider()

        # Launch
        if st.button("🚀 Launch Campaign", use_container_width=True):
            if not (ch_whatsapp or ch_email or ch_sms):
                st.error("Please select at least one channel")
            else:
                st.success("✅ Campaign launched successfully!")
                st.info(
                    f"""
                    **Summary**
                    - Discount: {discount}%
                    - Min Purchase: ₹{min_purchase:,.0f}
                    - Channels: {', '.join([c for c, v in {
                        'WhatsApp': ch_whatsapp,
                        'Email': ch_email,
                        'SMS': ch_sms
                    }.items() if v])}
                    """
                )

    # ==========================
    # ACTIVE CAMPAIGNS
    # ==========================
    with tab_active:
        st.subheader("Active Campaigns")

        active_df = pd.DataFrame({
            "Campaign": ["Diwali Sale", "VIP Reminder", "Wedding Season"],
            "Type": ["Festival Offer", "Payment Reminder", "Seasonal"],
            "Start Date": ["2025-10-15", "2025-12-01", "2025-11-20"],
            "End Date": ["2025-11-15", "2025-12-31", "2026-03-31"],
            "Discount": ["20%", "-", "15%"],
            "Channel": ["WhatsApp", "WhatsApp + SMS", "Email"],
            "Status": ["🟢 Active", "🟢 Active", "🟢 Active"]
        })

        st.dataframe(active_df, use_container_width=True, hide_index=True)

    # ==========================
    # CAMPAIGN REPORTS
    # ==========================
    with tab_reports:
        st.subheader("Campaign Performance")

        report_df = pd.DataFrame({
            "Campaign": ["Diwali Sale", "VIP Reminder"],
            "Sent": [1250, 320],
            "Responses": [340, 190],
            "Conversions": [180, 95],
            "Revenue Generated": ["₹12,50,000", "₹6,80,000"]
        })

        st.dataframe(report_df, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Revenue", "₹19,30,000")
        with col2:
            st.metric("Avg Conversion Rate", "28%")

# -------------------------------
# Staff Management page (v5)
# -------------------------------
def staff_management_page():
    st.markdown("<h2 class='main-title'>👨‍💼 Staff Management</h2>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["📊 Staff Directory", "💰 Pending Amounts"])
    with tab1:
        st.subheader("Staff Directory")
        staff_df = pd.DataFrame({
            "Name": ["Ram Kumar", "Priya Singh", "Amit Verma", "Neha Sharma", "Vikram Gupta"],
            "Position": ["Sales Executive", "Manager", "Sales Associate", "Cashier", "Showroom Lead"],
            "Department": ["Sales", "Management", "Sales", "Operations", "Sales"],
            "Joining Date": ["2022-01-15", "2021-03-20", "2023-06-10", "2022-11-05", "2023-02-14"],
            "Status": ["✅ Active", "✅ Active", "✅ Active", "✅ Active", "✅ Active"],
        })
        st.dataframe(staff_df, use_container_width=True, hide_index=True)
    with tab2:
        st.subheader("💸 Pending Commission/Amount")
        pending_df = pd.DataFrame({
            "Staff Name": ["Ram Kumar", "Priya Singh", "Amit Verma", "Neha Sharma"],
            "Position": ["Sales Executive", "Manager", "Sales Associate", "Cashier"],
            "Pending Amount": ["₹15,000", "₹8,500", "₹12,000", "₹5,500"],
            "Due Date": ["2025-12-15", "2025-12-20", "2025-12-18", "2025-12-15"],
            "Status": ["⏳ Pending", "⏳ Pending", "⏳ Pending", "⏳ Pending"],
        })
        st.dataframe(pending_df, use_container_width=True, hide_index=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("💳 Pay All Pending", use_container_width=True):
                st.success("✅ All pending amounts paid!")
        with col2:
            if st.button("📧 Send Reminder", use_container_width=True):
                st.info("✉️ Reminders sent to all staff!")

# -------------------------------
# Staff Dashboard (new)
# -------------------------------
def staff_dashboard_page():
    st.markdown("<h2 class='main-title'>👨‍💼 Staff Dashboard</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📅 Today Sales (est.)", "₹1,85,000", "+12%")
    with col2:
        st.metric("🧾 Pending Orders", "8", "⏳")
    with col3:
        st.metric("📈 Target Progress", "72%", "₹7.2L / ₹10L")
    with col4:
        st.metric("👥 Customers Served", "24", "+3")
    st.divider()
    st.subheader("⚡ Quick Staff Actions")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔔 Show Pending Commissions", use_container_width=True):
            pending_df = pd.DataFrame.from_records([{"Staff Name": v["name"], "Position": v["position"], "Pending Amount": v["pending"]} for k, v in STAFF_MEMBERS.items()])
            st.dataframe(pending_df, use_container_width=True)
    with col2:
        if st.button("📦 Today's Shipments", use_container_width=True):
            st.info("✅ All shipments processed: 12")
    with col3:
        if st.button("📥 Export Sales (CSV)", use_container_width=True):
            sales_example = pd.DataFrame({"Date": ["2025-12-10", "2025-12-09"], "Item": ["Gold Ring", "Silver Bracelet"], "Amount": [45000, 8000]})
            csv = sales_example.to_csv(index=False).encode("utf-8")
            st.download_button("Download sales.csv", data=csv, file_name="sales_today.csv", mime="text/csv")
    st.divider()
    st.subheader("📋 Today's Tasks & Recent Sales")
    sales_df = pd.DataFrame({"Date": ["2025-12-10", "2025-12-09", "2025-12-08"], "Item": ["Gold Ring", "Silver Bracelet", "Diamond Pendant"], "Amount": ["₹45,000", "₹8,000", "₹55,000"], "Status": ["Completed", "Completed", "Pending"]})
    st.dataframe(sales_df, use_container_width=True)

# -------------------------------
# AI Assistant (v5)
# -------------------------------
def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'><strong>🤖 Jewellery Shop AI Assistant</strong><br>Get instant insights, recommendations, and automated suggestions for your jewellery business!</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["💡 Insights", "📊 Recommendations", "🔍 Analytics"])
    with tab1:
        st.subheader("💡 AI Business Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("✅ **Sales Trend Analysis**\n- Sales trending upward by 15% this month\n- Peak sales time: 2 PM - 5 PM\n- Best selling category: Gold (45%)\n\n💡 **Recommendation:** Stock more gold items during peak hours")
        with col2:
            st.markdown("👥 **Customer Insights**\n- 87% customers are repeat buyers\n- Average customer lifetime value: ₹2,50,000\n- Premium tier customers spend 4x more\n\n💡 **Recommendation:** Focus on premium customer retention")
        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("📦 **Inventory Optimization**\n- Platinum inventory critical (8 items)\n- Silver stock high (120 items)\n- Estimated stockout: 5 days for diamonds\n\n💡 **Recommendation:** Reorder platinum immediately")
        with col2:
            st.markdown("💰 **Profit Analysis**\n- Average profit margin: 28%\n- Peak profit items: Diamond (35% margin)\n- Low margin items: Silver (12% margin)\n\n💡 **Recommendation:** Push diamond sales for better margins")
    with tab2:
        st.subheader("📊 AI Recommendations")
        recommendations = [
            "🎯 Launch 'Diamond Premium' campaign - predicted ROI: 320%",
            "👥 Create loyalty program for premium customers - estimated 25% increase in repeat purchases",
            "📦 Implement dynamic pricing for high-demand items",
            "🌍 Expand online presence - untapped market worth ₹50L+",
            "⏰ Shift staff schedule to peak hours - 40% efficiency gain",
            "💳 Introduce EMI option - predicted 18% sales increase",
        ]
        for i, rec in enumerate(recommendations, 1):
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown(f"**{i}.**")
            with col2:
                st.markdown(rec)
    with tab3:
        st.subheader("🔍 Advanced Analytics")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**📈 Predictive Sales Forecast**")
            forecast_data = pd.DataFrame({"Month": ["Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026"], "Predicted Sales": [65, 72, 68, 85], "Confidence": ["92%", "88%", "85%", "80%"]})
            st.dataframe(forecast_data, hide_index=True)
        with col2:
            st.markdown("**👥 Customer Segmentation**")
            segment_data = pd.DataFrame({"Segment": ["Premium", "Gold", "Silver", "Standard"], "Count": [125, 320, 580, 225], "Value": ["₹2,50L", "₹1,60L", "₹87.5L", "₹22.5L"]})
            st.dataframe(segment_data, hide_index=True)

# -------------------------------
# Smart Commands (v5)
# -------------------------------
def smart_commands_page():
    st.markdown("<h2 class='main-title'>💬 Smart Commands</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>AI Command Center</strong><br>
    Use natural language to query data or execute actions.<br>
    Examples:
    <ul>
      <li><code>alert ram about pending</code></li>
      <li><code>show customer rajesh</code></li>
      <li><code>purchases for rajesh</code></li>
      <li><code>pending payments</code></li>
      <li><code>export customers</code></li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

    if "smart_chat" not in st.session_state:
        st.session_state.smart_chat = []

    # Show chat history
    for msg in st.session_state.smart_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Input
    prompt = st.chat_input("Enter a command or question")

    if not prompt:
        return

    # Save user message
    st.session_state.smart_chat.append({"role": "user", "content": prompt})
    q = prompt.lower()

    # -----------------------------
    # COMMAND PARSING
    # -----------------------------
    response = None

    # ---- STAFF ALERTS ----
    staff = {
        "ram": "Ram Kumar",
        "priya": "Priya Singh",
        "amit": "Amit Verma",
        "neha": "Neha Sharma"
    }

    if "alert" in q or "notify" in q:
        for key, name in staff.items():
            if key in q:
                response = f"🔔 Alert sent to **{name}**"
                break
        if "all" in q:
            response = "📢 Alert sent to **all staff members**"

    # ---- CUSTOMER LOOKUP ----
    elif "show customer" in q:
        cust = CUSTOMER_DATA["customer"]
        if cust["id"].lower() in q or cust["name"].lower().split()[0] in q:
            response = "### 👤 Customer Details"
            st.session_state.smart_chat.append({"role": "assistant", "content": response})
            st.dataframe(pd.DataFrame([cust]), use_container_width=True)
            return
        else:
            response = "❌ Customer not found"

    # ---- PURCHASES ----
    elif "purchase" in q:
        response = "### 🧾 Purchase History"
        st.session_state.smart_chat.append({"role": "assistant", "content": response})
        st.dataframe(pd.DataFrame(CUSTOMER_PURCHASES), use_container_width=True)
        return

    # ---- PENDING PAYMENTS ----
    elif "pending" in q or "due" in q:
        response = "### ⚠️ Pending Payments"
        st.session_state.smart_chat.append({"role": "assistant", "content": response})
        st.dataframe(pd.DataFrame(PENDING_PAYMENTS), use_container_width=True)
        return

    # ---- EXPORT ----
    elif "export" in q:
        df = pd.DataFrame([CUSTOMER_DATA["customer"]])
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Download customers.csv",
            data=csv,
            file_name="customers.csv",
            mime="text/csv"
        )
        response = "📥 Customer data exported"

    # ---- HELP ----
    elif "help" in q:
        response = """
**Available Commands**
- alert ram / notify all staff
- show customer <name/id>
- purchases for <name>
- pending payments
- export customers
"""

    else:
        response = "🤖 I didn’t understand that. Type `help` to see commands."

    # Save response
    st.session_state.smart_chat.append({"role": "assistant", "content": response})

    st.rerun()


# -------------------------------
# Chatbot (original v5)
# -------------------------------
def chatbot_page():
    st.markdown("<h2 class='main-title'>💬 Smart Chatbot</h2>", unsafe_allow_html=True)
    st.subheader("🎯 Quick Help Topics")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📦 Purchase Help", use_container_width=True, key="cb_purchase"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "📦 You have 4 purchases. Latest: Gold Ring (Dec 10, ₹15,000) ✅"}]
            st.rerun()
    with col2:
        if st.button("💎 Chit Support", use_container_width=True, key="cb_chit"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "💎 Active chits: Gold 12-Month & Diamond Savings"}]
            st.rerun()
    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True, key="cb_loyalty"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "🎁 Gold Tier - 890 points. 100 points = ₹50 discount!"}]
            st.rerun()
    st.divider()
    if st.session_state.chatbot_messages:
        for message in st.session_state.chatbot_messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
                else:
                    st.markdown(message["content"])
    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        response = "How can I help you?"
        if any(word in prompt.lower() for word in ["purchase", "buy"]):
            response = "📦 Your purchases are delivered!"
        elif any(word in prompt.lower() for word in ["chit", "payment"]):
            response = "💎 Next payment due Dec 15"
        elif any(word in prompt.lower() for word in ["loyalty", "points"]):
            response = "🎁 Gold tier with 890 points!"
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        st.rerun()

# -------------------------------
# ML Models page (v4 feature)
# -------------------------------
def show_ml_models():
    st.markdown("<h2 class='main-title'>🤖 ML Models</h2>", unsafe_allow_html=True)
    customers_df = load_mock_customers()
    transactions_df = load_mock_transactions()
    tab1, tab2, tab3 = st.tabs(["Churn Prediction", "Demand Forecast", "Dynamic Pricing"])
    with tab1:
        st.subheader("Customer Churn Risk Prediction")
        today = datetime.now().date()
        customers_df_copy = customers_df.copy()
        customers_df_copy["recency_days"] = (today - customers_df_copy["last_visit"]).apply(lambda x: x.days)
        customers_df_copy["churn_risk"] = (
            (customers_df_copy["recency_days"] / 180 * 50)
            + (customers_df_copy["pending_amount"] / (customers_df_copy["pending_amount"].max() or 1) * 30)
            + np.random.normal(10, 5, len(customers_df_copy))
        )
        customers_df_copy["churn_risk"] = customers_df_copy["churn_risk"].clip(0, 100)
        high_risk = customers_df_copy[customers_df_copy["churn_risk"] > 60].copy()
        st.warning(f"🚨 {len(high_risk)} customers at HIGH risk of churn")
        high_risk_display = high_risk[["name", "phone", "pending_amount", "last_visit"]].copy()
        high_risk_display["churn_risk"] = high_risk["churn_risk"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(high_risk_display, use_container_width=True)
        if st.button("📢 Send Retention Offers to High-Risk Customers"):
            st.success(f"✅ Sent retention offers to {len(high_risk)} customers")
    with tab2:
        st.subheader("60-Day Demand Forecast")
        dates = pd.date_range(start=datetime.now().date(), periods=60)
        forecast_values = np.random.normal(2.5, 0.8, 60) * 100000
        forecast_values = np.maximum(forecast_values, 500000)
        forecast_df = pd.DataFrame({"date": dates, "forecast": forecast_values, "upper_bound": forecast_values * 1.2, "lower_bound": forecast_values * 0.8})
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["forecast"], mode="lines", name="Forecast"))
        fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["upper_bound"], fill=None, mode="lines", name="Upper Bound"))
        fig.add_trace(go.Scatter(x=forecast_df["date"], y=forecast_df["lower_bound"], fill="tonexty", mode="lines", name="Lower Bound"))
        st.plotly_chart(fig, use_container_width=True)
        total_forecast = forecast_df["forecast"].sum()
        st.metric("60-Day Total Forecast", f"₹{total_forecast:,.0f}")
    with tab3:
        st.subheader("💰 Dynamic Pricing Recommendations")
        selected_customer = st.selectbox("Select Customer", customers_df["name"].values)
        customer = customers_df[customers_df["name"] == selected_customer].iloc[0]
        base_price = 45000
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Cost", f"₹{base_price * 0.4:,.0f}")
        with col2:
            st.metric("Standard Price", f"₹{base_price:,.0f}")
        with col3:
            if customer["tier"] == "VIP":
                recommended = base_price * 1.08
                margin = "+15%"
            elif customer["tier"] == "Regular":
                recommended = base_price * 0.95
                margin = "+12%"
            else:
                recommended = base_price * 0.85
                margin = "+10%"
            st.metric("Recommended Price", f"₹{recommended:,.0f}", delta=margin)

# -------------------------------
# Chit Fund Management page (v4 feature)
# -------------------------------
def show_chit_management():
    st.markdown("<h2 class='main-title'>💎 Chit Fund Management</h2>", unsafe_allow_html=True)
    chit_df = load_mock_chit_schedule()
    tab1, tab2 = st.tabs(["Chit Schedule", "Pre-Order Planning"])
    with tab1:
        st.subheader("Upcoming Chit Payouts (Next 60 Days)")
        today = datetime.now().date()
        upcoming = chit_df[(chit_df["payout_date"] >= today) & (chit_df["payout_date"] <= today + timedelta(days=60))].copy()
        st.metric("Upcoming Payouts", len(upcoming))
        if len(upcoming) > 0:
            display_df = upcoming[["chit_group", "payout_date", "payout_amount", "expected_spending"]].copy()
            display_df["payout_amount"] = display_df["payout_amount"].apply(lambda x: f"₹{x:,.0f}")
            display_df["expected_spending"] = display_df["expected_spending"].apply(lambda x: f"₹{x:,.0f}")
            st.dataframe(display_df, use_container_width=True)
            total_expected = upcoming["expected_spending"].sum()
            st.metric("Total Expected Orders", f"₹{total_expected:,.0f}")
        else:
            st.info("ℹ️ No upcoming chit payouts")
    with tab2:
        st.subheader("🛍️ Pre-Order Recommendations")
        today = datetime.now().date()
        upcoming = chit_df[(chit_df["payout_date"] >= today) & (chit_df["payout_date"] <= today + timedelta(days=60))].copy()
        if len(upcoming) > 0:
            st.info(f"Pre-book inventory for {len(upcoming)} upcoming chit payouts")
            high_value = upcoming[upcoming["expected_spending"] > 100000]["expected_spending"].sum()
            medium_value = upcoming[(upcoming["expected_spending"] >= 50000) & (upcoming["expected_spending"] <= 100000)]["expected_spending"].sum()
            low_value = upcoming[upcoming["expected_spending"] < 50000]["expected_spending"].sum()
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Premium Designs", f"₹{high_value:,.0f}")
            with col2:
                st.metric("Regular Designs", f"₹{medium_value:,.0f}")
            with col3:
                st.metric("Light Designs", f"₹{low_value:,.0f}")
            if st.button("📋 Generate Pre-Order List"):
                st.success("✅ Pre-order list generated")
                st.write(
                    """
                **Recommended Stock:**
                - Premium rings/necklaces: 8-10 pieces
                - Regular bangles/sets: 15-20 pieces
                - Light earrings/pendants: 20-25 pieces
                """
                )
        else:
            st.info("ℹ️ No upcoming chit payouts in next 60 days")

# -------------------------------
# Advanced Settings (v4 feature, non-destructive)
# -------------------------------
def show_settings_v4():
    st.markdown("<h2 class='main-title'>⚙️ Advanced Settings</h2>", unsafe_allow_html=True)
    if st.session_state.get("user_role") not in ("Admin", "Manager"):
        st.error("Only Admin or Manager can access advanced settings")
        return
    tab1, tab2, tab3 = st.tabs(["System", "WhatsApp", "Integrations"])
    with tab1:
        st.subheader("System Settings")
        shop_name = st.text_input("Shop Name", value="Shree Jewels")
        shop_email = st.text_input("Shop Email", value="contact@shreejewels.com")
        shop_phone = st.text_input("Shop Phone", value="+91 98765 43210")
        if st.button("💾 Save Settings (Advanced)"):
            st.success("✅ Settings saved")
    with tab2:
        st.subheader("WhatsApp Integration (Demo)")
        phone_number_id = st.text_input("Phone Number ID", type="password", value="")
        access_token = st.text_input("Access Token", type="password", value="")
        if st.button("🧪 Test WhatsApp Connection"):
            if phone_number_id and access_token:
                st.success("✅ WhatsApp API connected successfully (demo)")
            else:
                st.warning("⚠️ Please enter API credentials first")
    with tab3:
        st.subheader("Third-Party Integrations")
        openai_key = st.text_input("OpenAI API Key (optional)", type="password", value="")
        db_connection = st.selectbox("Database", ["SQLite", "PostgreSQL", "MySQL"])
        if st.button("💾 Save Integrations"):
            st.success("✅ Integrations configured")

# -------------------------------
# Original v5 Settings page left intact (named settings_page)
# -------------------------------
def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    st.subheader("Account Settings")
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Full Name", value="Manager")
        st.text_input("Email", value="manager@jewellery.com")
    with col2:
        st.text_input("Phone", value="+91-XXXXXXXXXX")
        st.selectbox("Theme", ["Luxury Black & Silver ⭐ CURRENT", "Light Mode", "Other"], index=0)
    if st.button("💾 Save Settings"):
        st.success("✅ Settings saved!")

# -------------------------------
# Customer pages (v5)
# -------------------------------
def my_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

def my_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)
    chits_df = pd.DataFrame({"Chit Name": ["Gold 12-Month", "Diamond Savings"], "Amount": ["₹1,00,000", "₹2,00,000"], "Status": ["✅ Active", "✅ Active"], "Next Payment": ["2026-01-15", "2026-02-15"]})
    st.dataframe(chits_df, use_container_width=True, hide_index=True)

def offers_rewards_page():
    st.markdown("<h2 class='main-title'>🎁 Offers & Rewards</h2>", unsafe_allow_html=True)
    st.info("🎉 **Active Offers:**\n- 15% Wedding Discount\n- 30% Clearance Sale\n- Free Maintenance")

def my_summary_page():
    st.markdown("<h2 class='main-title'>📊 My Summary</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Spent", "₹5,00,000", "Premium")
    with col2:
        st.metric("🛍️ Purchases", "12", "+2")
    with col3:
        st.metric("💎 Active Chits", "2", "₹3L")
    with col4:
        st.metric("⭐ Loyalty Tier", "Gold", "🏆")

def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)
    st.markdown("<div class='success-box'><strong>📞 24/7 Customer Support</strong><br>We're here to help!</div>", unsafe_allow_html=True)
    if prompt := st.chat_input("How can we help?"):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("Thank you! We'll respond soon.")

def sales_record_page():
    st.markdown("<h2 class='main-title'>💾 Sales Record</h2>", unsafe_allow_html=True)
    sales_df = pd.DataFrame({"Date": ["2025-12-10", "2025-12-09", "2025-12-08", "2025-12-07"], "Item": ["Gold Ring", "Silver Bracelet", "Diamond Pendant", "Gold Necklace"], "Amount": ["₹45,000", "₹8,000", "₹55,000", "₹32,000"], "Commission": ["₹2,250", "₹400", "₹2,750", "₹1,600"]})
    st.dataframe(sales_df, use_container_width=True, hide_index=True)

def loyalty_program_page():
    st.markdown("<h2 class='main-title'>🎁 Loyalty Program</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("💎 Your Tier", "Gold", "🏆")
    with col2:
        st.metric("⭐ Total Points", "890", "+150")
    with col3:
        st.metric("🎁 Redemptions", "5", "₹250")

# -------------------------------
# ML/Chit/Settings pages already added above
# -------------------------------

# -------------------------------
# MAIN
# -------------------------------
def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}!</h3>", unsafe_allow_html=True)
            st.markdown(f"**Role:** {st.session_state.user_role}")
            st.divider()
            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)
            st.divider()
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()

        # route to selected page
        if selected_page == "📊 Dashboard":
            dashboard_page()
        elif selected_page == "💎 My Dashboard":
            customer_dashboard_page()
        elif selected_page == "👥 Customers":
            customers_page()
        elif selected_page == "📦 Inventory":
            inventory_page()
        elif selected_page == "💰 Tax & Compliance":
            tax_compliance_page()
        elif selected_page == "📢 Campaigns":
            campaigns_page()
        elif selected_page == "👨‍💼 Staff Management":
            staff_management_page()
        elif selected_page == "⚡ Quick Actions":
            quick_actions_page()
        elif selected_page == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected_page == "💬 Smart Commands":
            smart_commands_page()
        elif selected_page == "💬 Chatbot":
            chatbot_page()
        elif selected_page == "🔎 Integrated Chatbot":
            integrated_chatbot_with_data_page()
        elif selected_page == "🤖 ML Models":
            show_ml_models()
        elif selected_page == "💎 Chit Management":
            show_chit_management()
        elif selected_page == "⚙️ Advanced Settings":
            show_settings_v4()
        elif selected_page == "⚙️ Settings":
            settings_page()
        elif selected_page == "💬 Smart Chatbot":
            chatbot_page()
        elif selected_page == "💾 Sales Record":
            sales_record_page()
        elif selected_page == "🎁 Loyalty Program":
            loyalty_program_page()
        elif selected_page == "🛍️ My Purchases":
            my_purchases_page()
        elif selected_page == "💎 My Chits":
            my_chits_page()
        elif selected_page == "🎁 Offers & Rewards":
            offers_rewards_page()
        elif selected_page == "📊 My Summary":
            my_summary_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "👨‍💼 Staff Dashboard":
            staff_dashboard_page()
        else:
            st.info("Select a page from the sidebar")

# Quick actions function used in routing (exists earlier in v5)
def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    st.markdown("<div class='info-box'><strong>⚡ Common Tasks</strong><br>Quickly perform frequently used operations with one click!</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 Generate Daily Report", use_container_width=True, key="quick_report"):
            st.success("✅ Daily report generated!")
            st.info(f"Report Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    with col2:
        if st.button("💳 Process Pending Payments", use_container_width=True, key="quick_payment"):
            st.success("✅ Processed 5 pending payments")
            st.info("Total Amount: ₹41,000")
    with col3:
        if st.button("📦 Inventory Stock Check", use_container_width=True, key="quick_stock"):
            st.success("✅ Stock check completed")
            st.warning("⚠️ 2 items low on stock")
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👥 Export Customer List", use_container_width=True, key="quick_export"):
            st.success("✅ Customer list exported as CSV")
    with col2:
        if st.button("📧 Send Marketing Email", use_container_width=True, key="quick_email"):
            st.success("✅ Email campaign sent to 1,250 customers")
    with col3:
        if st.button("📞 Backup Data", use_container_width=True, key="quick_backup"):
            st.success("✅ Data backup completed successfully")
    st.divider()
    st.subheader("📊 Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Today's Sales", "₹1,85,000", "+₹25,000")
    with col2:
        st.metric("New Customers", "12", "+3")
    with col3:
        st.metric("Pending Orders", "8", "-2")
    with col4:
        st.metric("Staff On Duty", "4/5", "80%")

if __name__ == "__main__":
    main()
