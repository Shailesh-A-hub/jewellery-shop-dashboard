"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v7.0 ✨
ENHANCED FINAL VERSION - ALL FEATURES INTEGRATED
Manager, Staff, Customer, Admin Roles
Live Market Data + Customer AI Support + ML Models
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
    page_title="💎 Jewellery AI Dashboard v7.0",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# LUXURY BLACK & SILVER THEME
st.markdown("""
<style>
    :root {
        --primary-color: #c0c0c0;
        --secondary-color: #ffd700;
        --bg-dark: #0f0f0f;
        --bg-lighter: #1a1a1a;
        --text-primary: #e8e8e8;
        --text-secondary: #a8a8a8;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0f0f0f !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1a1a1a !important;
        border-right: 2px solid #c0c0c0 !important;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #c0c0c0 !important;
        letter-spacing: 1px;
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
    
    .ai-response {
        background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important;
        border: 2px solid #c0c0c0 !important;
        border-radius: 10px !important;
        padding: 18px !important;
        margin: 12px 0 !important;
        color: #e8e8e8 !important;
        box-shadow: 0 4px 16px rgba(192, 192, 192, 0.08) !important;
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
    
    [data-testid="stMetricValue"] {
        color: #c0c0c0 !important;
        font-size: 2rem !important;
        font-weight: bold !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #a8a8a8 !important;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.smart_command_messages = []
    st.session_state.customer_messages = []
    st.session_state.chatbot_messages = []

# ============================================================================
# LIVE MARKET DATA
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
# CUSTOMER DATA & SAMPLE DATA
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

# ============================================================================
# AUTHENTICATION
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
            "⚡ Quick Actions",
            "📢 Campaigns",
            "💎 Chit Management",
            "🤖 ML Models",
            "🤖 AI Assistant"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "⚡ Quick Actions",
            "🤖 AI Assistant"
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
            "⚡ Quick Actions",
            "📢 Campaigns",
            "💎 Chit Management",
            "🤖 ML Models",
            "🤖 AI Assistant",
            "⚙️ Settings"
        ]
    }
    return pages.get(role, [])

# ============================================================================
# MOCK DATA LOADERS
# ============================================================================
@st.cache_data
def load_mock_customers():
    return pd.DataFrame({
        'ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
        'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
        'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
        'Total Purchases': [500000, 350000, 180000, 220000, 80000],
        'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25'],
        'Pending Amount': [45000, 0, 12000, 8000, 0],
        'phone': ['98765-43210', '87654-32109', '76543-21098', '65432-10987', '54321-09876']
    })

@st.cache_data
def load_mock_inventory():
    return pd.DataFrame({
        'Code': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005'],
        'Item': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
        'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold'],
        'Quantity': [45, 120, 15, 8, 32],
        'Unit Price': [15000, 2000, 50000, 75000, 22000],
        'Status': ['In Stock', 'In Stock', 'Low Stock', 'Critical', 'In Stock'],
        'Days Sold': [2, 5, 45, 92, 3]
    })

@st.cache_data
def load_mock_chit_schedule():
    return pd.DataFrame({
        'chit_group': ['Gold 12-Month', 'Diamond Savings', 'Silver Elite', 'Platinum Plus'],
        'payout_date': [
            datetime.now().date() + timedelta(days=5),
            datetime.now().date() + timedelta(days=15),
            datetime.now().date() + timedelta(days=25),
            datetime.now().date() + timedelta(days=35)
        ],
        'payout_amount': [100000, 200000, 75000, 150000],
        'expected_spending': [120000, 250000, 85000, 180000]
    })

# ============================================================================
# LOGIN PAGE
# ============================================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("**Premium Management System for Indian Jewellery Retail**")
        
        st.divider()
        
        login_type = st.radio("Login As", ["Manager", "Staff", "Customer", "Admin"], horizontal=True, key="login_type")
        
        if login_type == "Manager":
            st.subheader("🔐 Manager Login")
            username = st.text_input("Username", key="mgr_user_id")
            password = st.text_input("Password", type="password", key="mgr_pass_id")
            
            if st.button("Login", use_container_width=True, key="mgr_btn"):
                if username == "manager" and hashlib.sha256(password.encode()).hexdigest() == USERS["manager"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        elif login_type == "Staff":
            st.subheader("🔐 Staff Login")
            username = st.text_input("Username", key="staff_user_id")
            password = st.text_input("Password", type="password", key="staff_pass_id")
            
            if st.button("Login", use_container_width=True, key="staff_btn"):
                if username == "staff" and hashlib.sha256(password.encode()).hexdigest() == USERS["staff"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Sales Staff"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        elif login_type == "Customer":
            st.subheader("🔐 Customer Login")
            username = st.text_input("Username", key="cust_user_id")
            password = st.text_input("Password", type="password", key="cust_pass_id")
            
            if st.button("Login", use_container_width=True, key="cust_btn"):
                if username == "customer" and hashlib.sha256(password.encode()).hexdigest() == USERS["customer"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        else:  # Admin
            st.subheader("🔐 Admin Login")
            username = st.text_input("Username", key="admin_user_id")
            password = st.text_input("Password", type="password", key="admin_pass_id")
            
            if st.button("Login", use_container_width=True, key="admin_btn"):
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
        **Demo Credentials:**
        - Manager: `manager` / `manager123`
        - Staff: `staff` / `staff123`
        - Customer: `customer` / `customer123`
        - Admin: `admin` / `admin123`
        """)

# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================
def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)
    
    customer = CUSTOMER_DATA["customer"]
    
    st.markdown(f"""
    <div class='info-box'>
        <strong>Welcome, {customer['name']}!</strong><br>
        <strong>Member Since:</strong> {customer['joining_date']}<br>
        <strong>Status:</strong> {customer['tier']} Tier<br>
        <strong>Loyalty Points:</strong> {customer['loyalty_points']}
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("📊 Today's Live Market Rates")
    col1, col2 = st.columns(2)
    
    with col1:
        gold = TODAY_RATES["gold"]
        change_color = "🔼" if gold['change'] > 0 else "🔽"
        st.markdown(f"""
        <div class='gold-box'>
            <h3>⭐ GOLD</h3>
            <h2>{gold['current']}{gold['unit'].split()[1]}</h2>
            <p>{change_color} {gold['currency']}{gold['change']} ({gold['change_percent']:.2f}%)</p>
            <small>Previous: ₹{gold['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        silver = TODAY_RATES["silver"]
        change_color = "🔼" if silver['change'] > 0 else "🔽"
        st.markdown(f"""
        <div class='silver-box'>
            <h3>✨ SILVER</h3>
            <h2>{silver['current']}{silver['unit'].split()[1]}</h2>
            <p>{change_color} {silver['currency']}{silver['change']} ({silver['change_percent']:.2f}%)</p>
            <small>Previous: ₹{silver['previous']}</small><br>
            <small>Last Updated: {datetime.now().strftime('%H:%M:%S')}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.subheader("📈 Your Account Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💰 Total Spent", f"₹{customer['total_spent']:,}", f"₹{customer['total_spent']//12:,}/year")
    with col2:
        st.metric("🛍️ Purchases", customer['total_purchases'], f"Last: {customer['last_purchase']}")
    with col3:
        st.metric("🎁 Loyalty Points", customer['loyalty_points'], "100pts = ₹50")
    with col4:
        st.metric("👑 Your Tier", customer['tier'], "Premium Member")
    
    st.divider()
    
    st.subheader("📋 Your Purchase History")
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    purchases_df = purchases_df[['date', 'item', 'purity', 'weight', 'amount', 'status']]
    purchases_df.columns = ['Date', 'Item', 'Purity', 'Weight', 'Amount', 'Status']
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Purchases", len(CUSTOMER_PURCHASES), "items")
    with col2:
        total_amount = sum(p['amount'] for p in CUSTOMER_PURCHASES)
        st.metric("Total Amount", f"₹{total_amount:,}", "all purchases")
    with col3:
        avg_amount = total_amount // len(CUSTOMER_PURCHASES)
        st.metric("Average Purchase", f"₹{avg_amount:,}", "per transaction")
    
    st.divider()
    
    st.subheader("💳 Pending Payments")
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
                st.markdown(f"**Status:** {payment['status']}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💳 Pay Now", use_container_width=True, key=f"pay_{payment['item']}"):
                    st.success(f"✅ Payment of ₹{payment['amount']:,} processed successfully!")
            with col2:
                if st.button("📅 Schedule Payment", use_container_width=True, key=f"schedule_{payment['item']}"):
                    st.info(f"Payment scheduled for {payment['due_date']}")
        st.divider()
    else:
        st.success("✅ No pending payments! You're all caught up!")
        st.divider()
    
    st.subheader("🎯 Active Campaign Notifications")
    st.markdown("""
    <div class='info-box'>
        <strong>You have 4 active offers & campaigns!</strong><br>
        Browse the latest deals tailored for Gold tier members like you.
    </div>
    """, unsafe_allow_html=True)
    
    for campaign in CAMPAIGN_NOTIFICATIONS:
        st.markdown(f"""
        <div class='campaign-notification'>
            <h4>{campaign['title']}</h4>
            <strong style='color: #ffd700; font-size: 1.2rem;'>{campaign['discount']}</strong><br>
            {campaign['description']}<br>
            <small>Valid: {campaign['valid']}</small>
            <strong style='color: #7cb342;'>{campaign['status']}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📖 Learn More", use_container_width=True, key=f"learn_{campaign['title']}"):
                st.info(f"{campaign['title']}\n\n{campaign['description']}")
        with col2:
            if st.button(f"🛒 Shop Now", use_container_width=True, key=f"shop_{campaign['title']}"):
                st.success("Redirecting to shop... (in app)")

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Sales", "₹25,50,000", "+₹5,00,000")
    with col2:
        st.metric("👥 Total Customers", "1,250", "+45")
    with col3:
        st.metric("💎 Stock Value", "₹45,00,000", "-₹2,00,000")
    with col4:
        st.metric("💰 Active Chits", "85", "+12")
    
    st.divider()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sales Trend (Nov-Dec 2025)")
        dates = pd.date_range(start='2025-11-01', end='2025-12-11', freq='D')
        sales_data = np.random.randint(50000, 200000, len(dates))
        
        fig = px.line(x=dates, y=sales_data, title="Daily Sales Trend")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Sales")
        fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📦 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        
        fig = px.pie(values=values, names=categories, title="Product Sales by Category")
        fig.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    st.subheader("💳 Recent Transactions")
    transactions_df = pd.DataFrame({
        'Transaction ID': ['TXN001', 'TXN002', 'TXN003', 'TXN004', 'TXN005'],
        'Customer': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
        'Amount': ['₹45,000', '₹32,000', '₹18,000', '₹22,000', '₹8,000'],
        'Date': ['2025-12-10', '2025-12-09', '2025-12-08', '2025-12-07', '2025-12-06'],
        'Status': ['Completed', 'Completed', 'Pending', 'Completed', 'Completed']
    })
    st.dataframe(transactions_df, use_container_width=True, hide_index=True)

# ============================================================================
# CUSTOMERS PAGE (EXACT v5)
# ============================================================================
def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Customers", "At Risk", "VIP Management", "Pending Customers"])
    
    customers_df = load_mock_customers()
    today = datetime.now().date()
    
    with tab1:
        st.subheader("📋 Customer List")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            search_name = st.text_input("Search by Name", key="search_cust")
        with col2:
            filter_tier = st.selectbox("Filter by Tier", ["All", "Premium", "Gold", "Silver", "Standard"], key="filter_tier")
        with col3:
            st.write("")  # Alignment
        
        if search_name:
            customers_df = customers_df[customers_df['Name'].str.contains(search_name, case=False)]
        if filter_tier != "All":
            customers_df = customers_df[customers_df['Tier'] == filter_tier]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Found", len(customers_df))
        with col2:
            st.metric("Total Pending", f"₹{customers_df['Pending Amount'].sum():,}")
        with col3:
            st.metric("Total Spent", f"₹{customers_df['Total Purchases'].sum():,}")
        
        st.dataframe(customers_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("⚠️ At-Risk Customers (90+ days no visit)")
        
        at_risk = customers_df.copy()
        at_risk['days_inactive'] = np.random.randint(90, 180, len(at_risk))
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("At-Risk Count", len(at_risk))
        with col2:
            st.metric("Total Pending", f"₹{at_risk['Pending Amount'].sum():,}")
        with col3:
            st.metric("Urgent Calls", len(at_risk[at_risk['Pending Amount'] > 10000]))
        
        st.dataframe(at_risk[['Name', 'Tier', 'days_inactive', 'Pending Amount']], use_container_width=True, hide_index=True)
        
        if st.button("📢 Send Reminder Campaign", use_container_width=True):
            st.success(f"✅ Reminder campaign sent to {len(at_risk)} customers!")
    
    with tab3:
        st.subheader("👑 VIP Customers Management")
        
        vip = customers_df[customers_df['Tier'] == 'Premium']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total VIPs", len(vip))
        with col2:
            st.metric("Total Spent", f"₹{vip['Total Purchases'].sum():,}")
        with col3:
            avg_value = vip['Total Purchases'].mean() if len(vip) > 0 else 0
            st.metric("Avg Value", f"₹{avg_value:,.0f}")
        
        st.dataframe(vip, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("💳 Pending Customers")
        
        min_pending = st.slider("Minimum pending amount", 0, 50000, 5000, key="pending_slider")
        pending = customers_df[customers_df['Pending Amount'] >= min_pending].sort_values('Pending Amount', ascending=False)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Count", len(pending))
        with col2:
            st.metric("Total Pending", f"₹{pending['Pending Amount'].sum():,}")
        with col3:
            avg = pending['Pending Amount'].mean() if len(pending) > 0 else 0
            st.metric("Avg Per Customer", f"₹{avg:,.0f}")
        
        st.dataframe(pending, use_container_width=True, hide_index=True)
        
        if st.button("💬 Send Payment Collection Campaign", use_container_width=True):
            st.success(f"✅ Collection campaign sent to {len(pending)} customers!")

# ============================================================================
# INVENTORY PAGE
# ============================================================================
def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Current Stock", "Slow Movers", "Markdown"])
    
    inventory_df = load_mock_inventory()
    
    with tab1:
        st.subheader("📊 Current Inventory")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Items", inventory_df['Quantity'].sum())
        with col2:
            st.metric("Total Value", f"₹{(inventory_df['Quantity'] * inventory_df['Unit Price']).sum():,}")
        with col3:
            st.metric("Low Stock Items", len(inventory_df[inventory_df['Status'] != 'In Stock']))
        
        st.dataframe(inventory_df, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📈 Stock by Category")
            stock_data = inventory_df.groupby('Category')['Quantity'].sum().reset_index()
            fig = px.bar(stock_data, x='Category', y='Quantity', title="Items by Category")
            fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("💎 Inventory Value")
            inventory_df['Value'] = inventory_df['Quantity'] * inventory_df['Unit Price']
            fig = px.pie(inventory_df, values='Value', names='Category', title="Inventory Value by Category")
            fig.update_layout(paper_bgcolor="#0f0f0f", font=dict(color="#e8e8e8"))
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("🐌 Slow Moving Items (90+ days)")
        
        slow = inventory_df[inventory_df['Days Sold'] > 30].copy()
        st.metric("Slow Items", len(slow))
        
        st.dataframe(slow[['Item', 'Quantity', 'Days Sold', 'Unit Price']], use_container_width=True, hide_index=True)
        
        if st.button("📢 Send Campaign", use_container_width=True):
            st.success(f"✅ Campaign sent for {len(slow)} slow items!")
    
    with tab3:
        st.subheader("💰 Markdown Recommendations")
        
        st.markdown("""
        <div class='warning-box'>
            <strong>Markdown Strategy:</strong><br>
            • Dead stock (25%+): Apply 25-30% discount<br>
            • Slow stock (15-30 days): Apply 15-20% discount<br>
            • Seasonal items: Apply 10-15% discount
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Dead Stock (25%+)", "5 items")
        with col2:
            st.metric("Slow Stock (15%+)", "12 items")

# ============================================================================
# QUICK ACTIONS PAGE (v4)
# ============================================================================
def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    
    action_type = st.radio("Select Action", [
        "Send Payment Reminder",
        "Send Festival Offer",
        "Send Return Offer",
        "View Campaign Stats"
    ])
    
    if action_type == "Send Payment Reminder":
        st.subheader("📞 Send Payment Reminders")
        
        customers_df = load_mock_customers()
        pending_customers = customers_df[customers_df['Pending Amount'] > 0].copy()
        st.info(f"Found {len(pending_customers)} customers with pending amounts")
        
        min_amount = st.slider("Minimum pending amount", 0, 100000, 10000)
        filtered = pending_customers[pending_customers['Pending Amount'] >= min_amount]
        
        st.write(f"Will send to {len(filtered)} customers")
        
        message_template = st.text_area(
            "Message Template",
            value="""Hi {name},

We hope you're doing well! Your pending payment: ₹{pending:.0f}

Please make payment at your earliest convenience.

Thank you!
Shree Jewels""",
            height=150
        )
        
        if st.button("Send Messages", use_container_width=True):
            st.success(f"✅ Sent {len(filtered)} WhatsApp messages!")
    
    elif action_type == "Send Festival Offer":
        st.subheader("🎉 Festival Campaign")
        
        festival = st.selectbox("Select Festival", 
            ["Diwali", "Holi", "Wedding Season", "Akshaya Tritiya", "Custom"])
        
        target_tier = st.multiselect("Target Customer Tier",
            ["VIP", "Regular", "Dormant"], default=["VIP", "Regular"])
        
        offer_text = st.text_area("Festival Offer Message",
            value=f"""{festival} Special Offer!

Celebrate {festival} with us! Exclusive discounts.

✨ Special offer: 15% off
💎 Extra 10% for VIP
🎁 Free gift on ₹50,000+

Limited time only!""", height=150)
        
        if st.button("Send Campaign", use_container_width=True):
            st.success(f"✅ Festival campaign sent!")
    
    elif action_type == "Send Return Offer":
        st.subheader("🎯 Win-Back Campaign")
        
        st.info("Found 8 dormant customers (60+ days inactive)")
        
        col1, col2 = st.columns(2)
        with col1:
            discount = st.slider("Discount %", 0, 50, 20)
        with col2:
            incentive = st.selectbox("Incentive", ["Discount", "Free Gift", "Loyalty Points"])
        
        if st.button("Send Return Offers", use_container_width=True):
            st.success("✅ Return offers sent to 8 customers!")
    
    else:  # Campaign Stats
        st.subheader("📊 Campaign Performance")
        
        campaigns_df = pd.DataFrame({
            'Campaign': ['Payment Reminder', 'Diwali Offer', 'Festival Flash', 'VIP Exclusive'],
            'Sent': [150, 200, 180, 50],
            'Opened': [65, 120, 95, 42],
            'Clicked': [25, 45, 38, 18],
            'Revenue': [120000, 250000, 180000, 95000]
        })
        
        st.dataframe(campaigns_df, use_container_width=True, hide_index=True)

# ============================================================================
# CAMPAIGNS PAGE (v4)
# ============================================================================
def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Create Campaign", "Active Campaigns", "Reports"])
    
    with tab1:
        st.subheader("Create New Campaign")
        
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", placeholder="e.g., Diwali 2025")
            campaign_type = st.selectbox("Type", 
                ["Payment Reminder", "Festival", "Launch", "Clearance", "VIP", "Win-back"])
        with col2:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
        
        discount = st.slider("Discount %", 0, 50, 10)
        
        if st.button("Launch Campaign", use_container_width=True):
            if campaign_name:
                st.success(f"✅ Campaign '{campaign_name}' launched!")
            else:
                st.error("Please enter campaign name")
    
    with tab2:
        st.subheader("Active Campaigns")
        
        active_df = pd.DataFrame({
            'Campaign': ['Diwali Special', 'Payment Reminder', 'New Year Flash'],
            'Type': ['Festival', 'Reminder', 'Flash Sale'],
            'Status': ['Active', 'Active', 'Active'],
            'Reach': [180, 150, 200]
        })
        
        st.dataframe(active_df, use_container_width=True, hide_index=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Sent", 700, "+120")
        with col2:
            st.metric("Delivered", 680, "97%")
        with col3:
            st.metric("Opened", 410, "60%")
        with col4:
            st.metric("Clicked", 125, "18%")
    
    with tab3:
        st.subheader("Campaign Analytics")
        
        reports_df = pd.DataFrame({
            'Campaign': ['Diwali', 'Payment', 'New Year', 'VIP', 'Wedding'],
            'Sent': [180, 150, 200, 50, 120],
            'Opened': [105, 89, 117, 45, 71],
            'Converted': [12, 8, 14, 5, 9],
            'Revenue': [85000, 45000, 72000, 38000, 52000]
        })
        
        st.dataframe(reports_df, use_container_width=True, hide_index=True)

# ============================================================================
# CHIT MANAGEMENT PAGE (v4)
# ============================================================================
def chit_management_page():
    st.markdown("<h2 class='main-title'>💎 Chit Fund Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Chit Schedule", "Pre-Order Planning"])
    
    chit_df = load_mock_chit_schedule()
    today = datetime.now().date()
    
    with tab1:
        st.subheader("📅 Upcoming Chit Payouts (Next 60 Days)")
        
        upcoming = chit_df[
            (chit_df['payout_date'] >= today) &
            (chit_df['payout_date'] <= today + timedelta(days=60))
        ].copy()
        
        st.metric("Upcoming Payouts", len(upcoming))
        
        if len(upcoming) > 0:
            display_df = upcoming[['chit_group', 'payout_date', 'payout_amount', 'expected_spending']].copy()
            display_df['payout_amount'] = display_df['payout_amount'].apply(lambda x: f"₹{x:,}")
            display_df['expected_spending'] = display_df['expected_spending'].apply(lambda x: f"₹{x:,}")
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            total_expected = upcoming['expected_spending'].sum()
            st.metric("Total Expected Orders", f"₹{total_expected:,}")
    
    with tab2:
        st.subheader("📦 Pre-Order Recommendations")
        
        upcoming = chit_df[
            (chit_df['payout_date'] >= today) &
            (chit_df['payout_date'] <= today + timedelta(days=60))
        ].copy()
        
        if len(upcoming) > 0:
            st.info(f"Pre-book for {len(upcoming)} upcoming chit payouts")
            
            high_value = upcoming[upcoming['expected_spending'] > 100000]['expected_spending'].sum()
            medium_value = upcoming[
                (upcoming['expected_spending'] >= 50000) &
                (upcoming['expected_spending'] <= 100000)
            ]['expected_spending'].sum()
            low_value = upcoming[upcoming['expected_spending'] < 50000]['expected_spending'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🏆 Premium", f"₹{high_value:,}")
            with col2:
                st.metric("💎 Regular", f"₹{medium_value:,}")
            with col3:
                st.metric("✨ Light", f"₹{low_value:,}")

# ============================================================================
# ML MODELS PAGE
# ============================================================================
def ml_models_page():
    st.markdown("<h2 class='main-title'>🤖 ML Models</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Customer Risk", "Demand Forecast", "Pricing"])
    
    with tab1:
        st.subheader("⚠️ Customer Risk Scoring")
        
        np.random.seed(42)
        risk_df = pd.DataFrame({
            'Customer': ['Rajesh', 'Priya', 'Amit', 'Neha', 'Vikram'],
            'Risk Score': np.random.uniform(0, 100, 5),
            'Days Inactive': [15, 45, 5, 120, 30],
            'Pending Amount': [45000, 0, 12000, 5000, 0]
        })
        
        fig = px.scatter(risk_df, x='Days Inactive', y='Risk Score', size='Pending Amount',
                        hover_name='Customer', color='Risk Score', title="Customer Risk Analysis")
        fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 30-Day Demand Forecast")
        
        forecast_df = pd.DataFrame({
            'Date': pd.date_range('2025-12-13', periods=30),
            'Forecast': np.random.randint(50000, 150000, 30)
        })
        
        fig = px.line(forecast_df, x='Date', y='Forecast', title="Sales Forecast")
        fig.update_layout(paper_bgcolor="#0f0f0f", plot_bgcolor="#1a1a1a", font=dict(color="#e8e8e8"))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("💰 Dynamic Pricing Recommendations")
        
        pricing_df = pd.DataFrame({
            'Item': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Gold Necklace'],
            'Current Price': [15000, 2000, 50000, 22000],
            'Recommended Price': [16500, 2200, 55000, 24200],
            'Margin': [10, 10, 10, 10]
        })
        
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================
def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>Jewellery Shop AI Assistant</strong><br>
        Get instant insights, recommendations, and business strategies!
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Insights", "Recommendations"])
    
    with tab1:
        st.subheader("📊 AI Business Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Sales Trend Analysis**
            - Sales trending upward by 15% this month
            - Peak sales time: 2-5 PM
            - Best selling: Gold (45%)
            
            **Recommendation:**
            Stock more gold items during peak hours
            """)
        
        with col2:
            st.markdown("""
            **Customer Insights**
            - 87% repeat buyers
            - Avg lifetime value: ₹2,50,000
            - Premium tier spend 4x more
            
            **Recommendation:**
            Focus on premium customer retention
            """)
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Inventory Optimization**
            - Platinum inventory critical (8 items)
            - Silver stock high (120 items)
            - Diamonds: 5 days to stockout
            
            **Recommendation:**
            Reorder platinum immediately
            """)
        
        with col2:
            st.markdown("""
            **Profit Analysis**
            - Avg profit margin: 28%
            - Peak profit: Diamond (35%)
            - Low margin: Silver (12%)
            
            **Recommendation:**
            Push diamond sales
            """)
    
    with tab2:
        st.subheader("💡 AI Recommendations")
        
        recommendations = [
            "✅ Launch Diamond Premium campaign - Predicted ROI: 320%",
            "✅ Create loyalty program for premium customers - Est. 25% increase",
            "✅ Implement dynamic pricing - High-demand items",
            "✅ Expand online presence - Untapped market: ₹50L",
            "✅ Shift staff to peak hours - 40% efficiency gain",
            "✅ Introduce EMI option - 18% sales increase"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            col1, col2 = st.columns([0.1, 0.9])
            with col1:
                st.markdown(f"**{i}.**")
            with col2:
                st.markdown(rec)

# ============================================================================
# SUPPORT CHAT PAGE (Customer)
# ============================================================================
def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>24/7 Customer Support</strong><br>
        We're here to help with any questions!
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛍️ Purchase Help", use_container_width=True):
            st.session_state.chatbot_messages.append({
                "role": "assistant",
                "content": "You have 4 purchases. Latest: Gold Ring on Dec 10, ₹15,000"
            })
            st.rerun()
    with col2:
        if st.button("💎 Chit Support", use_container_width=True):
            st.session_state.chatbot_messages.append({
                "role": "assistant",
                "content": "Active chits: Gold 12-Month, Diamond Savings. Next payment: Dec 15"
            })
            st.rerun()
    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True):
            st.session_state.chatbot_messages.append({
                "role": "assistant",
                "content": "Gold Tier - 890 points. 100 points = ₹50 discount!"
            })
            st.rerun()
    
    st.divider()
    
    if st.session_state.chatbot_messages:
        for message in st.session_state.chatbot_messages:
            if message["role"] == "assistant":
                st.markdown(f"<div class='ai-response'>{message['content']}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"**You:** {message['content']}")
    
    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})
        
        response = "How can I help you?"
        if any(word in prompt.lower() for word in ['purchase', 'buy', 'order']):
            response = "Your purchases are delivered! Need details on any specific order?"
        elif any(word in prompt.lower() for word in ['chit', 'payment']):
            response = "Next payment due Dec 15. Active chits: Gold 12-Month, Diamond Savings"
        elif any(word in prompt.lower() for word in ['loyalty', 'points', 'rewards']):
            response = "Gold tier with 890 points! 100 points = ₹50 discount"
        
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================================================
# MY PURCHASES PAGE (Customer)
# ============================================================================
def my_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    purchases_df = purchases_df[['date', 'item', 'purity', 'weight', 'amount', 'status']]
    purchases_df.columns = ['Date', 'Item', 'Purity', 'Weight', 'Amount', 'Status']
    
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

# ============================================================================
# MY CHITS PAGE (Customer)
# ============================================================================
def my_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)
    
    chits_df = pd.DataFrame({
        'Chit Name': ['Gold 12-Month', 'Diamond Savings'],
        'Amount': [100000, 200000],
        'Status': ['Active', 'Active'],
        'Next Payment': ['2026-01-15', '2026-02-15']
    })
    
    st.dataframe(chits_df, use_container_width=True, hide_index=True)

# ============================================================================
# OFFERS & REWARDS PAGE (Customer)
# ============================================================================
def offers_rewards_page():
    st.markdown("<h2 class='main-title'>🎁 Offers & Rewards</h2>", unsafe_allow_html=True)
    
    for campaign in CAMPAIGN_NOTIFICATIONS:
        st.markdown(f"""
        <div class='campaign-notification'>
            <h4>{campaign['title']}</h4>
            <strong style='color: #ffd700;'>{campaign['discount']}</strong><br>
            {campaign['description']}
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# MY SUMMARY PAGE (Customer)
# ============================================================================
def my_summary_page():
    st.markdown("<h2 class='main-title'>📊 My Summary</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", "₹5,00,000", "Premium")
    with col2:
        st.metric("Purchases", "12", "+2")
    with col3:
        st.metric("Active Chits", "2", "+₹3L")
    with col4:
        st.metric("Loyalty Tier", "Gold", "890 pts")

# ============================================================================
# SETTINGS PAGE (Admin)
# ============================================================================
def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    st.subheader("Account Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        st.text_input("Full Name", value="Manager")
        st.text_input("Email", value="manager@jewellery.com")
    with col2:
        st.text_input("Phone", value="91-XXXXXXXXXX")
        st.selectbox("Theme", ["Luxury Black & Silver (CURRENT)", "Light Mode", "Other"], index=0)
    
    if st.button("💾 Save Settings", use_container_width=True):
        st.success("✅ Settings saved!")

# ============================================================================
# MAIN APP
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
        elif selected_page == "⚡ Quick Actions":
            quick_actions_page()
        elif selected_page == "📢 Campaigns":
            campaigns_page()
        elif selected_page == "💎 Chit Management":
            chit_management_page()
        elif selected_page == "🤖 ML Models":
            ml_models_page()
        elif selected_page == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "🛍️ My Purchases":
            my_purchases_page()
        elif selected_page == "💎 My Chits":
            my_chits_page()
        elif selected_page == "🎁 Offers & Rewards":
            offers_rewards_page()
        elif selected_page == "📊 My Summary":
            my_summary_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
