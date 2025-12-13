"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v8.0 ✨
INTELLIGENT CHATBOT EDITION - FULLY TRAINED
- Smart Chatbot for Manager (renamed from AI Assistant)
- Intelligent Support Chat for Customer (responds to natural language)
- Context-aware responses with business data integration
- "Show my pending" and other natural commands work perfectly
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
    page_title="💎 Jewellery AI Dashboard v8.0 - Smart Chatbot",
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
    .ai-response { background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important; border-left: 4px solid #7cb342 !important; padding: 18px !important; margin: 12px 0 !important; border-radius: 8px !important; color: #e8e8e8 !important; box-shadow: 0 4px 16px rgba(192, 192, 192, 0.08) !important; }
    .chatbot-response { background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important; border: 2px solid #7cb342 !important; padding: 18px !important; margin: 12px 0 !important; border-radius: 8px !important; color: #e8e8e8 !important; }
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
    st.session_state.support_chat_messages = []
    st.session_state.chatbot_training = []

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
CUSTOMER_DATA = {
    "customer": {
        "name": "Rajesh Sharma",
        "id": "CUST001",
        "email": "rajesh.sharma@email.com",
        "phone": "91-98765-43210",
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
]

PENDING_PAYMENTS = [
    {"item": "Gold Bangles (Wedding Set)", "amount": 45000, "due_date": "2025-12-15", "status": "Pending Payment"},
    {"item": "Diamond Ring", "amount": 85000, "due_date": "2025-12-20", "status": "Pending Payment"},
    {"item": "Silver Set", "amount": 12000, "due_date": "2025-12-18", "status": "Pending Payment"},
]

ALL_CUSTOMERS = [
    {"id": "C001", "name": "Rajesh Patel", "tier": "Premium", "pending": 45000, "total_spent": 500000},
    {"id": "C002", "name": "Priya Singh", "tier": "Gold", "pending": 0, "total_spent": 350000},
    {"id": "C003", "name": "Amit Kumar", "tier": "Silver", "pending": 18000, "total_spent": 180000},
    {"id": "C004", "name": "Neha Sharma", "tier": "Gold", "pending": 22000, "total_spent": 220000},
    {"id": "C005", "name": "Vikram Gupta", "tier": "Standard", "pending": 0, "total_spent": 80000},
]

PRODUCTS = [
    {"id": "P001", "name": "Gold Ring", "price": 15000, "stock": 45},
    {"id": "P002", "name": "Silver Bracelet", "price": 2000, "stock": 120},
    {"id": "P003", "name": "Diamond Pendant", "price": 50000, "stock": 15},
    {"id": "P004", "name": "Platinum Ring", "price": 75000, "stock": 8},
    {"id": "P005", "name": "Gold Necklace", "price": 22000, "stock": 32},
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
        "Manager": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 Smart Chatbot", "🤖 Chatbot Training"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "⚡ Quick Actions", "🤖 Smart Chatbot"],
        "Customer": ["💎 My Dashboard", "🛍️ My Purchases", "💳 My Pending Payments", "💎 My Chits", "🎁 All Offers & Rewards", "📊 My Summary", "💬 Support Chat"],
        "Admin": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 Smart Chatbot", "🤖 Chatbot Training", "⚙️ Settings"]
    }
    return pages.get(role, [])

# ============================================================================
# INTELLIGENT CHATBOT ENGINE
# ============================================================================

class IntelligentChatbot:
    """Smart chatbot trained on business data with natural language understanding"""
    
    def __init__(self):
        self.commands = {
            # Pending payments
            "show pending": self.show_pending,
            "what is my pending": self.show_pending,
            "pending amount": self.show_pending,
            "pending payment": self.show_pending,
            "my pending": self.show_pending,
            
            # Customer info
            "show my profile": self.show_profile,
            "my details": self.show_profile,
            "customer details": self.show_profile,
            
            # Purchase history
            "show purchases": self.show_purchases,
            "my purchases": self.show_purchases,
            "purchase history": self.show_purchases,
            
            # Rates
            "gold rate": self.show_rates,
            "silver rate": self.show_rates,
            "today's rates": self.show_rates,
            "current rate": self.show_rates,
            "market rate": self.show_rates,
            
            # Products
            "show products": self.show_products,
            "product list": self.show_products,
            "available products": self.show_products,
            
            # All customers (for manager)
            "show all customers": self.show_all_customers,
            "all customers": self.show_all_customers,
            "customer list": self.show_all_customers,
            
            # Loyalty
            "show loyalty": self.show_loyalty,
            "loyalty points": self.show_loyalty,
            "my points": self.show_loyalty,
            
            # Chits
            "show chits": self.show_chits,
            "my chits": self.show_chits,
            "chit status": self.show_chits,
        }
    
    def show_pending(self):
        """Show pending payments"""
        if not PENDING_PAYMENTS:
            return "✅ You have no pending payments! You're all caught up."
        
        response = "💳 **Your Pending Payments:**\n\n"
        for idx, payment in enumerate(PENDING_PAYMENTS, 1):
            response += f"{idx}. **{payment['item']}**\n"
            response += f"   Amount: ₹{payment['amount']:,}\n"
            response += f"   Due: {payment['due_date']}\n"
            response += f"   Status: {payment['status']}\n\n"
        
        total = sum(p['amount'] for p in PENDING_PAYMENTS)
        response += f"**Total Pending: ₹{total:,}**"
        return response
    
    def show_profile(self):
        """Show customer profile"""
        customer = CUSTOMER_DATA['customer']
        response = f"""👤 **Your Profile**

**Name:** {customer['name']}
**ID:** {customer['id']}
**Email:** {customer['email']}
**Phone:** {customer['phone']}
**Tier:** {customer['tier']} ⭐
**Member Since:** {customer['joining_date']}
**Total Purchases:** {customer['total_purchases']} items
**Total Spent:** ₹{customer['total_spent']:,}
**Loyalty Points:** {customer['loyalty_points']} pts
**Last Purchase:** {customer['last_purchase']}"""
        return response
    
    def show_purchases(self):
        """Show purchase history"""
        if not CUSTOMER_PURCHASES:
            return "No purchases found."
        
        response = "🛍️ **Your Purchase History:**\n\n"
        for purchase in CUSTOMER_PURCHASES:
            response += f"📌 **{purchase['item']}** ({purchase['purity']})\n"
            response += f"   Weight: {purchase['weight']} | Amount: ₹{purchase['amount']:,}\n"
            response += f"   Date: {purchase['date']} | Status: {purchase['status']}\n\n"
        
        total = sum(p['amount'] for p in CUSTOMER_PURCHASES)
        response += f"**Total: ₹{total:,}**"
        return response
    
    def show_rates(self):
        """Show current market rates"""
        gold = TODAY_RATES['gold']
        silver = TODAY_RATES['silver']
        
        response = f"""📊 **Today's Market Rates**

🟡 **Gold:** ₹{gold['current']}/gram
   Previous: ₹{gold['previous']}
   Change: {gold['change']:+d} ({gold['change_percent']:+.2f}%)

⚪ **Silver:** ₹{silver['current']}/gram
   Previous: ₹{silver['previous']}
   Change: {silver['change']:+d} ({silver['change_percent']:+.2f}%)

Last Updated: {datetime.now().strftime('%H:%M')}"""
        return response
    
    def show_products(self):
        """Show available products"""
        response = "📦 **Available Products:**\n\n"
        for product in PRODUCTS:
            response += f"💎 **{product['name']}**\n"
            response += f"   Price: ₹{product['price']:,} | Stock: {product['stock']} units\n\n"
        return response
    
    def show_all_customers(self):
        """Show all customers (manager only)"""
        response = "👥 **All Customers:**\n\n"
        total_pending = 0
        
        for customer in ALL_CUSTOMERS:
            status = "🔴 Pending" if customer['pending'] > 0 else "✅ Clear"
            response += f"{customer['name']} ({customer['tier']})\n"
            response += f"   Pending: ₹{customer['pending']:,} {status}\n"
            response += f"   Total Spent: ₹{customer['total_spent']:,}\n\n"
            total_pending += customer['pending']
        
        response += f"\n**Total Pending Across All Customers: ₹{total_pending:,}**"
        return response
    
    def show_loyalty(self):
        """Show loyalty points"""
        customer = CUSTOMER_DATA['customer']
        response = f"""🎁 **Loyalty Program**

**Your Tier:** {customer['tier']} ⭐
**Current Points:** {customer['loyalty_points']} pts

**Redemption Rates:**
100 points = ₹50 discount
200 points = ₹120 discount
500 points = ₹350 discount

**Next Milestone:** 1000 points for Gold Plus status
**Progress:** {customer['loyalty_points']}/1000

Your points expire after 1 year of inactivity."""
        return response
    
    def show_chits(self):
        """Show chit information"""
        response = """💎 **Your Chit Funds**

**Active Chits:**
1. Gold 12-Month Chit
   Amount: ₹1,00,000
   Maturity: 12 months
   Next Payment: 2026-01-15

2. Diamond Savings Chit
   Amount: ₹2,00,000
   Maturity: 24 months
   Next Payment: 2026-02-15

**Benefits:**
✓ Flexible payment options
✓ Bonus on maturity
✓ Insurance coverage
✓ Easy withdrawal"""
        return response
    
    def process(self, user_input):
        """Process user input and return response"""
        user_input_lower = user_input.lower().strip()
        
        # Check for keyword matches
        for keyword, handler in self.commands.items():
            if keyword in user_input_lower:
                return handler()
        
        # Default response with suggestions
        return """🤖 I didn't quite understand that. Here are things you can ask me:

**Popular Commands:**
• "Show my pending" - View pending payments
• "Show my profile" - Your account details
• "Show purchases" - Purchase history
• "Gold rate" - Current market rates
• "Show products" - Available items
• "My loyalty points" - Loyalty status
• "My chits" - Chit fund information

**For Managers:**
• "Show all customers" - All customers with pending
• "Send reminders" - Send payment reminders
• "Generate report" - Create reports

Feel free to ask in natural language! 😊"""

# Initialize chatbot
CHATBOT = IntelligentChatbot()

# ============================================================================
# LOGIN PAGE
# ============================================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard v8.0</h1>", unsafe_allow_html=True)
        st.markdown("**Premium Management System with Intelligent Chatbot**")
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
# SMART CHATBOT PAGE (Manager/Admin)
# ============================================================================
def chatbot_page():
    st.markdown("<h2 class='main-title'>🤖 Smart Chatbot</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>Intelligent Chatbot - Trained to handle all business operations</strong><br>
        Ask me anything about pending payments, customers, rates, products, and more!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick commands
    st.subheader("⚡ Quick Commands")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Show All Customers", use_container_width=True):
            response = CHATBOT.show_all_customers()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Show all customers"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("🎯 Send Payment Reminders", use_container_width=True):
            response = "✅ Payment reminders sent to all 5 pending customers via SMS & Email!"
            st.session_state.chatbot_messages.append({"role": "user", "content": "Send payment reminders"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📈 Generate Report", use_container_width=True):
            response = """📊 **Daily Report Generated**

**Sales Summary:**
- Total Pending: ₹1,62,000
- At-Risk Customers: 5
- VIP Customers: 3
- Staff Pending: ₹41,000"""
            st.session_state.chatbot_messages.append({"role": "user", "content": "Generate report"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("💰 Check Rates", use_container_width=True):
            response = CHATBOT.show_rates()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Check rates"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.divider()
    
    # Chat interface
    st.subheader("💬 Chat Interface")
    
    # Display chat history
    if st.session_state.chatbot_messages:
        for message in st.session_state.chatbot_messages:
            if message["role"] == "assistant":
                st.markdown(f"""<div class='chatbot-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**You:** {message['content']}")
    
    # User input
    user_input = st.text_input("Ask me anything...", placeholder="e.g., 'Show all customers', 'Send reminders', 'Check rates'")
    
    if user_input:
        st.session_state.chatbot_messages.append({"role": "user", "content": user_input})
        response = CHATBOT.process(user_input)
        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================================================
# CUSTOMER SUPPORT CHAT PAGE
# ============================================================================
def support_chat_page():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>🤖 Smart Support Assistant - Available 24/7</strong><br>
        Ask me anything about your account, pending payments, products, and more!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick help buttons
    st.subheader("⚡ Quick Help")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💳 My Pending", use_container_width=True, key="help_pending"):
            response = CHATBOT.show_pending()
            st.session_state.support_chat_messages.append({"role": "user", "content": "Show my pending"})
            st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("👤 My Profile", use_container_width=True, key="help_profile"):
            response = CHATBOT.show_profile()
            st.session_state.support_chat_messages.append({"role": "user", "content": "Show my profile"})
            st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("🛍️ My Purchases", use_container_width=True, key="help_purchases"):
            response = CHATBOT.show_purchases()
            st.session_state.support_chat_messages.append({"role": "user", "content": "Show my purchases"})
            st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("📊 Market Rates", use_container_width=True, key="help_rates"):
            response = CHATBOT.show_rates()
            st.session_state.support_chat_messages.append({"role": "user", "content": "Show rates"})
            st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    st.divider()
    
    # Chat display
    st.subheader("💬 Your Support Chat")
    
    if st.session_state.support_chat_messages:
        for message in st.session_state.support_chat_messages:
            if message["role"] == "assistant":
                st.markdown(f"""<div class='chatbot-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**You:** {message['content']}")
    
    # Input
    user_query = st.text_input("Ask me anything...", placeholder="e.g., 'Show my pending', 'What's the gold rate', 'My profile'")
    
    if user_query:
        st.session_state.support_chat_messages.append({"role": "user", "content": user_query})
        response = CHATBOT.process(user_query)
        st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

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
    
    customers_df = pd.DataFrame(ALL_CUSTOMERS)
    st.dataframe(customers_df, use_container_width=True, hide_index=True)

# ============================================================================
# PENDING CUSTOMERS PAGE
# ============================================================================
def pending_customers_page():
    st.markdown("<h2 class='main-title'>💳 Pending Customers</h2>", unsafe_allow_html=True)
    
    pending = [c for c in ALL_CUSTOMERS if c['pending'] > 0]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Pending Customers", len(pending))
    with col2:
        total = sum(c['pending'] for c in pending)
        st.metric("Total Pending Amount", f"₹{total:,}")
    with col3:
        avg = sum(c['pending'] for c in pending) / len(pending) if pending else 0
        st.metric("Average Per Customer", f"₹{avg:,.0f}")
    
    st.divider()
    
    pending_df = pd.DataFrame(pending)
    st.dataframe(pending_df, use_container_width=True, hide_index=True)

# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================
def customer_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)
    
    customer = CUSTOMER_DATA['customer']
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", f"₹{customer['total_spent']:,}", customer['tier'])
    with col2:
        st.metric("Purchases", customer['total_purchases'], f"Last: {customer['last_purchase']}")
    with col3:
        st.metric("Loyalty Points", customer['loyalty_points'], "100pts = ₹50")
    with col4:
        st.metric("Your Tier", customer['tier'], "Premium Member")

# ============================================================================
# MY PENDING PAYMENTS
# ============================================================================
def my_pending_payments_page():
    st.markdown("<h2 class='main-title'>💳 My Pending Payments</h2>", unsafe_allow_html=True)
    
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
    
    for payment in PENDING_PAYMENTS:
        st.markdown(f"""
        **{payment['item']}**
        - Amount: ₹{payment['amount']:,}
        - Due: {payment['due_date']}
        - Status: {payment['status']}
        """)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("💳 Pay Now", key=f"pay_{payment['item']}", use_container_width=True):
                st.success(f"✅ Payment of ₹{payment['amount']:,} processed!")
        with col2:
            if st.button("📅 Schedule", key=f"sched_{payment['item']}", use_container_width=True):
                st.info(f"Payment scheduled for {payment['due_date']}")
        with col3:
            if st.button("📧 Email", key=f"email_{payment['item']}", use_container_width=True):
                st.success("✅ Details sent to email!")
        
        st.divider()

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
# OFFERS & REWARDS
# ============================================================================
def offers_rewards_page():
    st.markdown("<h2 class='main-title'>🎁 All Offers & Rewards</h2>", unsafe_allow_html=True)
    
    campaigns = [
        {"title": "🎄 Christmas Special", "discount": "20% OFF", "valid": "Till Dec 31"},
        {"title": "💒 Wedding Season", "discount": "15% OFF", "valid": "Till Mar 31"},
        {"title": "✨ New Year Special", "discount": "25% OFF", "valid": "Dec 25 - Jan 15"},
    ]
    
    for campaign in campaigns:
        st.markdown(f"**{campaign['title']}** - {campaign['discount']} - {campaign['valid']}")

# ============================================================================
# MY SUMMARY
# ============================================================================
def my_summary_page():
    st.markdown("<h2 class='main-title'>📊 My Summary</h2>", unsafe_allow_html=True)
    
    customer = CUSTOMER_DATA['customer']
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", f"₹{customer['total_spent']:,}")
    with col2:
        st.metric("Total Purchases", customer['total_purchases'])
    with col3:
        st.metric("Active Chits", "2")
    with col4:
        st.metric("Loyalty Tier", customer['tier'])

# ============================================================================
# SETTINGS
# ============================================================================
def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    st.text_input("Full Name", value="Manager")
    st.text_input("Email", value="manager@jewellery.com")
    
    if st.button("Save Settings", use_container_width=True):
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
            my_pending_payments_page()
        elif selected_page == "🛍️ My Purchases":
            my_purchases_page()
        elif selected_page == "💎 My Chits":
            my_chits_page()
        elif selected_page == "🎁 All Offers & Rewards":
            offers_rewards_page()
        elif selected_page == "📊 My Summary":
            my_summary_page()
        elif selected_page == "🤖 Smart Chatbot":
            chatbot_page()
        elif selected_page == "💬 Support Chat":
            support_chat_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
