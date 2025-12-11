"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v11.0
✨ ENHANCED CUSTOMER DASHBOARD - Gold/Silver Rates, Summary, Pending, Campaigns
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
# PAGE CONFIG - LUXURY BLACK & SILVER THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# LUXURY BLACK & SILVER THEME - DARK & ELEGANT
st.markdown("""
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
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []

# ============================================================================
# LIVE MARKET DATA - TODAY'S RATES
# ============================================================================

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
    }
}

# ============================================================================
# CUSTOMER DATA - PURCHASE HISTORY & SUMMARY
# ============================================================================

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
        "last_purchase": "2025-12-08"
    }
}

# Customer Purchase History
CUSTOMER_PURCHASES = [
    {"date": "2025-12-08", "item": "Gold Ring", "purity": "22K", "weight": "5.2g", "amount": 45000, "status": "Delivered"},
    {"date": "2025-11-25", "item": "Silver Bracelet", "purity": "92.5%", "weight": "45g", "amount": 8500, "status": "Delivered"},
    {"date": "2025-11-15", "item": "Gold Necklace", "purity": "18K", "weight": "12.5g", "amount": 85000, "status": "Delivered"},
    {"date": "2025-10-30", "item": "Diamond Pendant", "purity": "Diamond", "weight": "0.5ct", "amount": 120000, "status": "Delivered"},
    {"date": "2025-10-10", "item": "Gold Earrings", "purity": "22K", "weight": "3.5g", "amount": 28000, "status": "Delivered"},
]

# Pending Payments
PENDING_PAYMENTS = [
    {"item": "Gold Bangles (Wedding Set)", "amount": 45000, "due_date": "2025-12-15", "status": "Pending Payment"},
]

# Campaign Notifications
CAMPAIGN_NOTIFICATIONS = [
    {
        "title": "🎄 Christmas Special Offer",
        "discount": "20% OFF",
        "description": "Get 20% discount on all gold items",
        "valid": "Till Dec 31, 2025",
        "status": "Active"
    },
    {
        "title": "💒 Wedding Season Sale",
        "discount": "15% OFF",
        "description": "Special discount on bridal collections",
        "valid": "Till Mar 31, 2026",
        "status": "Active"
    },
    {
        "title": "✨ New Year New Look",
        "discount": "25% OFF",
        "description": "Exclusive offers on selected items",
        "valid": "Dec 25 - Jan 15",
        "status": "Upcoming"
    },
    {
        "title": "🎁 Loyalty Rewards Program",
        "discount": "Extra Points",
        "description": "Earn 5X loyalty points on purchases",
        "valid": "Ongoing",
        "status": "Active"
    }
]

# STAFF DATA
STAFF_MEMBERS = {
    "ram": {"name": "Ram Kumar", "position": "Sales Executive", "pending": "₹15,000"},
    "priya": {"name": "Priya Singh", "position": "Manager", "pending": "₹8,500"},
    "amit": {"name": "Amit Verma", "position": "Sales Associate", "pending": "₹12,000"},
    "neha": {"name": "Neha Sharma", "position": "Cashier", "pending": "₹5,500"}
}

# Authentication
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
    "customer": {
        "password": hashlib.sha256("customer123".encode()).hexdigest(),
        "role": "Customer",
        "name": "Customer"
    },
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin",
        "name": "Admin"
    }
}

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
            "💬 Chatbot"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "💾 Sales Record",
            "🎁 Loyalty Program",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
            "💬 Chatbot"
        ],
        "Customer": [
            "💎 My Dashboard",
            "🛍️ My Purchases",
            "💎 My Chits",
            "🎁 Offers & Rewards",
            "📊 My Summary",
            "💬 Support Chat"
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
            "⚙️ Settings"
        ]
    }
    return pages.get(role, [])

# ============================================================================
# LOGIN PAGE
# ============================================================================

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
        st.markdown("""
        ### 📝 Demo Credentials:
        **Manager:** username: `manager` | password: `manager123`  
        **Staff:** username: `staff` | password: `staff123`  
        **Customer:** username: `customer` | password: `customer123`  
        **Admin:** username: `admin` | password: `admin123`
        """)

# ============================================================================
# CUSTOMER DASHBOARD PAGE - ENHANCED WITH RATES, SUMMARY, PENDING, CAMPAIGNS
# ============================================================================

def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)

    customer = CUSTOMER_DATA["customer"]

    # Welcome Section
    st.markdown(f"""
    <div class='info-box'>
    <strong>👋 Welcome, {customer['name']}!</strong><br>
    <strong>Member Since:</strong> {customer['joining_date']} | 
    <strong>Status:</strong> {customer['tier']} Tier | 
    <strong>Loyalty Points:</strong> ⭐ {customer['loyalty_points']}
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ========================================================================
    # SECTION 1: GOLD & SILVER LIVE RATES
    # ========================================================================

    st.subheader("💰 Today's Live Market Rates")

    col1, col2 = st.columns(2)

    with col1:
        gold = TODAY_RATES["gold"]
        change_color = "🟢" if gold["change"] >= 0 else "🔴"
        st.markdown(f"""
        <div class='gold-box'>
            <h3>💛 GOLD</h3>
            <h2>₹{gold['current']}/{gold['unit']}</h2>
            <p>{change_color} {gold['currency']}{gold['change']} ({gold['change_percent']:.2f}%)</p>
            <small>Previous: ₹{gold['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        silver = TODAY_RATES["silver"]
        change_color = "🟢" if silver["change"] >= 0 else "🔴"
        st.markdown(f"""
        <div class='silver-box'>
            <h3>🤍 SILVER</h3>
            <h2>₹{silver['current']}/{silver['unit']}</h2>
            <p>{change_color} {silver['currency']}{silver['change']} ({silver['change_percent']:.2f}%)</p>
            <small>Previous: ₹{silver['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ========================================================================
    # SECTION 2: ACCOUNT SUMMARY
    # ========================================================================

    st.subheader("📊 Your Account Summary")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("💰 Total Spent", f"₹{customer['total_spent']:,}", f"₹{customer['total_spent']//12:,.0f}/year")
    with col2:
        st.metric("🛍️ Purchases", f"{customer['total_purchases']}", f"Last: {customer['last_purchase']}")
    with col3:
        st.metric("⭐ Loyalty Points", f"{customer['loyalty_points']}", "100pts = ₹50")
    with col4:
        st.metric("💎 Your Tier", customer['tier'], "Premium Member")

    st.divider()

    # ========================================================================
    # SECTION 3: PURCHASE HISTORY & SUMMARY
    # ========================================================================

    st.subheader("🛍️ Your Purchase History")

    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    purchases_df = purchases_df[['date', 'item', 'purity', 'weight', 'amount', 'status']]
    purchases_df.columns = ['Date', 'Item', 'Purity', 'Weight', 'Amount (₹)', 'Status']

    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

    # Summary Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Purchases", f"{len(CUSTOMER_PURCHASES)}", "items")
    with col2:
        total_amount = sum([p['amount'] for p in CUSTOMER_PURCHASES])
        st.metric("Total Amount", f"₹{total_amount:,}", "all purchases")
    with col3:
        avg_amount = total_amount // len(CUSTOMER_PURCHASES)
        st.metric("Average Purchase", f"₹{avg_amount:,}", "per transaction")

    st.divider()

    # ========================================================================
    # SECTION 4: PENDING AMOUNT
    # ========================================================================

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
                    st.info("📅 Payment scheduled for " + payment['due_date'])

            st.divider()
    else:
        st.success("✅ No pending payments! You're all caught up!")

    st.divider()

    # ========================================================================
    # SECTION 5: CAMPAIGN NOTIFICATIONS
    # ========================================================================

    st.subheader("🎯 Active Campaign Notifications")

    st.markdown("""
    <div class='info-box'>
    <strong>🎉 You have 4 active offers & campaigns!</strong><br>
    Browse the latest deals tailored for Gold tier members like you.
    </div>
    """, unsafe_allow_html=True)

    for campaign in CAMPAIGN_NOTIFICATIONS:
        st.markdown(f"""
        <div class='campaign-notification'>
            <h4>{campaign['title']}</h4>
            <strong style='color: #ffd700; font-size: 1.2rem;'>{campaign['discount']}</strong><br>
            📝 {campaign['description']}<br>
            ⏰ <small>Valid: {campaign['valid']}</small> | 
            <strong style='color: #7cb342;'>✅ {campaign['status']}</strong>
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"🔖 Learn More", use_container_width=True, key=f"learn_{campaign['title']}"):
                st.info(f"📌 {campaign['title']}: {campaign['description']}")
        with col2:
            if st.button(f"🛍️ Shop Now", use_container_width=True, key=f"shop_{campaign['title']}"):
                st.success("✅ Redirecting to shop... (in app)")

        st.divider()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)

    dates = pd.date_range(start='2025-11-01', end='2025-12-11', freq='D')
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
        fig.update_layout(paper_bgcolor='#0f0f0f', plot_bgcolor='#1a1a1a', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Product Sales by Category")
        fig.update_layout(paper_bgcolor='#0f0f0f', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.subheader("📋 Recent Transactions")
    transactions_df = pd.DataFrame({
        'Transaction ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004', 'TXN005'],
        'Customer': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
        'Amount': ['₹45,000', '₹32,000', '₹18,000', '₹22,000', '₹8,000'],
        'Date': ['2025-12-10', '2025-12-09', '2025-12-08', '2025-12-07', '2025-12-06'],
        'Status': ['✅ Completed', '✅ Completed', '⏳ Pending', '✅ Completed', '✅ Completed']
    })
    st.dataframe(transactions_df, use_container_width=True, hide_index=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📋 All Customers", "➕ Add Customer"])

    with tab1:
        st.subheader("Customer List")
        customers_df = pd.DataFrame({
            'ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
            'Total Purchases': ['₹5,00,000', '₹3,50,000', '₹1,80,000', '₹2,20,000', '₹80,000'],
            'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25']
        })
        st.dataframe(customers_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Full Name", key="cust_name")
            st.text_input("Email", key="cust_email")
        with col2:
            st.selectbox("Customer Tier", ["Standard", "Silver", "Gold", "Premium"], key="cust_tier")
            st.date_input("Date of Birth", key="cust_dob")

        if st.button("✅ Add Customer", use_container_width=True):
            st.success("✅ Customer added successfully!")

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    inventory_df = pd.DataFrame({
        'Item Code': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005'],
        'Item Name': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
        'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold'],
        'Quantity': [45, 120, 15, 8, 32],
        'Unit Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
        'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low Stock', '🔴 Critical', '✅ In Stock']
    })

    st.subheader("Current Inventory")
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Stock by Category")
        stock_data = pd.DataFrame({
            'Category': ['Gold', 'Silver', 'Diamond', 'Platinum'],
            'Items': [45, 120, 15, 8]
        })
        fig = px.bar(stock_data, x='Category', y='Items', title="Items by Category", color='Category')
        fig.update_layout(paper_bgcolor='#0f0f0f', plot_bgcolor='#1a1a1a', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💰 Inventory Value by Category")
        value_data = pd.DataFrame({
            'Category': ['Gold', 'Silver', 'Diamond', 'Platinum'],
            'Value': [675000, 240000, 750000, 600000]
        })
        fig = px.pie(value_data, values='Value', names='Category', title="Inventory Value")
        fig.update_layout(paper_bgcolor='#0f0f0f', font=dict(color='#e8e8e8'))
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAX & COMPLIANCE PAGE
# ============================================================================

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
            'Month': ['October', 'November', 'December'],
            'Sales': ['₹15,00,000', '₹18,00,000', '₹22,00,000'],
            'GST Rate': ['18%', '18%', '18%'],
            'GST Amount': ['₹2,70,000', '₹3,24,000', '₹3,96,000'],
            'Status': ['✅ Filed', '✅ Filed', '⏳ Pending']
        })
        st.dataframe(gst_df, use_container_width=True, hide_index=True)

    with tab3:
        st.subheader("Generate Tax Reports")
        report_type = st.selectbox("Select Report Type", ["Monthly Summary", "Quarterly Filing", "Annual Return"])
        if st.button("📥 Generate Report"):
            st.success(f"✅ {report_type} generated successfully!")

# ============================================================================
# CAMPAIGNS PAGE
# ============================================================================

def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Active Campaigns", "➕ Create Campaign"])

    with tab1:
        st.subheader("All Active Campaigns")
        campaigns_df = pd.DataFrame({
            'Campaign Name': ['🎄 Diwali Sale 2025', '💒 Wedding Season', '🎉 Clearance Sale', '✨ New Year Special'],
            'Start Date': ['2025-10-15', '2025-11-01', '2025-12-01', '2025-12-25'],
            'End Date': ['2025-12-31', '2025-03-31', '2025-12-31', '2026-01-15'],
            'Discount': ['20%', '15%', '30%', '25%'],
            'Status': ['🟢 Active', '🟢 Active', '🟢 Active', '🟡 Scheduled'],
            'Revenue': ['₹45,00,000', '₹32,00,000', '₹25,00,000', '₹0'],
            'ROI': ['285%', '250%', '180%', 'TBD']
        })
        st.dataframe(campaigns_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Create New Campaign")
        col1, col2 = st.columns(2)

        with col1:
            st.text_input("Campaign Name", key="camp_name")
            st.selectbox("Campaign Type", ["Seasonal Sale", "Festival Offer", "Clearance"], key="camp_type")
            st.slider("Discount %", 5, 50, 15, key="camp_discount")

        with col2:
            st.number_input("Target Revenue (₹)", min_value=100000, step=100000, key="camp_target")
            st.number_input("Marketing Budget (₹)", min_value=10000, step=10000, key="camp_budget")
            st.date_input("End Date", key="camp_end")

        if st.button("🚀 Launch Campaign", use_container_width=True):
            st.success("✅ Campaign launched successfully!")
            st.balloons()

# ============================================================================
# STAFF MANAGEMENT PAGE
# ============================================================================

def staff_management_page():
    st.markdown("<h2 class='main-title'>👨‍💼 Staff Management</h2>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📊 Staff Directory", "💰 Pending Amounts"])

    with tab1:
        st.subheader("Staff Directory")
        staff_df = pd.DataFrame({
            'Name': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma', 'Vikram Gupta'],
            'Position': ['Sales Executive', 'Manager', 'Sales Associate', 'Cashier', 'Showroom Lead'],
            'Department': ['Sales', 'Management', 'Sales', 'Operations', 'Sales'],
            'Joining Date': ['2022-01-15', '2021-03-20', '2023-06-10', '2022-11-05', '2023-02-14'],
            'Status': ['✅ Active', '✅ Active', '✅ Active', '✅ Active', '✅ Active']
        })
        st.dataframe(staff_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("💸 Pending Commission/Amount")
        pending_df = pd.DataFrame({
            'Staff Name': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma'],
            'Position': ['Sales Executive', 'Manager', 'Sales Associate', 'Cashier'],
            'Pending Amount': ['₹15,000', '₹8,500', '₹12,000', '₹5,500'],
            'Due Date': ['2025-12-15', '2025-12-20', '2025-12-18', '2025-12-15'],
            'Status': ['⏳ Pending', '⏳ Pending', '⏳ Pending', '⏳ Pending']
        })
        st.dataframe(pending_df, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("💳 Pay All Pending", use_container_width=True):
                st.success("✅ All pending amounts paid!")
        with col2:
            if st.button("📧 Send Reminder", use_container_width=True):
                st.info("✉️ Reminders sent to all staff!")

# ============================================================================
# QUICK ACTIONS PAGE
# ============================================================================

def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>⚡ Common Tasks</strong><br>
    Quickly perform frequently used operations with one click!
    </div>
    """, unsafe_allow_html=True)

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

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='success-box'>
    <strong>🤖 Jewellery Shop AI Assistant</strong><br>
    Get instant insights, recommendations, and automated suggestions for your jewellery business!
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["💡 Insights", "📊 Recommendations", "🔍 Analytics"])

    with tab1:
        st.subheader("💡 AI Business Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            ✅ **Sales Trend Analysis**
            - Sales trending upward by 15% this month
            - Peak sales time: 2 PM - 5 PM
            - Best selling category: Gold (45%)

            💡 **Recommendation:** Stock more gold items during peak hours
            """)

        with col2:
            st.markdown("""
            👥 **Customer Insights**
            - 87% customers are repeat buyers
            - Average customer lifetime value: ₹2,50,000
            - Premium tier customers spend 4x more

            💡 **Recommendation:** Focus on premium customer retention
            """)

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            📦 **Inventory Optimization**
            - Platinum inventory critical (8 items)
            - Silver stock high (120 items)
            - Estimated stockout: 5 days for diamonds

            💡 **Recommendation:** Reorder platinum immediately
            """)

        with col2:
            st.markdown("""
            💰 **Profit Analysis**
            - Average profit margin: 28%
            - Peak profit items: Diamond (35% margin)
            - Low margin items: Silver (12% margin)

            💡 **Recommendation:** Push diamond sales for better margins
            """)

    with tab2:
        st.subheader("📊 AI Recommendations")

        recommendations = [
            "🎯 Launch 'Diamond Premium' campaign - predicted ROI: 320%",
            "👥 Create loyalty program for premium customers - estimated 25% increase in repeat purchases",
            "📦 Implement dynamic pricing for high-demand items",
            "🌍 Expand online presence - untapped market worth ₹50L+",
            "⏰ Shift staff schedule to peak hours - 40% efficiency gain",
            "💳 Introduce EMI option - predicted 18% sales increase"
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
            forecast_data = pd.DataFrame({
                'Month': ['Dec 2025', 'Jan 2026', 'Feb 2026', 'Mar 2026'],
                'Predicted Sales': [65, 72, 68, 85],
                'Confidence': ['92%', '88%', '85%', '80%']
            })
            st.dataframe(forecast_data, hide_index=True)

        with col2:
            st.markdown("**👥 Customer Segmentation**")
            segment_data = pd.DataFrame({
                'Segment': ['Premium', 'Gold', 'Silver', 'Standard'],
                'Count': [125, 320, 580, 225],
                'Value': ['₹2,50L', '₹1,60L', '₹87.5L', '₹22.5L']
            })
            st.dataframe(segment_data, hide_index=True)

# ============================================================================
# SMART COMMANDS PAGE
# ============================================================================

def smart_commands_page():
    st.markdown("<h2 class='main-title'>💬 Smart Commands - Staff Alerts</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>🎯 Smart Command System</strong><br>
    Send alerts and commands to staff members. Example: "Alert Ram about pending ₹15,000"
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔔 Alert Ram - Pending ₹15,000", use_container_width=True, key="alert_ram"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Ram about pending ₹15,000"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Ram Kumar notified\n📛 Pending: ₹15,000\n⏰ Time: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    with col2:
        if st.button("🔔 Alert Priya - Pending ₹8,500", use_container_width=True, key="alert_priya"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Priya about pending ₹8,500"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Priya Singh notified\n📛 Pending: ₹8,500\n⏰ Time: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    with col3:
        if st.button("📢 Notify All Staff", use_container_width=True, key="alert_all"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Send notification to all staff"},
                {"role": "assistant", "content": "📢 **Broadcast Sent**\n\n✅ All 5 staff notified\n⏰ Time: " + datetime.now().strftime("%H:%M")}
            ]
            st.rerun()

    st.divider()

    st.subheader("📤 Send Custom Alert/Command")

    col1, col2 = st.columns([3, 1])

    with col1:
        custom_command = st.text_input("Enter command", placeholder="e.g., 'Alert Ram about pending'", key="custom_cmd")

    with col2:
        send_btn = st.button("📤 Send", use_container_width=True, key="send_cmd_btn")

    if send_btn and custom_command:
        command_lower = custom_command.lower()
        staff_alerts = {
            "ram": {"name": "Ram Kumar", "pending": "₹15,000"},
            "priya": {"name": "Priya Singh", "pending": "₹8,500"},
            "amit": {"name": "Amit Verma", "pending": "₹12,000"},
            "neha": {"name": "Neha Sharma", "pending": "₹5,500"}
        }

        response = "❌ Command not recognized"

        if "alert" in command_lower or "notify" in command_lower:
            found = False
            for staff_key, staff_info in staff_alerts.items():
                if staff_key in command_lower:
                    response = f"🔔 **Alert Sent**\n\n✅ {staff_info['name']} notified\n📛 {custom_command}\n⏰ {datetime.now().strftime('%H:%M')}"
                    found = True
                    break

            if not found and "all" in command_lower:
                response = f"📢 **Broadcast Sent**\n\n✅ All staff notified\n📌 {custom_command}\n⏰ {datetime.now().strftime('%H:%M')}"

        st.session_state.smart_command_messages.append({"role": "user", "content": custom_command})
        st.session_state.smart_command_messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.divider()
    st.subheader("📋 Command History")

    if st.session_state.smart_command_messages:
        for message in st.session_state.smart_command_messages:
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**Command:** {message['content']}")
    else:
        st.info("✅ No commands sent yet.")

# ============================================================================
# CHATBOT PAGE
# ============================================================================

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

# ============================================================================
# CUSTOMER PAGES
# ============================================================================

def my_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

def my_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)
    chits_df = pd.DataFrame({
        'Chit Name': ['Gold 12-Month', 'Diamond Savings'],
        'Amount': ['₹1,00,000', '₹2,00,000'],
        'Status': ['✅ Active', '✅ Active'],
        'Next Payment': ['2026-01-15', '2026-02-15']
    })
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
    st.markdown("""
    <div class='success-box'>
    <strong>📞 24/7 Customer Support</strong><br>
    We're here to help!
    </div>
    """, unsafe_allow_html=True)

    if prompt := st.chat_input("How can we help?"):
        st.chat_message("user").write(prompt)
        st.chat_message("assistant").write("Thank you! We'll respond soon.")

def sales_record_page():
    st.markdown("<h2 class='main-title'>💾 Sales Record</h2>", unsafe_allow_html=True)
    st.subheader("Your Sales")
    sales_df = pd.DataFrame({
        'Date': ['2025-12-10', '2025-12-09', '2025-12-08', '2025-12-07'],
        'Item': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Gold Necklace'],
        'Amount': ['₹45,000', '₹8,000', '₹55,000', '₹32,000'],
        'Commission': ['₹2,250', '₹400', '₹2,750', '₹1,600']
    })
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

# ============================================================================
# MAIN APPLICATION
# ============================================================================

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

        # Route to pages
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
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
