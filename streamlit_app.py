"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v7.1 ✨
FIXED VERSION - ERROR RECTIFIED
- Fixed requirements installation
- Added Pending Customers page to Manager
- Added Campaign notifications to Customer login
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
    page_title="💎 Jewellery AI Dashboard v7.1",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# LUXURY DARK THEME
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #0f0f0f !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 2px solid #c0c0c0 !important; }
    h1, h2, h3, h4, h5, h6 { color: #c0c0c0 !important; letter-spacing: 1px; }
    .main-title { font-size: 2.5rem; font-weight: bold; color: #c0c0c0 !important; text-shadow: 2px 2px 8px rgba(192, 192, 192, 0.3); }
    .info-box { background: linear-gradient(135deg, #1a3a3a 0%, #1a2a3a 100%) !important; border-left: 4px solid #c0c0c0 !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; }
    .success-box { background: linear-gradient(135deg, #1a3a1a 0%, #1a2a1a 100%) !important; border-left: 4px solid #7cb342 !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; }
    .warning-box { background: linear-gradient(135deg, #3a3a1a 0%, #2a2a1a 100%) !important; border-left: 4px solid #fbc02d !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; }
    .campaign-notification { background: linear-gradient(135deg, #3a2a1a 0%, #2a1f0a 100%) !important; border-left: 5px solid #ffd700 !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; margin: 10px 0 !important; box-shadow: 0 4px 12px rgba(255, 215, 0, 0.1) !important; }
    .pending-box { background: linear-gradient(135deg, #3a2a1a 0%, #2a2a0f 100%) !important; border: 2px solid #ff9800 !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; margin: 10px 0 !important; }
    input, textarea, select { background-color: #1a1a1a !important; border: 1px solid #404040 !important; color: #e8e8e8 !important; border-radius: 6px !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.chatbot_messages = []

# ============================================================================
# LIVE MARKET DATA
# ============================================================================
TODAY_RATES = {
    "gold": {"current": 7850, "previous": 7800, "change": 50, "change_percent": 0.64, "currency": "₹", "unit": "per gram"},
    "silver": {"current": 95, "previous": 92, "change": 3, "change_percent": 3.26, "currency": "₹", "unit": "per gram"}
}

# ============================================================================
# SAMPLE DATA
# ============================================================================
CUSTOMER_PURCHASES = [
    {"date": "2025-12-08", "item": "Gold Ring", "purity": "22K", "weight": "5.2g", "amount": 45000, "status": "Delivered"},
    {"date": "2025-11-25", "item": "Silver Bracelet", "purity": "92.5%", "weight": "45g", "amount": 8500, "status": "Delivered"},
    {"date": "2025-11-15", "item": "Gold Necklace", "purity": "18K", "weight": "12.5g", "amount": 85000, "status": "Delivered"},
]

PENDING_PAYMENTS = [
    {"item": "Gold Bangles (Wedding Set)", "amount": 45000, "due_date": "2025-12-15", "status": "Pending Payment"},
    {"item": "Diamond Ring", "amount": 85000, "due_date": "2025-12-20", "status": "Pending Payment"},
    {"item": "Silver Set", "amount": 12000, "due_date": "2025-12-18", "status": "Pending Payment"},
]

# ALL CAMPAIGN NOTIFICATIONS (SHOWN TO CUSTOMERS)
CAMPAIGN_NOTIFICATIONS = [
    {
        "title": "🎄 Christmas Special Offer",
        "discount": "20% OFF",
        "description": "Get 20% discount on all gold items",
        "valid": "Till Dec 31, 2025",
        "status": "Active",
        "code": "XMAS20"
    },
    {
        "title": "💒 Wedding Season Sale",
        "discount": "15% OFF",
        "description": "Special discount on bridal collections",
        "valid": "Till Mar 31, 2026",
        "status": "Active",
        "code": "WEDDING15"
    },
    {
        "title": "✨ New Year New Look",
        "discount": "25% OFF",
        "description": "Exclusive offers on selected items",
        "valid": "Dec 25 - Jan 15",
        "status": "Upcoming",
        "code": "NEWYEAR25"
    },
    {
        "title": "🎁 Loyalty Rewards Program",
        "discount": "Extra Points",
        "description": "Earn 5X loyalty points on purchases",
        "valid": "Ongoing",
        "status": "Active",
        "code": "LOYALTY5X"
    }
]

# ============================================================================
# AUTHENTICATION
# ============================================================================
USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager", "name": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff", "name": "Sales Staff"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer", "name": "Customer"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin", "name": "Admin"}
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 AI Assistant"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "⚡ Quick Actions", "🤖 AI Assistant"],
        "Customer": ["💎 My Dashboard", "🛍️ My Purchases", "💳 My Pending Payments", "💎 My Chits", "🎁 All Offers & Rewards", "📊 My Summary", "💬 Support Chat"],
        "Admin": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 AI Assistant", "⚙️ Settings"]
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
        
        username = st.text_input("Username", key="user_id")
        password = st.text_input("Password", type="password", key="pass_id")
        
        if st.button("Login", use_container_width=True, key="login_btn"):
            if username in USERS and hashlib.sha256(password.encode()).hexdigest() == USERS[username]["password"]:
                st.session_state.authenticated = True
                st.session_state.user_role = USERS[username]["role"]
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
# PENDING CUSTOMERS PAGE (NEW)
# ============================================================================
def pending_customers_page():
    st.markdown("<h2 class='main-title'>💳 Pending Customers</h2>", unsafe_allow_html=True)
    
    customers_df = load_mock_customers()
    pending = customers_df[customers_df['Pending Amount'] > 0].sort_values('Pending Amount', ascending=False)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pending Customers", len(pending))
    with col2:
        st.metric("Total Pending Amount", f"₹{pending['Pending Amount'].sum():,}")
    with col3:
        avg = pending['Pending Amount'].mean() if len(pending) > 0 else 0
        st.metric("Avg Per Customer", f"₹{avg:,.0f}")
    
    st.divider()
    
    st.subheader("📋 All Pending Customers")
    display_df = pending[['ID', 'Name', 'Tier', 'Total Purchases', 'Pending Amount', 'Last Purchase', 'phone']].copy()
    display_df.columns = ['ID', 'Name', 'Tier', 'Total Purchases', 'Pending Amount', 'Last Purchase', 'Phone']
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.subheader("🎯 Payment Collection Campaigns")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📢 Send Payment Reminder SMS", use_container_width=True):
            st.success(f"✅ SMS reminder sent to {len(pending)} customers!")
    with col2:
        if st.button("📧 Send Email Reminder", use_container_width=True):
            st.success(f"✅ Email reminder sent to {len(pending)} customers!")
    
    st.divider()
    
    st.subheader("💬 Send Custom Payment Message")
    col1, col2 = st.columns([2, 1])
    with col1:
        message = st.text_area("Message Template", value="""Hi {name},

Your pending payment: ₹{pending:,}

Please pay at your earliest convenience.

Thanks!
Shree Jewels""", height=120)
    with col2:
        if st.button("Send", use_container_width=True):
            st.success(f"✅ Messages sent to {len(pending)} customers!")

# ============================================================================
# CUSTOMER DASHBOARD WITH CAMPAIGNS
# ============================================================================
def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)
    
    # Live Market Rates
    st.subheader("📊 Today's Live Market Rates")
    col1, col2 = st.columns(2)
    
    with col1:
        gold = TODAY_RATES["gold"]
        change_color = "🔼" if gold['change'] > 0 else "🔽"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3a2a1a 0%, #2a1a0a 100%); border: 2px solid #ffd700; border-radius: 10px; padding: 20px; text-align: center; color: #ffd700; box-shadow: 0 4px 16px rgba(255, 215, 0, 0.15);'>
            <h3>⭐ GOLD</h3>
            <h2>{gold['current']}{gold['unit'].split()[1]}</h2>
            <p>{change_color} {gold['currency']}{gold['change']} ({gold['change_percent']:.2f}%)</p>
            <small>Previous: ₹{gold['previous']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        silver = TODAY_RATES["silver"]
        change_color = "🔼" if silver['change'] > 0 else "🔽"
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #2a2a3a 0%, #1a1a2a 100%); border: 2px solid #c0c0c0; border-radius: 10px; padding: 20px; text-align: center; color: #c0c0c0; box-shadow: 0 4px 16px rgba(192, 192, 192, 0.15);'>
            <h3>✨ SILVER</h3>
            <h2>{silver['current']}{silver['unit'].split()[1]}</h2>
            <p>{change_color} {silver['currency']}{silver['change']} ({silver['change_percent']:.2f}%)</p>
            <small>Previous: ₹{silver['previous']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Account Summary
    st.subheader("📈 Your Account Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Total Spent", "₹5,00,000", "Premium")
    with col2:
        st.metric("🛍️ Total Purchases", "12", "+2")
    with col3:
        st.metric("🎁 Loyalty Points", "850", "100pts = ₹50")
    with col4:
        st.metric("👑 Your Tier", "Gold", "Premium Member")

# ============================================================================
# CUSTOMER PENDING PAYMENTS
# ============================================================================
def customer_pending_payments_page():
    st.markdown("<h2 class='main-title'>💳 My Pending Payments</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='info-box'>
        <strong>📌 Pending Payment Details</strong><br>
        View all your pending payments and due dates
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if PENDING_PAYMENTS:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Pending Items", len(PENDING_PAYMENTS))
        with col2:
            total = sum(p['amount'] for p in PENDING_PAYMENTS)
            st.metric("Total Pending Amount", f"₹{total:,}")
        with col3:
            avg = total / len(PENDING_PAYMENTS) if PENDING_PAYMENTS else 0
            st.metric("Average Per Item", f"₹{avg:,.0f}")
        
        st.divider()
        
        st.subheader("📋 Your Pending Payments")
        
        for idx, payment in enumerate(PENDING_PAYMENTS, 1):
            st.markdown(f"""
            <div class='pending-box'>
                <strong>#{idx}. {payment['item']}</strong><br>
                <strong style='color: #ff9800; font-size: 1.2rem;'>₹{payment['amount']:,}</strong><br>
                <small>Due Date: {payment['due_date']}</small><br>
                <strong style='color: #ff9800;'>{payment['status']}</strong>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"💳 Pay Now", key=f"pay_{idx}", use_container_width=True):
                    st.success(f"✅ Payment of ₹{payment['amount']:,} processed successfully!")
            with col2:
                if st.button(f"📅 Schedule", key=f"schedule_{idx}", use_container_width=True):
                    st.info(f"Payment scheduled for {payment['due_date']}")
            with col3:
                if st.button(f"📧 Email Details", key=f"email_{idx}", use_container_width=True):
                    st.success("✅ Payment details sent to your email!")
            
            st.divider()
    else:
        st.success("✅ No pending payments! You're all caught up!")

# ============================================================================
# ALL OFFERS & REWARDS (CUSTOMER VIEW)
# ============================================================================
def all_offers_rewards_page():
    st.markdown("<h2 class='main-title'>🎁 All Offers & Rewards from Our Shop</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>✨ Exclusive Offers Tailored for You!</strong><br>
        All active campaigns and rewards available at our shop
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Filter by status
    col1, col2, col3 = st.columns(3)
    with col1:
        active = len([c for c in CAMPAIGN_NOTIFICATIONS if c['status'] == 'Active'])
        st.metric("🟢 Active Offers", active)
    with col2:
        upcoming = len([c for c in CAMPAIGN_NOTIFICATIONS if c['status'] == 'Upcoming'])
        st.metric("🟡 Upcoming Offers", upcoming)
    with col3:
        total = len(CAMPAIGN_NOTIFICATIONS)
        st.metric("📊 Total Offers", total)
    
    st.divider()
    
    st.subheader("🎯 All Available Campaigns")
    
    for campaign in CAMPAIGN_NOTIFICATIONS:
        status_emoji = "🟢" if campaign['status'] == 'Active' else "🟡"
        
        st.markdown(f"""
        <div class='campaign-notification'>
            <h4>{status_emoji} {campaign['title']}</h4>
            <strong style='color: #ffd700; font-size: 1.2rem;'>{campaign['discount']}</strong><br>
            <p>{campaign['description']}</p>
            <small><strong>Code:</strong> {campaign['code']}</small><br>
            <small>Valid: {campaign['valid']}</small><br>
            <strong style='color: #7cb342;'>{campaign['status']}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"📖 Details", key=f"details_{campaign['title']}", use_container_width=True):
                st.info(f"""
                **{campaign['title']}**
                
                {campaign['description']}
                
                **Discount:** {campaign['discount']}
                **Code:** {campaign['code']}
                **Valid:** {campaign['valid']}
                """)
        with col2:
            if st.button(f"🛒 Shop Now", key=f"shop_{campaign['title']}", use_container_width=True):
                st.success("Redirecting to shop... 🛒")
        
        st.divider()

# ============================================================================
# DASHBOARD PAGE
# ============================================================================
def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📈 Total Sales", "₹25,50,000", "+₹5,00,000")
    with col2:
        st.metric("👥 Total Customers", "1,250", "+45")
    with col3:
        st.metric("💎 Stock Value", "₹45,00,000", "-₹2,00,000")
    with col4:
        st.metric("💰 Active Chits", "85", "+12")

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================
def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["All Customers", "At Risk", "VIP Management", "Pending Customers"])
    
    customers_df = load_mock_customers()
    
    with tab1:
        st.subheader("📋 Customer List")
        col1, col2 = st.columns(2)
        with col1:
            search_name = st.text_input("Search by Name", key="search_cust")
        with col2:
            filter_tier = st.selectbox("Filter by Tier", ["All", "Premium", "Gold", "Silver", "Standard"], key="filter_tier")
        
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
        st.subheader("⚠️ At-Risk Customers (90+ days)")
        at_risk = customers_df.copy()
        at_risk['days_inactive'] = np.random.randint(90, 180, len(at_risk))
        st.dataframe(at_risk[['Name', 'Tier', 'days_inactive', 'Pending Amount']], use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("👑 VIP Customers")
        vip = customers_df[customers_df['Tier'] == 'Premium']
        st.dataframe(vip, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("💳 Pending Customers")
        pending = customers_df[customers_df['Pending Amount'] > 0]
        st.dataframe(pending, use_container_width=True, hide_index=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================
def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)
    
    inventory_df = load_mock_inventory()
    st.dataframe(inventory_df, use_container_width=True, hide_index=True)

# ============================================================================
# QUICK ACTIONS PAGE
# ============================================================================
def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Generate Report", use_container_width=True):
            st.success("✅ Report generated!")
    with col2:
        if st.button("💳 Process Payments", use_container_width=True):
            st.success("✅ 5 payments processed!")
    with col3:
        if st.button("📦 Stock Check", use_container_width=True):
            st.success("✅ Stock check completed!")
    with col4:
        if st.button("📧 Send Campaigns", use_container_width=True):
            st.success("✅ Campaigns sent!")

# ============================================================================
# CAMPAIGNS PAGE
# ============================================================================
def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Create Campaign", "Active Campaigns", "Reports"])
    
    with tab1:
        st.subheader("Create New Campaign")
        name = st.text_input("Campaign Name")
        ctype = st.selectbox("Type", ["Festival", "Seasonal", "Special"])
        discount = st.slider("Discount %", 0, 50, 10)
        if st.button("Launch", use_container_width=True):
            st.success(f"✅ Campaign '{name}' launched!")
    
    with tab2:
        st.subheader("Active Campaigns")
        active_df = pd.DataFrame({
            'Campaign': ['Diwali Special', 'New Year', 'Wedding'],
            'Status': ['Active', 'Active', 'Active'],
            'Reach': [180, 200, 150]
        })
        st.dataframe(active_df, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Campaign Reports")
        st.metric("Avg Open Rate", "58%")

# ============================================================================
# CHIT MANAGEMENT PAGE
# ============================================================================
def chit_management_page():
    st.markdown("<h2 class='main-title'>💎 Chit Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Schedule", "Pre-Order"])
    
    with tab1:
        st.metric("Upcoming Payouts", 4)
    with tab2:
        st.metric("Pre-Order Items", 12)

# ============================================================================
# ML MODELS PAGE
# ============================================================================
def ml_models_page():
    st.markdown("<h2 class='main-title'>🤖 ML Models</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Risk Scoring", "Forecast", "Pricing"])
    with tab1:
        st.metric("High Risk Customers", 5)
    with tab2:
        st.metric("30-Day Forecast", "₹25,00,000")
    with tab3:
        st.metric("Pricing Optimization", "15% potential gain")

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================
def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>AI Business Insights</strong><br>
        - Sales trending up 15% this month
        - 87% customers are repeat buyers
        - Profit margin at 28% average
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SUPPORT CHAT PAGE
# ============================================================================
def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🛍️ My Purchases", use_container_width=True):
            st.session_state.chatbot_messages.append({"role": "assistant", "content": "You have 4 purchases. Latest: Gold Ring - Dec 10, ₹45,000"})
    with col2:
        if st.button("💎 My Chits", use_container_width=True):
            st.session_state.chatbot_messages.append({"role": "assistant", "content": "Active chits: Gold 12-Month, Diamond Savings. Next payment: Dec 15"})
    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True):
            st.session_state.chatbot_messages.append({"role": "assistant", "content": "Gold Tier - 850 points. 100 points = ₹50 discount!"})
    
    if st.session_state.chatbot_messages:
        for msg in st.session_state.chatbot_messages:
            if msg["role"] == "assistant":
                st.markdown(f"<div class='info-box'>{msg['content']}</div>", unsafe_allow_html=True)
            else:
                st.write(f"**You:** {msg['content']}")

# ============================================================================
# MY PURCHASES
# ============================================================================
def my_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

# ============================================================================
# MY CHITS
# ============================================================================
def my_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)
    chits = pd.DataFrame({
        'Chit': ['Gold 12-Month', 'Diamond Savings'],
        'Amount': [100000, 200000],
        'Status': ['Active', 'Active']
    })
    st.dataframe(chits, use_container_width=True, hide_index=True)

# ============================================================================
# MY SUMMARY
# ============================================================================
def my_summary_page():
    st.markdown("<h2 class='main-title'>📊 My Summary</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", "₹5,00,000")
    with col2:
        st.metric("Total Purchases", "12")
    with col3:
        st.metric("Active Chits", "2")
    with col4:
        st.metric("Loyalty Tier", "Gold")

# ============================================================================
# SETTINGS PAGE
# ============================================================================
def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    st.text_input("Full Name", value="Manager")
    st.text_input("Email", value="manager@jewellery.com")
    if st.button("Save", use_container_width=True):
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
        
        # Route pages
        if selected_page == "📊 Dashboard":
            dashboard_page()
        elif selected_page == "💎 My Dashboard":
            customer_dashboard_page()
        elif selected_page == "👥 Customers":
            customers_page()
        elif selected_page == "💳 Pending Customers":
            pending_customers_page()
        elif selected_page == "💳 My Pending Payments":
            customer_pending_payments_page()
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
        elif selected_page == "🎁 All Offers & Rewards":
            all_offers_rewards_page()
        elif selected_page == "📊 My Summary":
            my_summary_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
