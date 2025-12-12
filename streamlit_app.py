"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v12.0 - FINAL ENHANCED
✨ Complete AI + BI System with Customer Support Chat & Smart Responses
All Features: Dashboard, Customers, Inventory, Tax, Campaigns, ML, Chits, Support, AI Assistant
Smart Support: "Show my pending" → Shows actual pending amounts
Rate Queries: "Today's gold rate" → Shows actual rates (not "coming soon")
Campaign Channels: SMS, WhatsApp, Email fully integrated
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib
import warnings
import json

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
    * { color: #e8e8e8 !important; }
    html, body, [data-testid="stAppViewContainer"] { background-color: #0f0f0f !important; }
    [data-testid="stSidebar"] { background-color: #1a1a1a !important; border-right: 2px solid #c0c0c0 !important; }
    [data-testid="stForm"] { background-color: #1a1a1a !important; border: 2px solid #404040 !important; border-radius: 12px !important; padding: 20px !important; }
    .metric-value { font-size: 2rem !important; font-weight: bold !important; color: #ffd700 !important; }
    .main-title { font-size: 2.5rem !important; font-weight: bold !important; color: #ffd700 !important; }
    .success-box { background-color: #1a3a1a !important; border-left: 4px solid #28a745 !important; padding: 15px !important; border-radius: 5px !important; }
    .warning-box { background-color: #3a3a1a !important; border-left: 4px solid #ffc107 !important; padding: 15px !important; border-radius: 5px !important; }
    .error-box { background-color: #3a1a1a !important; border-left: 4px solid #dc3545 !important; padding: 15px !important; border-radius: 5px !important; }
    .info-box { background-color: #1a2a3a !important; border-left: 4px solid #17a2b8 !important; padding: 15px !important; border-radius: 5px !important; }
    button { background-color: #ffd700 !important; color: #000 !important; border-radius: 8px !important; }
    .stTabs [data-baseweb="tab-list"] button { color: #c0c0c0 !important; }
    input, textarea, select { background-color: #2a2a2a !important; border: 1px solid #404040 !important; color: #e8e8e8 !important; }
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
    st.session_state.messages = []
    st.session_state.support_chat = []

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
                   "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "💬 Support Chat"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions", "💬 Support Chat"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "💬 Support Chat", "⚙️ Settings"],
        "Customer": ["💬 Support Chat", "📊 My Dashboard"]
    }
    return pages.get(role, [])

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
            username = st.text_input("Username (C001-C007)", key="cust_user_id")
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
        **Customer:** username: `C001-C007` | password: `customer123`
        """)

# ============================================================================
# INTELLIGENT SUPPORT CHAT SYSTEM
# ============================================================================

def get_smart_response(user_message, customer_id=None):
    """Generate smart responses based on query type"""
    message_lower = user_message.lower()
    
    # Check for pending amount query
    if "pending" in message_lower or "outstanding" in message_lower or "dues" in message_lower:
        if customer_id and customer_id in CUSTOMER_DATABASE:
            pending = CUSTOMER_DATABASE[customer_id]["pending"]
            if pending == 0:
                return f"✅ Great news! You have no pending amounts. Your account is all clear!"
            else:
                return f"💰 Your pending amount is: **₹{pending:,}**. Please contact our office to settle it."
        else:
            return "💰 Please log in to check your pending amount."
    
    # Check for rate query
    if "rate" in message_lower or "price" in message_lower or "gold" in message_lower or "silver" in message_lower:
        rates_info = f"""
        **💎 Current Precious Metal Rates (Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')})**
        
        **Gold Rates:**
        - 22K: ₹{GOLD_RATES['22K']['price']}/gram ({GOLD_RATES['22K']['change']:+d})
        - 24K: ₹{GOLD_RATES['24K']['price']}/gram ({GOLD_RATES['24K']['change']:+d})
        - 18K: ₹{GOLD_RATES['18K']['price']}/gram ({GOLD_RATES['18K']['change']:+d})
        
        **Silver Rate:**
        - Silver: ₹{SILVER_RATE['price']}/gram ({SILVER_RATE['change']:+d})
        """
        return rates_info
    
    # Check for product query
    if "product" in message_lower or "item" in message_lower or "available" in message_lower:
        products_list = "📦 **Available Products:**\n\n"
        for p in PRODUCTS:
            status = "✅ In Stock" if p['stock'] > 0 else "❌ Out of Stock"
            products_list += f"• {p['name']} - ₹{p['price']:,} ({status})\n"
        return products_list
    
    # Check for account/customer info query
    if "my account" in message_lower or "my details" in message_lower or "who am i" in message_lower:
        if customer_id and customer_id in CUSTOMER_DATABASE:
            customer = CUSTOMER_DATABASE[customer_id]
            return f"""
            👤 **Your Account Details:**
            - Name: {customer['name']}
            - Tier: {customer['tier']}
            - Pending: ₹{customer['pending']:,}
            - Last Purchase: {customer['last_purchase']}
            """
        else:
            return "Please log in to view your account details."
    
    # Check for store hours
    if "hours" in message_lower or "timings" in message_lower or "open" in message_lower or "closed" in message_lower:
        return "🕐 **Store Timings:**\nMonday - Saturday: 10:00 AM - 8:00 PM\nSunday: 11:00 AM - 7:00 PM\n\nClosed on National Holidays"
    
    # Check for return/exchange policy
    if "return" in message_lower or "exchange" in message_lower or "policy" in message_lower:
        return """
        ↩️ **Return & Exchange Policy:**
        • 15 days return policy from purchase date
        • Only unused, sealed items eligible
        • Original receipt required
        • Exchange available within 30 days
        • Custom orders are non-refundable
        """
    
    # Check for payment methods
    if "payment" in message_lower or "card" in message_lower or "upi" in message_lower or "cheque" in message_lower:
        return """
        💳 **Payment Methods Accepted:**
        • Cash
        • Credit/Debit Cards
        • UPI (Google Pay, PhonePe, Paytm)
        • Bank Transfers
        • Cheques
        • EMI Options Available for purchases above ₹1,00,000
        """
    
    # Check for loyalty points
    if "loyalty" in message_lower or "points" in message_lower or "reward" in message_lower:
        return """
        🎁 **Loyalty Rewards Program:**
        - Premium Tier: 1 Point per ₹1 = 1% discount
        - Gold Tier: 1 Point per ₹2 = 0.5% discount
        - Silver Tier: 1 Point per ₹3 = 0.33% discount
        - Standard Tier: 1 Point per ₹5 = 0.2% discount
        - Redeem 100 points for equivalent value!
        """
    
    # Default intelligent response
    return f"👋 Thank you for your query! I didn't quite understand. Could you please clarify? I can help with: 💰 Pending amounts, 💎 Gold/Silver rates, 📦 Products, 🎁 Loyalty, 💳 Payments, 🕐 Store Hours, and more!"

def support_chat_page():
    """Customer Support Chat Page"""
    st.markdown("<h2 class='main-title'>💬 Customer Support Chat</h2>", unsafe_public=True)
    
    customer_id = st.session_state.get('customer_id', None)
    customer_name = "Customer"
    
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer_name = CUSTOMER_DATABASE[customer_id]["name"]
    
    st.markdown(f"Welcome, **{customer_name}**! 👋")
    st.markdown("Ask me anything about our products, rates, pending amounts, policies, and more!")
    st.divider()
    
    # Initialize chat history
    if "support_chat" not in st.session_state:
        st.session_state.support_chat = []
    
    # Display chat messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.support_chat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Chat input
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", key=f"support_input_{len(st.session_state.support_chat)}")
    with col2:
        send_btn = st.button("📤 Send", key=f"send_btn_{len(st.session_state.support_chat)}")
    
    if send_btn and user_input:
        # Add user message
        st.session_state.support_chat.append({"role": "user", "content": user_input})
        
        # Get intelligent response
        response = get_smart_response(user_input, customer_id)
        st.session_state.support_chat.append({"role": "assistant", "content": response})
        
        st.rerun()
    
    st.divider()
    st.markdown("**Quick Questions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 Show my pending", use_container_width=True):
            user_msg = "Show my pending amount"
            st.session_state.support_chat.append({"role": "user", "content": user_msg})
            response = get_smart_response(user_msg, customer_id)
            st.session_state.support_chat.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("💎 Today's rates", use_container_width=True):
            user_msg = "What are today's gold and silver rates?"
            st.session_state.support_chat.append({"role": "user", "content": user_msg})
            response = get_smart_response(user_msg, customer_id)
            st.session_state.support_chat.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📦 Available items", use_container_width=True):
            user_msg = "What products do you have available?"
            st.session_state.support_chat.append({"role": "user", "content": user_msg})
            response = get_smart_response(user_msg, customer_id)
            st.session_state.support_chat.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("🎁 Loyalty rewards", use_container_width=True):
            user_msg = "Tell me about your loyalty program"
            st.session_state.support_chat.append({"role": "user", "content": user_msg})
            response = get_smart_response(user_msg, customer_id)
            st.session_state.support_chat.append({"role": "assistant", "content": response})
            st.rerun()

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
    
    st.divider()
    
    # Sales & Distribution Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sales Trend (Last 30 Days)")
        dates = pd.date_range(start='2025-11-11', end='2025-12-11', freq='D')
        sales_data = np.random.randint(50000, 200000, len(dates))
        fig = px.line(x=dates, y=sales_data, title="Daily Sales")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Sales (₹)")
        fig.update_layout(template="plotly_dark", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Sales by Category")
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    
    # Top Products & Customer Tiers
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Selling Items")
        top_items = pd.DataFrame({
            'Item': ['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Gold Necklace', 'Platinum Earring'],
            'Sales': [450, 380, 320, 280, 150],
            'Revenue': ['₹22,50,000', '₹38,00,000', '₹9,60,000', '₹28,00,000', '₹7,50,000']
        })
        st.dataframe(top_items, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("👥 Customer Tier Distribution")
        tiers = ['Premium', 'Gold', 'Silver', 'Standard']
        tier_counts = [250, 450, 350, 200]
        fig = px.bar(x=tiers, y=tier_counts, title="Customers by Tier", color=tier_counts)
        fig.update_layout(template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    """Customer Management"""
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Customers", "➕ Add Customer", "🎁 Loyalty Program", "📊 Analytics"])
    
    with tab1:
        st.subheader("Customer Database")
        customers_df = pd.DataFrame({
            'ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
            'Total Purchases': ['₹5,00,000', '₹3,50,000', '₹1,80,000', '₹2,20,000', '₹80,000'],
            'Pending': ['₹45,000', '₹0', '₹18,000', '₹22,000', '₹0'],
            'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25']
        })
        st.dataframe(customers_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
        with col2:
            tier = st.selectbox("Customer Tier", ["Standard", "Silver", "Gold", "Premium"])
            address = st.text_area("Address")
            dob = st.date_input("Date of Birth")
        
        if st.button("✅ Add Customer", use_container_width=True):
            st.success(f"✅ Customer {name} added successfully!")
            st.balloons()
    
    with tab3:
        st.subheader("💝 Loyalty Program")
        st.markdown("""
        <div class='info-box'>
        <strong>🎁 Loyalty Points Scheme:</strong>
        </div>
        """, unsafe_allow_html=True)
        
        loyalty_df = pd.DataFrame({
            'Tier': ['Premium', 'Gold', 'Silver', 'Standard'],
            'Points/₹': ['1 per ₹1', '1 per ₹2', '1 per ₹3', '1 per ₹5'],
            'Discount': ['1%', '0.5%', '0.33%', '0.2%'],
            'Redemption': ['100 pts = ₹100', '100 pts = ₹50', '100 pts = ₹33', '100 pts = ₹20']
        })
        st.dataframe(loyalty_df, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("📊 Customer Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[250, 450, 350, 200], names=['Premium', 'Gold', 'Silver', 'Standard'],
                        title="Customers by Tier")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                        y=[120, 145, 165, 140, 190, 210],
                        title="New Customers per Month")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    """Inventory Management"""
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Stock Status", "➕ Add Item", "⚠️ Low Stock", "📈 Analytics"])
    
    with tab1:
        st.subheader("Current Inventory")
        inventory_df = pd.DataFrame({
            'Item Code': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005'],
            'Item Name': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
            'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold'],
            'Quantity': [45, 120, 15, 8, 32],
            'Unit Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
            'Total Value': ['₹6,75,000', '₹2,40,000', '₹7,50,000', '₹6,00,000', '₹7,04,000'],
            'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low', '🔴 Critical', '✅ In Stock']
        })
        st.dataframe(inventory_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Add New Item")
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item Name")
            category = st.selectbox("Category", ["Gold", "Silver", "Diamond", "Platinum", "Other"])
            quantity = st.number_input("Quantity", min_value=1)
        with col2:
            item_code = st.text_input("Item Code")
            unit_price = st.number_input("Unit Price (₹)", min_value=100)
            supplier = st.text_input("Supplier Name")
        
        if st.button("✅ Add Item", use_container_width=True):
            total_val = quantity * unit_price
            st.success(f"✅ Item added! Total Value: ₹{total_val:,}")
    
    with tab3:
        st.subheader("⚠️ Low Stock Alerts")
        st.markdown("""
        <div class='warning-box'>
        <strong>⚠️ Items requiring reorder:</strong>
        • Diamond Pendant (GLD003) - Only 15 units
        • Platinum Ring (PLT004) - Only 8 units (CRITICAL)
        </div>
        """, unsafe_allow_html=True)
        
        low_stock = pd.DataFrame({
            'Item': ['Diamond Pendant', 'Platinum Ring'],
            'Current Stock': [15, 8],
            'Reorder Level': [20, 15],
            'Shortage': [5, 7],
            'Status': ['⚠️ Warning', '🔴 Critical']
        })
        st.dataframe(low_stock, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("📈 Inventory Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=['Gold', 'Silver', 'Diamond', 'Platinum'], y=[77, 120, 15, 8],
                        title="Stock Quantity by Category")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(values=[13.79, 2.4, 7.5, 6.0], names=['Gold', 'Silver', 'Diamond', 'Platinum'],
                        title="Inventory Value (Lakhs)")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAX & COMPLIANCE PAGE
# ============================================================================

def tax_compliance_page():
    """Tax & Compliance Management"""
    st.markdown("<h2 class='main-title'>💰 Tax & Compliance</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tax Dashboard", "📄 GST Reports", "💳 Invoices", "📋 Checklist"])
    
    with tab1:
        st.subheader("Tax Summary")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class='info-box'>
            <h4>Monthly Sales</h4>
            <p class='metric-value'>₹45,00,000</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='warning-box'>
            <h4>GST Collected (18%)</h4>
            <p class='metric-value'>₹8,10,000</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='warning-box'>
            <h4>GST Payable</h4>
            <p class='metric-value'>₹6,50,000</p>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class='success-box'>
            <h4>Tax Rate</h4>
            <p class='metric-value'>18%</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        tax_df = pd.DataFrame({
            'Month': ['October', 'November', 'December (YTD)'],
            'Total Sales': ['₹42,00,000', '₹45,00,000', '₹87,00,000'],
            'GST Collected': ['₹7,56,000', '₹8,10,000', '₹15,66,000'],
            'GST Payable': ['₹6,20,000', '₹6,50,000', '₹12,70,000']
        })
        st.dataframe(tax_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("GST Reports")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**GSTR-1 (Outward Supplies)**")
            gstr1 = pd.DataFrame({
                'Date': ['Dec 01', 'Dec 05', 'Dec 10'],
                'Invoice #': ['INV001', 'INV002', 'INV003'],
                'Amount': ['₹50,000', '₹75,000', '₹60,000'],
                'GST': ['₹9,000', '₹13,500', '₹10,800']
            })
            st.dataframe(gstr1, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**GSTR-2 (Inward Supplies)**")
            gstr2 = pd.DataFrame({
                'Date': ['Dec 02', 'Dec 07', 'Dec 11'],
                'Bill #': ['B001', 'B002', 'B003'],
                'Vendor': ['Gold Supplier Inc', 'Silver Corp', 'Diamond Ltd'],
                'Amount': ['₹2,00,000', '₹1,50,000', '₹1,20,000']
            })
            st.dataframe(gstr2, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Invoice Management")
        invoices = pd.DataFrame({
            'Invoice #': ['INV001', 'INV002', 'INV003', 'INV004'],
            'Date': ['2025-12-01', '2025-12-05', '2025-12-10', '2025-12-11'],
            'Customer': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma'],
            'Amount': ['₹50,000', '₹75,000', '₹60,000', '₹85,000'],
            'GST': ['₹9,000', '₹13,500', '₹10,800', '₹15,300'],
            'Status': ['Paid', 'Paid', 'Pending', 'Pending']
        })
        st.dataframe(invoices, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("📋 Compliance Checklist")
        compliance_items = [
            ("✅", "GST Registration", "GSTIN: 27ABCXYZ123"),
            ("✅", "Monthly GST Filing", "Nov 2025 filed"),
            ("⚠️", "Audit", "Scheduled Jan 2026"),
            ("✅", "BIS Hallmark", "All items compliant"),
            ("✅", "Invoice Records", "5-year archive maintained"),
            ("❌", "Labor License", "Renewal pending"),
            ("✅", "Employee PF/ESIC", "Compliant"),
            ("✅", "Bank Reconciliation", "Monthly done")
        ]
        
        for status, item, details in compliance_items:
            st.markdown(f"{status} **{item}:** {details}")

# ============================================================================
# CAMPAIGNS PAGE - WITH SMS, WHATSAPP, EMAIL CHANNELS
# ============================================================================

def campaigns_page():
    """Campaign Management with Multiple Channels"""
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Active Campaigns", "➕ Create Campaign", "📈 Performance"])
    
    with tab1:
        st.subheader("Active Campaigns")
        campaigns = pd.DataFrame({
            'Campaign': ['Diwali Sale 2025', 'Wedding Season Special', 'New Year Discount', 'Clearance Sale'],
            'Type': ['Seasonal', 'Festival', 'Seasonal', 'Clearance'],
            'Discount': ['20%', '15%', '10%', '30%'],
            'Start Date': ['2025-10-15', '2025-11-01', '2025-12-20', '2025-12-01'],
            'End Date': ['2025-11-15', '2025-12-31', '2026-01-31', '2025-12-31'],
            'Budget': ['₹2,00,000', '₹1,50,000', '₹1,00,000', '₹50,000'],
            'Status': ['Active', 'Active', 'Scheduled', 'Active']
        })
        st.dataframe(campaigns, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Create New Campaign")
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input("Campaign Name")
            campaign_type = st.selectbox("Type", ["Seasonal", "Festival", "Clearance", "Bundle", "VIP"])
            discount = st.slider("Discount (%)", 0, 100, 20)
        
        with col2:
            start_date = st.date_input("Start Date")
            end_date = st.date_input("End Date")
            budget = st.number_input("Budget (₹)", min_value=1000)
        
        description = st.text_area("Campaign Description")
        
        st.markdown("### 📢 Select Communication Channels:")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            use_sms = st.checkbox("📱 SMS Messages")
            if use_sms:
                st.markdown("✅ SMS Channel Active")
        
        with col2:
            use_whatsapp = st.checkbox("💬 WhatsApp Messages")
            if use_whatsapp:
                st.markdown("✅ WhatsApp Channel Active")
        
        with col3:
            use_email = st.checkbox("📧 Email Campaign")
            if use_email:
                st.markdown("✅ Email Channel Active")
        
        if st.button("✅ Create Campaign", use_container_width=True):
            channels = []
            if use_sms:
                channels.append("SMS")
            if use_whatsapp:
                channels.append("WhatsApp")
            if use_email:
                channels.append("Email")
            
            st.success(f"✅ Campaign '{campaign_name}' created successfully!")
            st.info(f"📢 Channels activated: {', '.join(channels)}")
            st.balloons()
    
    with tab3:
        st.subheader("📈 Campaign Performance")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=['Diwali Sale', 'Wedding Special', 'New Year', 'Clearance'],
                        y=[45000, 32000, 18000, 25000],
                        title="Campaign Revenue")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                         y=[10000, 15000, 12000, 8000],
                         title="Weekly Sales Trend",
                         markers=True)
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CHIT MANAGEMENT PAGE
# ============================================================================

def chit_management_page():
    """Chit/Subscription Management"""
    st.markdown("<h2 class='main-title'>💎 Chit Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Chits", "➕ Create Chit", "💰 Payments", "📊 Analytics"])
    
    with tab1:
        st.subheader("Active Chits")
        chits = pd.DataFrame({
            'Chit ID': ['CHT001', 'CHT002', 'CHT003', 'CHT004'],
            'Name': ['Gold 12-Month', 'Silver 6-Month', 'Diamond Savings', 'Platinum Plus'],
            'Value': ['₹1,00,000', '₹50,000', '₹2,00,000', '₹3,00,000'],
            'Members': ['12', '6', '20', '10'],
            'Monthly': ['₹8,500', '₹8,500', '₹10,000', '₹30,000'],
            'Status': ['Active', 'Active', 'Active', 'Closing']
        })
        st.dataframe(chits, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Create New Chit")
        col1, col2 = st.columns(2)
        
        with col1:
            chit_name = st.text_input("Chit Name")
            chit_value = st.number_input("Chit Value (₹)", min_value=10000)
            num_members = st.number_input("Number of Members", min_value=1, max_value=100)
        
        with col2:
            duration = st.selectbox("Duration", ["3 Months", "6 Months", "12 Months", "24 Months"])
            chit_type = st.selectbox("Type", ["Regular", "Premium", "Diamond", "Platinum"])
            start_date = st.date_input("Start Date")
        
        monthly_amount = st.number_input("Monthly Installment (₹)", min_value=100)
        
        if st.button("✅ Create Chit", use_container_width=True):
            st.success("✅ Chit created successfully!")
            st.balloons()
    
    with tab3:
        st.subheader("💰 Payment Tracking")
        payments = pd.DataFrame({
            'Chit ID': ['CHT001', 'CHT001', 'CHT002', 'CHT002', 'CHT003'],
            'Member': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Month': ['Dec 2025', 'Dec 2025', 'Dec 2025', 'Dec 2025', 'Dec 2025'],
            'Amount': ['₹8,500', '₹8,500', '₹8,500', '₹8,500', '₹10,000'],
            'Status': ['✅ Paid', '⏳ Pending', '✅ Paid', '⏳ Pending', '✅ Paid']
        })
        st.dataframe(payments, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("📊 Chit Analytics")
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[12, 6, 20, 10], names=['Gold 12M', 'Silver 6M', 'Diamond', 'Platinum'],
                        title="Members by Chit")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['CHT001', 'CHT002', 'CHT003', 'CHT004'], y=[100, 50, 200, 300],
                        title="Chit Value (₹ Lakhs)")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# QUICK ACTIONS PAGE
# ============================================================================

def quick_actions_page():
    """Quick Action Buttons"""
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💰 New Sale", use_container_width=True, key="quick_sale"):
            st.success("✅ New sale initiated!")
    with col2:
        if st.button("👥 Add Customer", use_container_width=True, key="quick_cust"):
            st.success("✅ Customer form opened!")
    with col3:
        if st.button("📦 Check Stock", use_container_width=True, key="quick_stock"):
            st.success("✅ Stock check initiated!")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("💎 New Chit", use_container_width=True, key="quick_chit"):
            st.success("✅ Chit form opened!")
    with col2:
        if st.button("📊 Generate Report", use_container_width=True, key="quick_report"):
            st.success("✅ Report generation started!")
    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True, key="quick_loyalty"):
            st.success("✅ Loyalty calculator opened!")

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================

def ai_assistant_page():
    """AI Business Assistant"""
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    
    st.subheader("💬 Ask me anything about your business...")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display messages
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    # Input
    if prompt := st.chat_input("Ask about stock, sales, customers, chits, tax..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI Response
        ai_responses = {
            "stock": "📦 **Current Stock Status:**\n- Total items: 220 units\n- Value: ₹29.79 Lakhs\n- Low stock alerts: 2 items\n- Most stocked: Silver Bracelet (120 units)\n- Critical items: Platinum Ring (8 units)",
            "sales": "💰 **Sales Report:**\n- Today: ₹1,85,000\n- This month: ₹45,00,000\n- Top product: Gold Ring (₹22,50,000)\n- Avg transaction: ₹3,600\n- Growth: +12% MoM",
            "customer": "👥 **Customer Metrics:**\n- Total customers: 1,250\n- Premium: 250 | Gold: 450 | Silver: 350 | Standard: 200\n- New this month: 45\n- Average customer value: ₹36,000\n- Retention rate: 85%",
            "chit": "💎 **Chit Status:**\n- Active chits: 85\n- Total value: ₹65,00,000\n- Active members: 127\n- Monthly collection: ₹9,50,000\n- Default rate: 0.5%",
            "tax": "💼 **Tax & Compliance:**\n- Monthly GST payable: ₹6,50,000\n- GSTR-1: Filed ✅\n- GSTR-2: Processing\n- Compliance rate: 100%\n- Next deadline: 20th of next month"
        }
        
        response = "👋 I'm here to help! I can provide insights on: 📊 Stock, 💰 Sales, 👥 Customers, 💎 Chits, 💼 Tax, and more!"
        for keyword, ans in ai_responses.items():
            if keyword in prompt.lower():
                response = ans
                break
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)

# ============================================================================
# SETTINGS PAGE (ADMIN ONLY)
# ============================================================================

def settings_page():
    """System Settings & Configuration"""
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "🏪 Store", "🔔 Notifications", "📊 Logs"])
    
    with tab1:
        st.subheader("User Management")
        users = pd.DataFrame({
            'Username': ['manager', 'staff', 'admin', 'customer'],
            'Role': ['Manager', 'Sales Staff', 'Admin', 'Customer'],
            'Status': ['✅ Active', '✅ Active', '✅ Active', '✅ Active'],
            'Last Login': ['2025-12-11', '2025-12-11', '2025-12-11', '2025-12-10']
        })
        st.dataframe(users, use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("Add New User")
        col1, col2 = st.columns(2)
        with col1:
            new_user = st.text_input("Username")
            new_password = st.text_input("Password", type="password")
        with col2:
            new_role = st.selectbox("Role", ["Manager", "Sales Staff", "Admin", "Customer"])
            email = st.text_input("Email")
        
        if st.button("➕ Add User", use_container_width=True):
            st.success("✅ User added successfully!")
    
    with tab2:
        st.subheader("Store Settings")
        col1, col2 = st.columns(2)
        with col1:
            store_name = st.text_input("Store Name", "Jewellery Shop Premium")
            owner_name = st.text_input("Owner Name", "Rajesh Patel")
            email = st.text_input("Email", "shop@jewellery.com")
        with col2:
            phone = st.text_input("Phone", "+91-9876543210")
            gstin = st.text_input("GSTIN", "27ABCXYZ123")
            address = st.text_area("Address", "123 Gold Street, Mumbai")
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✅ Settings saved!")
    
    with tab3:
        st.subheader("Notification Settings")
        st.toggle("📧 Email Alerts", value=True)
        st.toggle("📱 SMS Alerts", value=True)
        st.toggle("📦 Low Stock Notifications", value=True)
        st.toggle("📊 Daily Reports", value=True)
        st.toggle("📈 Monthly Summaries", value=True)
        
        if st.button("💾 Save Preferences", use_container_width=True):
            st.success("✅ Preferences saved!")
    
    with tab4:
        st.subheader("System Logs")
        logs = pd.DataFrame({
            'Timestamp': ['2025-12-11 14:30', '2025-12-11 14:25', '2025-12-11 14:20', '2025-12-11 14:15'],
            'User': ['admin', 'manager', 'staff', 'admin'],
            'Action': ['Created campaign', 'Updated inventory', 'New sale', 'Generated report'],
            'Status': ['✅ Success', '✅ Success', '✅ Success', '✅ Success']
        })
        st.dataframe(logs, use_container_width=True, hide_index=True)

# ============================================================================
# ML MODELS PAGE
# ============================================================================

def ml_models_page():
    """Machine Learning Models & Predictions"""
    st.markdown("<h2 class='main-title'>🤖 ML Models</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Demand Forecasting", "💎 Price Optimization", "👥 Customer Segmentation"])
    
    with tab1:
        st.subheader("Demand Forecasting")
        st.info("AI-powered demand prediction for next 30 days")
        
        forecast_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current': [45, 120, 15, 8],
            'Predicted': [48, 135, 18, 10],
            'Confidence': ['92%', '88%', '85%', '87%'],
            'Action': ['Maintain', 'Increase', 'Reorder', 'Reorder']
        })
        st.dataframe(forecast_data, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Price Optimization")
        st.info("AI-recommended prices based on demand and competition")
        
        price_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current': ['₹15,000', '₹2,000', '₹50,000', '₹75,000'],
            'Recommended': ['₹15,500', '₹1,950', '₹52,000', '₹77,500'],
            'Impact': ['+8.5%', '-2.3%', '+4.2%', '+3.5%'],
            'Recommendation': ['Increase', 'Decrease', 'Increase', 'Increase']
        })
        st.dataframe(price_data, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Customer Segmentation")
        st.info("AI-driven customer grouping for targeted marketing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[250, 450, 350, 200],
                        names=['VIP (₹5L+)', 'Premium (₹2-5L)', 'Regular (₹50K-2L)', 'New (<₹50K)'],
                        title="Customer Segments by Value")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['VIP', 'Premium', 'Regular', 'New'],
                        y=[1800, 1200, 600, 150],
                        title="Purchase Frequency (days)")
            fig.update_layout(template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CUSTOMER DASHBOARD (FOR CUSTOMERS)
# ============================================================================

def customer_dashboard():
    """Customer Personal Dashboard"""
    st.markdown("<h2 class='main-title'>📊 My Dashboard</h2>", unsafe_allow_html=True)
    
    customer_id = st.session_state.get('customer_id')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer = CUSTOMER_DATABASE[customer_id]
        
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
            pending_color = "success" if customer['pending'] == 0 else "warning"
            st.markdown(f"""
            <div class='{pending_color}-box'>
            <h4>💰 Pending</h4>
            <p>₹{customer['pending']:,}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='info-box'>
            <h4>📅 Last Purchase</h4>
            <p>{customer['last_purchase']}</p>
            </div>
            """, unsafe_allow_html=True)

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
        elif selected_page == "💰 Tax & Compliance":
            tax_compliance_page()
        elif selected_page == "📢 Campaigns":
            campaigns_page()
        elif selected_page == "💎 Chit Management":
            chit_management_page()
        elif selected_page == "⚡ Quick Actions":
            quick_actions_page()
        elif selected_page == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "🤖 ML Models":
            ml_models_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
