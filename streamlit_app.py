"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v13.0 - CLEAN & PROFESSIONAL
✨ Complete AI + BI System with Enhanced ML, AI Assistant, and Customer Support
Clean Professional Theme + Pending Customers + Slow Stock + Advanced ML Models
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
# PAGE CONFIG - CLEAN PROFESSIONAL THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# CLEAN PROFESSIONAL THEME
st.markdown("""
<style>
    /* Clean Light Professional Theme */
    * { margin: 0; padding: 0; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
    }
    
    [data-testid="stSidebar"] { 
        background-color: #ffffff !important;
        border-right: 1px solid #e0e6ed !important;
    }
    
    [data-testid="stForm"] { 
        background-color: #ffffff !important;
        border: 1px solid #e0e6ed !important;
        border-radius: 8px !important;
        padding: 20px !important;
    }
    
    .main-title { 
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #1a365d !important;
        margin-bottom: 8px !important;
    }
    
    .metric-value { 
        font-size: 1.8rem !important;
        font-weight: 600 !important;
        color: #2d3748 !important;
    }
    
    .success-card { 
        background: linear-gradient(135deg, #f0fff4 0%, #e6fffa 100%) !important;
        border-left: 4px solid #22863a !important;
        padding: 16px !important;
        border-radius: 6px !important;
    }
    
    .info-card { 
        background: linear-gradient(135deg, #f0f7ff 0%, #f0f9ff 100%) !important;
        border-left: 4px solid #0366d6 !important;
        padding: 16px !important;
        border-radius: 6px !important;
    }
    
    .warning-card { 
        background: linear-gradient(135deg, #fff8f0 0%, #ffe8cc 100%) !important;
        border-left: 4px solid #d97706 !important;
        padding: 16px !important;
        border-radius: 6px !important;
    }
    
    .danger-card { 
        background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%) !important;
        border-left: 4px solid #cb2431 !important;
        padding: 16px !important;
        border-radius: 6px !important;
    }
    
    button { 
        background-color: #0366d6 !important;
        color: white !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 600 !important;
    }
    
    button:hover {
        background-color: #0256c7 !important;
    }
    
    [data-baseweb="tab-list"] button {
        color: #586069 !important;
        border-bottom: 2px solid transparent !important;
    }
    
    [aria-selected="true"] {
        color: #0366d6 !important;
        border-bottom: 2px solid #0366d6 !important;
    }
    
    input, textarea, select { 
        background-color: #ffffff !important;
        border: 1px solid #d0d7de !important;
        color: #2c3e50 !important;
        padding: 8px 12px !important;
        border-radius: 6px !important;
    }
    
    input:focus, textarea:focus, select:focus {
        border-color: #0366d6 !important;
        box-shadow: 0 0 0 3px rgba(3,102,214,0.1) !important;
    }
    
    .stDataFrame { background-color: white !important; }
    [data-testid="stTable"] { background-color: white !important; }
    
    .metric-label { color: #586069 !important; font-size: 0.875rem !important; }
    
    h1, h2, h3, h4, h5, h6 { color: #1a365d !important; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.messages = []
    st.session_state.support_chat = []

# ============================================================================
# SAMPLE DATA
# ============================================================================

GOLD_RATES = {
    "22K": {"price": 7250, "change": 50, "currency": "₹/gram"},
    "24K": {"price": 7950, "change": 75, "currency": "₹/gram"},
    "18K": {"price": 6200, "change": 40, "currency": "₹/gram"}
}

SILVER_RATE = {"price": 95, "change": 2, "currency": "₹/gram"}

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
    {"id": "P001", "name": "Gold Ring", "category": "Gold", "stock": 45, "price": 15000, "sku": "GLD001"},
    {"id": "P002", "name": "Silver Bracelet", "category": "Silver", "stock": 120, "price": 2000, "sku": "SLV002"},
    {"id": "P003", "name": "Diamond Pendant", "category": "Diamond", "stock": 15, "price": 50000, "sku": "DMD003"},
    {"id": "P004", "name": "Platinum Ring", "category": "Platinum", "stock": 8, "price": 75000, "sku": "PLT004"},
    {"id": "P005", "name": "Gold Necklace", "category": "Gold", "stock": 32, "price": 22000, "sku": "GLD005"},
    {"id": "P006", "name": "Silver Earrings", "category": "Silver", "stock": 50, "price": 3500, "sku": "SLV006"},
]

# ============================================================================
# AUTHENTICATION
# ============================================================================

USERS = {
    "manager": {"password": hashlib.sha256("manager123".encode()).hexdigest(), "role": "Manager"},
    "staff": {"password": hashlib.sha256("staff123".encode()).hexdigest(), "role": "Sales Staff"},
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "role": "Admin"},
    "customer": {"password": hashlib.sha256("customer123".encode()).hexdigest(), "role": "Customer"}
}

def get_accessible_pages(role):
    pages = {
        "Manager": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", 
                   "📢 Campaigns", "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "⚡ Quick Actions"],
        "Admin": ["📊 Dashboard", "👥 Customers", "📦 Inventory", "💰 Tax & Compliance", "📢 Campaigns",
                 "🤖 ML Models", "💎 Chit Management", "⚡ Quick Actions", "🤖 AI Assistant", "⚙️ Settings"],
        "Customer": ["💬 Support Chat", "📊 My Dashboard"]
    }
    return pages.get(role, [])

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("**Premium Management System for Indian Jewellery Retail**")
        st.divider()
        
        login_type = st.radio("Login As:", ["Manager", "Staff", "Admin", "Customer"], horizontal=True)
        
        if login_type == "Manager":
            st.subheader("👨‍💼 Manager Login")
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", key="mgr_user")
            with col2:
                password = st.text_input("Password", type="password", key="mgr_pass")
            
            if st.button("🔓 Login", use_container_width=True):
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
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", key="staff_user")
            with col2:
                password = st.text_input("Password", type="password", key="staff_pass")
            
            if st.button("🔓 Login", use_container_width=True):
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
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username", key="admin_user")
            with col2:
                password = st.text_input("Password", type="password", key="admin_pass")
            
            if st.button("🔓 Login", use_container_width=True):
                if username == "admin" and hashlib.sha256(password.encode()).hexdigest() == USERS["admin"]["password"]:
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Admin"
                    st.session_state.username = username
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        else:
            st.subheader("👤 Customer Login")
            col1, col2 = st.columns(2)
            with col1:
                username = st.text_input("Username (C001-C007)", key="cust_user")
            with col2:
                password = st.text_input("Password", type="password", key="cust_pass")
            
            if st.button("🔓 Login", use_container_width=True):
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
        st.info("""
        **Demo Credentials:**
        - Manager: `manager` / `manager123`
        - Staff: `staff` / `staff123`
        - Admin: `admin` / `admin123`
        - Customer: `C001-C007` / `customer123`
        """)

# ============================================================================
# INTELLIGENT SUPPORT CHAT
# ============================================================================

def get_smart_response(user_message, customer_id=None):
    message_lower = user_message.lower()
    
    if "pending" in message_lower or "outstanding" in message_lower or "dues" in message_lower:
        if customer_id and customer_id in CUSTOMER_DATABASE:
            pending = CUSTOMER_DATABASE[customer_id]["pending"]
            if pending == 0:
                return f"✅ Great news! You have no pending amounts. Your account is all clear!"
            else:
                return f"💰 Your pending amount is: **₹{pending:,}**\n\nPlease contact our office to settle it."
        return "💰 Please log in to check your pending amount."
    
    if "rate" in message_lower or "price" in message_lower or "gold" in message_lower or "silver" in message_lower:
        return f"""
**💎 Current Precious Metal Rates** *(Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')})*

**Gold Rates:**
- 22K: ₹{GOLD_RATES['22K']['price']}/gram ({GOLD_RATES['22K']['change']:+d})
- 24K: ₹{GOLD_RATES['24K']['price']}/gram ({GOLD_RATES['24K']['change']:+d})
- 18K: ₹{GOLD_RATES['18K']['price']}/gram ({GOLD_RATES['18K']['change']:+d})

**Silver Rate:**
- Silver: ₹{SILVER_RATE['price']}/gram ({SILVER_RATE['change']:+d})
        """
    
    if "product" in message_lower or "item" in message_lower or "available" in message_lower:
        products_list = "📦 **Available Products:**\n\n"
        for p in PRODUCTS:
            status = "✅ In Stock" if p['stock'] > 0 else "❌ Out of Stock"
            products_list += f"• **{p['name']}** - ₹{p['price']:,} | Stock: {p['stock']} ({status})\n"
        return products_list
    
    if "my account" in message_lower or "my details" in message_lower or "who am i" in message_lower:
        if customer_id and customer_id in CUSTOMER_DATABASE:
            c = CUSTOMER_DATABASE[customer_id]
            return f"""
👤 **Your Account Details:**
- Name: {c['name']}
- Tier: {c['tier']}
- Pending: ₹{c['pending']:,}
- Last Purchase: {c['last_purchase']}
            """
        return "Please log in to view your account details."
    
    if "hours" in message_lower or "timings" in message_lower or "open" in message_lower:
        return """
🕐 **Store Timings:**
- Monday - Saturday: 10:00 AM - 8:00 PM
- Sunday: 11:00 AM - 7:00 PM
- Closed on National Holidays
        """
    
    if "return" in message_lower or "exchange" in message_lower or "policy" in message_lower:
        return """
↩️ **Return & Exchange Policy:**
• 15 days return policy from purchase date
• Only unused, sealed items eligible
• Original receipt required
• Exchange available within 30 days
• Custom orders are non-refundable
        """
    
    if "payment" in message_lower or "card" in message_lower or "upi" in message_lower:
        return """
💳 **Payment Methods:**
• Cash
• Credit/Debit Cards
• UPI (Google Pay, PhonePe, Paytm)
• Bank Transfers
• EMI Options for purchases above ₹1,00,000
        """
    
    if "loyalty" in message_lower or "points" in message_lower or "reward" in message_lower:
        return """
🎁 **Loyalty Rewards Program:**
- Premium: 1 Point per ₹1 = 1% discount
- Gold: 1 Point per ₹2 = 0.5% discount
- Silver: 1 Point per ₹3 = 0.33% discount
- Standard: 1 Point per ₹5 = 0.2% discount
        """
    
    return "👋 I can help with: 💰 Pending amounts, 💎 Rates, 📦 Products, 🎁 Loyalty, 💳 Payments, 🕐 Hours, and policies!"

def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Customer Support Chat</h2>", unsafe_allow_html=True)
    
    customer_id = st.session_state.get('customer_id')
    customer_name = "Customer"
    
    if customer_id and customer_id in CUSTOMER_DATABASE:
        customer_name = CUSTOMER_DATABASE[customer_id]["name"]
    
    st.markdown(f"Welcome **{customer_name}**! 👋")
    st.markdown("Ask me anything about our products, rates, pending amounts, and policies.")
    
    if "support_chat" not in st.session_state:
        st.session_state.support_chat = []
    
    for message in st.session_state.support_chat:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    col1, col2 = st.columns([5, 1])
    with col1:
        user_input = st.text_input("Type your message...", key=f"sup_{len(st.session_state.support_chat)}")
    with col2:
        send_btn = st.button("Send", key=f"send_{len(st.session_state.support_chat)}")
    
    if send_btn and user_input:
        st.session_state.support_chat.append({"role": "user", "content": user_input})
        response = get_smart_response(user_input, customer_id)
        st.session_state.support_chat.append({"role": "assistant", "content": response})
        st.rerun()
    
    st.divider()
    st.write("**Quick Questions:**")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💰 My Pending", use_container_width=True, key="q1"):
            st.session_state.support_chat.append({"role": "user", "content": "Show my pending amount"})
            st.session_state.support_chat.append({"role": "assistant", "content": get_smart_response("pending", customer_id)})
            st.rerun()
    with col2:
        if st.button("💎 Today's Rates", use_container_width=True, key="q2"):
            st.session_state.support_chat.append({"role": "user", "content": "What are today's rates?"})
            st.session_state.support_chat.append({"role": "assistant", "content": get_smart_response("rates", customer_id)})
            st.rerun()
    with col3:
        if st.button("📦 Products", use_container_width=True, key="q3"):
            st.session_state.support_chat.append({"role": "user", "content": "Available products?"})
            st.session_state.support_chat.append({"role": "assistant", "content": get_smart_response("products", customer_id)})
            st.rerun()
    with col4:
        if st.button("🎁 Loyalty", use_container_width=True, key="q4"):
            st.session_state.support_chat.append({"role": "user", "content": "Loyalty program?"})
            st.session_state.support_chat.append({"role": "assistant", "content": get_smart_response("loyalty", customer_id)})
            st.rerun()

# ============================================================================
# DASHBOARD
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='success-card'>
        <div class='metric-label'>💰 Total Sales</div>
        <div class='metric-value'>₹45,00,000</div>
        <small style='color: #22863a;'>+₹5,00,000 this month</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='info-card'>
        <div class='metric-label'>👥 Customers</div>
        <div class='metric-value'>1,250</div>
        <small style='color: #0366d6;'>+45 new customers</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='warning-card'>
        <div class='metric-label'>📦 Stock Value</div>
        <div class='metric-value'>₹45,00,000</div>
        <small style='color: #d97706;'>-₹2,00,000</small>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='success-card'>
        <div class='metric-label'>💎 Active Chits</div>
        <div class='metric-value'>85</div>
        <small style='color: #22863a;'>+12 new chits</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sales Trend (Last 30 Days)")
        dates = pd.date_range(start='2025-11-11', end='2025-12-11', freq='D')
        sales_data = np.random.randint(50000, 200000, len(dates))
        fig = px.line(x=dates, y=sales_data, title="Daily Sales")
        fig.update_layout(template="plotly_light", hovermode="x unified", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Sales by Category")
        fig.update_layout(template="plotly_light", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top Selling Items")
        top_items = pd.DataFrame({
            'Item': ['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Gold Necklace'],
            'Sales': [450, 380, 320, 280],
            'Revenue': ['₹22,50,000', '₹38,00,000', '₹9,60,000', '₹28,00,000']
        })
        st.dataframe(top_items, use_container_width=True, hide_index=True)
    
    with col2:
        st.subheader("👥 Customer Tier Distribution")
        tiers = ['Premium', 'Gold', 'Silver', 'Standard']
        tier_counts = [250, 450, 350, 200]
        fig = px.bar(x=tiers, y=tier_counts, title="Customers by Tier", color=tier_counts)
        fig.update_layout(template="plotly_light", height=350)
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 All Customers", "⏳ Pending Customers", "➕ Add Customer", "🎁 Loyalty", "📊 Analytics"])
    
    with tab1:
        st.subheader("Customer Database")
        customers_df = pd.DataFrame({
            'ID': ['C001', 'C002', 'C003', 'C004', 'C005', 'C006', 'C007'],
            'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta', 'Deepika Sharma', 'Raj Singh'],
            'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard', 'Premium', 'Gold'],
            'Total Purchases': ['₹5,00,000', '₹3,50,000', '₹1,80,000', '₹2,20,000', '₹80,000', '₹6,50,000', '₹2,80,000'],
            'Pending': ['₹45,000', '₹0', '₹18,000', '₹22,000', '₹0', '₹65,000', '₹12,000'],
            'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25', '2025-12-11', '2025-12-10']
        })
        st.dataframe(customers_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("⏳ Customers with Pending Amounts")
        pending_df = pd.DataFrame({
            'ID': ['C001', 'C003', 'C004', 'C006', 'C007'],
            'Name': ['Rajesh Patel', 'Amit Kumar', 'Neha Sharma', 'Deepika Sharma', 'Raj Singh'],
            'Pending': ['₹45,000', '₹18,000', '₹22,000', '₹65,000', '₹12,000'],
            'Tier': ['Premium', 'Silver', 'Gold', 'Premium', 'Gold'],
            'Last Purchase': ['2025-12-10', '2025-12-05', '2025-12-08', '2025-12-11', '2025-12-10'],
            'Days Overdue': [3, 8, 5, 2, 3]
        })
        st.dataframe(pending_df, use_container_width=True, hide_index=True)
        
        st.markdown(f"**Total Pending Amount:** ₹{45000 + 18000 + 22000 + 65000 + 12000:,}")
    
    with tab3:
        st.subheader("Add New Customer")
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
        with col2:
            tier = st.selectbox("Customer Tier", ["Standard", "Silver", "Gold", "Premium"])
            address = st.text_area("Address")
        
        if st.button("✅ Add Customer", use_container_width=True):
            st.success(f"✅ Customer {name} added successfully!")
            st.balloons()
    
    with tab4:
        st.subheader("💝 Loyalty Program")
        loyalty_df = pd.DataFrame({
            'Tier': ['Premium', 'Gold', 'Silver', 'Standard'],
            'Points/₹': ['1 per ₹1', '1 per ₹2', '1 per ₹3', '1 per ₹5'],
            'Discount': ['1%', '0.5%', '0.33%', '0.2%'],
            'Redemption': ['100 pts = ₹100', '100 pts = ₹50', '100 pts = ₹33', '100 pts = ₹20']
        })
        st.dataframe(loyalty_df, use_container_width=True, hide_index=True)
    
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[250, 450, 350, 200], names=['Premium', 'Gold', 'Silver', 'Standard'])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'], y=[120, 145, 165, 140, 190, 210])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Stock Status", "🐌 Slow Stock", "➕ Add Item", "⚠️ Low Stock", "📈 Analytics"])
    
    with tab1:
        st.subheader("Current Inventory")
        inventory_df = pd.DataFrame({
            'SKU': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005', 'SLV006'],
            'Item Name': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace', 'Silver Earrings'],
            'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold', 'Silver'],
            'Quantity': [45, 120, 15, 8, 32, 50],
            'Unit Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000', '₹3,500'],
            'Total Value': ['₹6,75,000', '₹2,40,000', '₹7,50,000', '₹6,00,000', '₹7,04,000', '₹1,75,000'],
            'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low', '🔴 Critical', '✅ In Stock', '✅ In Stock']
        })
        st.dataframe(inventory_df, use_container_width=True, hide_index=True)
        st.markdown(f"**Total Inventory Value:** ₹29,44,000")
    
    with tab2:
        st.subheader("🐌 Slow Moving Stock (Not sold in 30+ days)")
        slow_stock = pd.DataFrame({
            'SKU': ['GLD005', 'SLV006'],
            'Item': ['Gold Necklace', 'Silver Earrings'],
            'Stock': [32, 50],
            'Days in Stock': [45, 38],
            'Value': ['₹7,04,000', '₹1,75,000'],
            'Recommendation': ['Consider promotion', 'Run flash sale']
        })
        st.dataframe(slow_stock, use_container_width=True, hide_index=True)
    
    with tab3:
        st.subheader("Add New Item")
        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item Name")
            category = st.selectbox("Category", ["Gold", "Silver", "Diamond", "Platinum", "Other"])
            quantity = st.number_input("Quantity", min_value=1)
        with col2:
            sku = st.text_input("SKU/Item Code")
            unit_price = st.number_input("Unit Price (₹)", min_value=100)
        
        if st.button("✅ Add Item", use_container_width=True):
            st.success(f"✅ Item added! Total Value: ₹{quantity * unit_price:,}")
    
    with tab4:
        st.subheader("⚠️ Low Stock Alerts")
        st.markdown("""
        <div class='danger-card'>
        <strong>🔴 Critical Items (Reorder Immediately):</strong>
        • Platinum Ring (SKU: PLT004) - Only 8 units
        <br><br>
        <strong>⚠️ Warning Items (Reorder Soon):</strong>
        • Diamond Pendant (SKU: DMD003) - Only 15 units
        </div>
        """, unsafe_allow_html=True)
        
        low_stock = pd.DataFrame({
            'Item': ['Platinum Ring', 'Diamond Pendant'],
            'Current Stock': [8, 15],
            'Reorder Level': [15, 20],
            'Shortage': [7, 5],
            'Status': ['🔴 Critical', '⚠️ Warning']
        })
        st.dataframe(low_stock, use_container_width=True, hide_index=True)
    
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=['Gold', 'Silver', 'Diamond', 'Platinum'], y=[77, 170, 15, 8])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(values=[13.79, 4.15, 7.5, 6.0], names=['Gold', 'Silver', 'Diamond', 'Platinum'])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAX & COMPLIANCE
# ============================================================================

def tax_compliance_page():
    st.markdown("<h2 class='main-title'>💰 Tax & Compliance</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tax Dashboard", "📄 GST Reports", "💳 Invoices", "📋 Checklist"])
    
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown("""
            <div class='info-card'>
            <div class='metric-label'>Monthly Sales</div>
            <div class='metric-value'>₹45,00,000</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='warning-card'>
            <div class='metric-label'>GST Collected (18%)</div>
            <div class='metric-value'>₹8,10,000</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='warning-card'>
            <div class='metric-label'>GST Payable</div>
            <div class='metric-value'>₹6,50,000</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div class='success-card'>
            <div class='metric-label'>Tax Rate</div>
            <div class='metric-value'>18%</div>
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
            'Status': ['✅ Paid', '✅ Paid', '⏳ Pending', '⏳ Pending']
        })
        st.dataframe(invoices, use_container_width=True, hide_index=True)
    
    with tab4:
        st.subheader("📋 Compliance Checklist")
        items = [
            ("✅", "GST Registration", "GSTIN: 27ABCXYZ123"),
            ("✅", "Monthly GST Filing", "Nov 2025 filed"),
            ("⚠️", "Audit", "Scheduled Jan 2026"),
            ("✅", "BIS Hallmark", "All items compliant"),
            ("✅", "Invoice Records", "5-year archive"),
            ("❌", "Labor License", "Renewal pending"),
            ("✅", "Employee PF/ESIC", "Compliant"),
            ("✅", "Bank Reconciliation", "Monthly done")
        ]
        for status, item, details in items:
            st.write(f"{status} **{item}:** {details}")

# ============================================================================
# CAMPAIGNS
# ============================================================================

def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Active", "➕ Create", "📈 Performance"])
    
    with tab1:
        campaigns = pd.DataFrame({
            'Campaign': ['Diwali Sale 2025', 'Wedding Season', 'New Year Discount', 'Clearance Sale'],
            'Type': ['Seasonal', 'Festival', 'Seasonal', 'Clearance'],
            'Discount': ['20%', '15%', '10%', '30%'],
            'Start': ['2025-10-15', '2025-11-01', '2025-12-20', '2025-12-01'],
            'End': ['2025-11-15', '2025-12-31', '2026-01-31', '2025-12-31'],
            'Budget': ['₹2,00,000', '₹1,50,000', '₹1,00,000', '₹50,000'],
            'Status': ['✅ Active', '✅ Active', '📅 Scheduled', '✅ Active']
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
        
        st.write("**Select Channels:**")
        col1, col2, col3 = st.columns(3)
        with col1:
            use_sms = st.checkbox("📱 SMS")
        with col2:
            use_whatsapp = st.checkbox("💬 WhatsApp")
        with col3:
            use_email = st.checkbox("📧 Email")
        
        if st.button("✅ Create Campaign", use_container_width=True):
            channels = ", ".join(filter(None, ["SMS" if use_sms else "", "WhatsApp" if use_whatsapp else "", "Email" if use_email else ""]))
            st.success(f"✅ Campaign created! Channels: {channels}")
            st.balloons()
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(x=['Diwali', 'Wedding', 'New Year', 'Clearance'], y=[45000, 32000, 18000, 25000])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(x=['W1', 'W2', 'W3', 'W4'], y=[10000, 15000, 12000, 8000], markers=True)
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# QUICK ACTIONS
# ============================================================================

def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)
    
    st.subheader("📊 Select Quick Action (Business Challenge)")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📈 Send Payment Reminder", use_container_width=True, key="qact1"):
            st.info("Found 60 customers with pending amounts\nWill send SMS to 58 customers")
    with col2:
        if st.button("📦 Send Festival Offer", use_container_width=True, key="qact2"):
            st.info("Festival Offer\nWill boost sales during peak")
    with col3:
        if st.button("📢 Send Festival Offer", use_container_width=True, key="qact3"):
            st.info("View Campaign Status\nCheck insights")
    
    st.divider()
    st.subheader("💬 Message Template")
    st.write("**Hi [Name],**")
    st.write("We have an exciting offer for you.")
    st.write("Come visit us today!")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Save Message Template", use_container_width=True):
            st.success("✅ Template saved!")
    with col2:
        if st.button("📤 Send Messages", use_container_width=True):
            st.success("✅ Messages sent to 58 customers!")

# ============================================================================
# ML MODELS - ENHANCED
# ============================================================================

def ml_models_page():
    st.markdown("<h2 class='main-title'>🤖 ML Models & AI Predictions</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["💎 Charm Prediction", "📈 Demand Forecast", "💰 Dynamic Pricing", "👥 Segmentation"])
    
    with tab1:
        st.subheader("💎 Charm Prediction - Jewelry Appeal Analysis")
        st.info("🔮 AI predicts which jewelry items will be most popular based on seasonal trends, customer preferences, and market analysis")
        
        charm_pred = pd.DataFrame({
            'Item': ['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Platinum Ring', 'Gold Necklace'],
            'Charm Score': [92, 88, 76, 84, 79],
            'Popularity': ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐⭐'],
            'Recommendation': ['High Demand', 'High Demand', 'Moderate', 'Increase Stock', 'Maintain'],
            'Trend': ['↑ Rising', '↑ Rising', '→ Stable', '↑ Rising', '↓ Declining']
        })
        st.dataframe(charm_pred, use_container_width=True, hide_index=True)
        
        fig = px.bar(x=['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Platinum Ring', 'Gold Necklace'],
                    y=[92, 88, 76, 84, 79], title="Charm Popularity Score", color=[92, 88, 76, 84, 79])
        fig.update_layout(template="plotly_light", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("📈 Demand Forecasting - AI Predictions")
        st.info("📊 AI-powered demand prediction for next 30 days based on historical data and trends")
        
        demand_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current Stock': [45, 120, 15, 8],
            'Predicted Demand (30d)': [48, 135, 18, 10],
            'Confidence': ['92%', '88%', '85%', '87%'],
            'Action': ['Maintain', 'Increase Stock', 'Reorder', 'Critical Reorder']
        })
        st.dataframe(demand_data, use_container_width=True, hide_index=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig = px.bar(x=['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
                        y=[45, 120, 15, 8], title="Current Stock Levels")
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(x=['Day 5', 'Day 10', 'Day 15', 'Day 20', 'Day 25', 'Day 30'],
                         y=[150, 165, 180, 175, 190, 210], title="Demand Forecast (30 Days)", markers=True)
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("💰 Dynamic Pricing - AI Optimization")
        st.info("💡 AI recommends optimal prices based on demand, competition, inventory levels, and customer segments")
        
        pricing_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000'],
            'AI Recommended': ['₹15,500', '₹1,950', '₹52,000', '₹77,500'],
            'Revenue Impact': ['+8.5%', '-2.3%', '+4.2%', '+3.5%'],
            'Action': ['✅ Increase', '❌ Decrease', '✅ Increase', '✅ Increase']
        })
        st.dataframe(pricing_data, use_container_width=True, hide_index=True)
        
        fig = px.scatter(x=['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
                        y=[8.5, -2.3, 4.2, 3.5], title="Revenue Impact (%)")
        fig.update_layout(template="plotly_light", height=350)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("👥 Customer Segmentation - AI Analysis")
        st.info("🎯 AI groups customers for targeted marketing based on purchase behavior and value")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[250, 450, 350, 200],
                        names=['VIP (₹5L+)', 'Premium (₹2-5L)', 'Regular (₹50K-2L)', 'New (<₹50K)'],
                        title="Customer Segments by Value")
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['VIP', 'Premium', 'Regular', 'New'],
                        y=[1800, 1200, 600, 150],
                        title="Average Days Between Purchases")
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# AI ASSISTANT - ENHANCED LIKE SCREENSHOT
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Business Assistant</h2>", unsafe_allow_html=True)
    
    st.subheader("💬 Ask me anything about optimizing your jewellery business")
    st.divider()
    
    # Challenge Selector
    st.write("**What's your business challenge?**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.checkbox("📈 Slow Moving Inventory", value=True, key="ch1")
        st.checkbox("👥 Customer Retention", key="ch2")
    
    with col2:
        st.checkbox("💎 Pricing Strategy", key="ch3")
        st.checkbox("📊 Sales Improvement", key="ch4")
    
    with col3:
        st.checkbox("🎁 Custom Orders", key="ch5")
    
    st.divider()
    
    # Your Situation
    st.write("**Your Situation:**")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("- Product: Diamond Necklace - 18K")
        st.markdown("- In stock for: 93 days")
        st.markdown("- Current price: ₹50,000")
        st.markdown("- Cost: ₹35,000")
    
    with col2:
        st.markdown("- Monthly sales: 0 units")
        st.markdown("- Margin: ₹15,000")
        st.markdown("- Storage cost/month: ₹500")
        st.markdown("- Total loss: ₹46,500")
    
    st.divider()
    
    # AI Assistant Chat
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    st.write("**AI Assistant Recommendation:**")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask about stock, sales, customers, chits, pricing..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Enhanced AI Responses
        ai_responses = {
            "stock": """📦 **Current Stock Optimization:**
- Total inventory value: ₹29,44,000
- Fast-moving items: 3 products (Gold Ring, Diamond Pendant, Silver Bracelet)
- Slow-moving items: 2 products (Gold Necklace, Silver Earrings)
- Low stock alert: 2 items (Platinum Ring - critical, Diamond Pendant - warning)

**Recommendation:**
✅ Increase reorders for fast-moving Gold Ring (92% charm score)
⚠️ Run promotional campaign for slow stock items
🔄 Implement dynamic pricing for items in stock >30 days
""",
            "sales": """💰 **Sales Performance Analysis:**
- Total Sales (30-day): ₹45,00,000
- Daily Average: ₹1,50,000
- Top Product: Gold Ring (₹22,50,000 revenue)
- Best Time: Weekends & Festivals

**Key Metrics:**
- Avg Transaction Value: ₹3,600
- Monthly Growth: +12% MoM
- Customer Repeat Rate: 68%

**AI Insights:**
🎯 Peak hours: 3 PM - 7 PM (focus staff here)
📈 Best days: Thursday-Sunday (plan inventory)
🎁 Bundle opportunity: Ring + Bracelet combo
""",
            "customer": """👥 **Customer Intelligence Report:**
- Total Customers: 1,250 active
- Pending Collections: ₹1,62,000 (5 customers)
- Premium Tier: 250 customers (avg ₹20,000 value)
- Gold Tier: 450 customers (avg ₹7,800 value)

**Segmentation Analysis:**
- VIP: 25 customers | Avg purchase: ₹50,000
- Premium: 225 customers | Avg purchase: ₹20,000
- Regular: 600 customers | Avg purchase: ₹5,000
- New: 400 customers | Avg purchase: ₹2,000

**Retention Strategy:**
✅ 85% retention rate (excellent)
🎁 Loyalty points are working well
💬 Personalized offers increase repeat rate by 35%
""",
            "chit": """💎 **Chit Fund Performance:**
- Active Chits: 85
- Total Value: ₹65,00,000
- Active Members: 127
- Monthly Collection: ₹9,50,000
- Default Rate: 0.5% (excellent)

**Top Performing Chits:**
1. Diamond Savings - 20 members - ₹2,00,000 value
2. Platinum Plus - 10 members - ₹3,00,000 value
3. Gold 12-Month - 12 members - ₹1,00,000 value

**Revenue Contribution:** 15% of total business
""",
            "price": """💰 **Dynamic Pricing Intelligence:**
- Current strategy: Fixed pricing
- Market opportunity: +8-12% revenue with dynamic pricing
- Competition analysis: Prices 5-8% lower

**AI Recommended Adjustments:**
✅ Gold Ring: ₹15,000 → ₹15,500 (+3.3%)
✅ Diamond Pendant: ₹50,000 → ₹52,000 (+4%)
✅ Platinum Ring: ₹75,000 → ₹77,500 (+3.3%)
❌ Silver Bracelet: ₹2,000 → ₹1,950 (-2.5% to increase volume)

**Impact:** +₹1,85,000 annual revenue
"""
        }
        
        response = "👋 I'm here to help! Ask about: Stock, Sales, Customers, Chits, Pricing, or Trends!"
        for keyword, ans in ai_responses.items():
            if keyword in prompt.lower():
                response = ans
                break
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(response)

# ============================================================================
# CHIT MANAGEMENT
# ============================================================================

def chit_management_page():
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
            'Status': ['✅ Active', '✅ Active', '✅ Active', '⏳ Closing']
        })
        st.dataframe(chits, use_container_width=True, hide_index=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            chit_name = st.text_input("Chit Name")
            chit_value = st.number_input("Chit Value (₹)", min_value=10000)
            num_members = st.number_input("Members", min_value=1, max_value=100)
        
        with col2:
            duration = st.selectbox("Duration", ["3 Months", "6 Months", "12 Months", "24 Months"])
            chit_type = st.selectbox("Type", ["Regular", "Premium", "Diamond", "Platinum"])
            start_date = st.date_input("Start Date")
        
        if st.button("✅ Create Chit", use_container_width=True):
            st.success("✅ Chit created successfully!")
            st.balloons()
    
    with tab3:
        payments = pd.DataFrame({
            'Chit ID': ['CHT001', 'CHT001', 'CHT002', 'CHT003'],
            'Member': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Vikram Gupta'],
            'Month': ['Dec 2025', 'Dec 2025', 'Dec 2025', 'Dec 2025'],
            'Amount': ['₹8,500', '₹8,500', '₹8,500', '₹10,000'],
            'Status': ['✅ Paid', '⏳ Pending', '✅ Paid', '✅ Paid']
        })
        st.dataframe(payments, use_container_width=True, hide_index=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(values=[12, 6, 20, 10], names=['Gold 12M', 'Silver 6M', 'Diamond', 'Platinum'])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(x=['CHT001', 'CHT002', 'CHT003', 'CHT004'], y=[100, 50, 200, 300])
            fig.update_layout(template="plotly_light", height=350)
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# SETTINGS
# ============================================================================

def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["👥 Users", "🏪 Store"])
    
    with tab1:
        users = pd.DataFrame({
            'Username': ['manager', 'staff', 'admin'],
            'Role': ['Manager', 'Sales Staff', 'Admin'],
            'Status': ['✅ Active', '✅ Active', '✅ Active'],
            'Last Login': ['2025-12-11', '2025-12-11', '2025-12-11']
        })
        st.dataframe(users, use_container_width=True, hide_index=True)
    
    with tab2:
        st.subheader("Store Information")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Store Name", "Jewellery Shop Premium")
            st.text_input("Owner", "Rajesh Patel")
            st.text_input("Email", "shop@jewellery.com")
        with col2:
            st.text_input("Phone", "+91-9876543210")
            st.text_input("GSTIN", "27ABCXYZ123")
        
        if st.button("💾 Save Settings", use_container_width=True):
            st.success("✅ Settings saved!")

# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================

def customer_dashboard():
    st.markdown("<h2 class='main-title'>📊 My Dashboard</h2>", unsafe_allow_html=True)
    
    customer_id = st.session_state.get('customer_id')
    if customer_id and customer_id in CUSTOMER_DATABASE:
        c = CUSTOMER_DATABASE[customer_id]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='info-card'>
            <div class='metric-label'>👤 Name</div>
            <div class='metric-value' style='font-size: 1.2rem;'>{c['name']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class='success-card'>
            <div class='metric-label'>⭐ Tier</div>
            <div class='metric-value' style='font-size: 1.2rem;'>{c['tier']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            pending_color = "success" if c['pending'] == 0 else "warning"
            st.markdown(f"""
            <div class='{pending_color}-card'>
            <div class='metric-label'>💰 Pending</div>
            <div class='metric-value' style='font-size: 1.2rem;'>₹{c['pending']:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class='info-card'>
            <div class='metric-label'>📅 Last Purchase</div>
            <div class='metric-value' style='font-size: 1.2rem;'>{c['last_purchase']}</div>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# MAIN
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>👋 {st.session_state.username.title()}</h3>", unsafe_allow_html=True)
            st.markdown(f"**{st.session_state.user_role}**")
            st.divider()
            
            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.rerun()
        
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
        elif selected_page == "🤖 ML Models":
            ml_models_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
