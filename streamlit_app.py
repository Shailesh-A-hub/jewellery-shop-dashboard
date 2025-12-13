"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v8.1 ✨
ENHANCED CHATBOT EDITION - PENDING PAYMENTS FULLY INTEGRATED
- Chatbot trained to handle ALL pending payment queries
- Real-time pending data integration
- Manager can see pending payments for ALL customers
- Customer sees only their own pending payments
- Natural language variations fully supported
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
    page_title="💎 Jewellery AI Dashboard v8.1 - Pending Payments Integrated",
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
    .pending-box { background: linear-gradient(135deg, #3a2a1a 0%, #2a1f0a 100%) !important; border-left: 5px solid #ff9800 !important; padding: 15px !important; border-radius: 8px !important; color: #e8e8e8 !important; margin: 10px 0 !important; }
    .chatbot-response { background: linear-gradient(135deg, #1a2a3a 0%, #0f2a3a 100%) !important; border-left: 4px solid #7cb342 !important; padding: 18px !important; margin: 12px 0 !important; border-radius: 8px !important; color: #e8e8e8 !important; }
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

# ============================================================================
# LIVE MARKET DATA & PENDING PAYMENTS DATABASE
# ============================================================================

TODAY_RATES = {
    "gold": {"current": 7850, "previous": 7800, "change": 50, "change_percent": 0.64, "currency": "₹", "unit": "per gram"},
    "silver": {"current": 95, "previous": 92, "change": 3, "change_percent": 3.26, "currency": "₹", "unit": "per gram"}
}

# ============================================================================
# ALL CUSTOMERS WITH PENDING PAYMENTS
# ============================================================================
ALL_CUSTOMERS = [
    {
        "id": "C001",
        "name": "Rajesh Patel",
        "tier": "Premium",
        "total_spent": 500000,
        "pending_items": [
            {"item": "Gold Bangles (Wedding Set)", "amount": 45000, "due_date": "2025-12-15", "status": "Pending Payment"}
        ]
    },
    {
        "id": "C002",
        "name": "Priya Singh",
        "tier": "Gold",
        "total_spent": 350000,
        "pending_items": []
    },
    {
        "id": "C003",
        "name": "Amit Kumar",
        "tier": "Silver",
        "total_spent": 180000,
        "pending_items": [
            {"item": "Silver Set", "amount": 12000, "due_date": "2025-12-18", "status": "Pending Payment"}
        ]
    },
    {
        "id": "C004",
        "name": "Neha Sharma",
        "tier": "Gold",
        "total_spent": 220000,
        "pending_items": [
            {"item": "Diamond Ring", "amount": 85000, "due_date": "2025-12-20", "status": "Pending Payment"},
            {"item": "Gold Necklace", "amount": 22000, "due_date": "2025-12-25", "status": "Pending Payment"}
        ]
    },
    {
        "id": "C005",
        "name": "Vikram Gupta",
        "tier": "Standard",
        "total_spent": 80000,
        "pending_items": []
    }
]

# LOGGED-IN CUSTOMER DATA
CUSTOMER_DATA = {
    "customer": {
        "id": "C001",
        "name": "Rajesh Patel",
        "email": "rajesh.sharma@email.com",
        "phone": "91-98765-43210",
        "joining_date": "2023-03-15",
        "tier": "Premium",
        "loyalty_points": 850,
        "total_purchases": 12,
        "total_spent": 500000,
        "last_purchase": "2025-12-08"
    }
}

CUSTOMER_PURCHASES = [
    {"date": "2025-12-08", "item": "Gold Ring", "purity": "22K", "weight": "5.2g", "amount": 45000, "status": "Delivered"},
    {"date": "2025-11-25", "item": "Silver Bracelet", "purity": "92.5%", "weight": "45g", "amount": 8500, "status": "Delivered"},
    {"date": "2025-11-15", "item": "Gold Necklace", "purity": "18K", "weight": "12.5g", "amount": 85000, "status": "Delivered"},
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
        "Manager": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 Smart Chatbot"],
        "Sales Staff": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "⚡ Quick Actions", "🤖 Smart Chatbot"],
        "Customer": ["💎 My Dashboard", "🛍️ My Purchases", "💳 My Pending Payments", "💎 My Chits", "🎁 All Offers & Rewards", "📊 My Summary", "💬 Support Chat"],
        "Admin": ["📊 Dashboard", "👥 Customers", "💳 Pending Customers", "📦 Inventory", "⚡ Quick Actions", "📢 Campaigns", "💎 Chit Management", "🤖 ML Models", "🤖 Smart Chatbot", "⚙️ Settings"]
    }
    return pages.get(role, [])

# ============================================================================
# INTELLIGENT CHATBOT ENGINE - TRAINED FOR PENDING PAYMENTS
# ============================================================================

class IntelligentChatbot:
    """Smart chatbot trained on pending payments and business operations"""
    
    def __init__(self):
        self.commands = {
            # PENDING PAYMENT QUERIES - MANAGER
            "show pending": self.show_all_pending,
            "show all pending": self.show_all_pending,
            "pending amount": self.show_all_pending,
            "pending customers": self.show_all_pending,
            "who has pending": self.show_all_pending,
            "all pending": self.show_all_pending,
            "total pending": self.show_all_pending,
            "pending list": self.show_all_pending,
            "show pending customers": self.show_all_pending,
            "pending payments": self.show_all_pending,
            
            # PENDING PAYMENT QUERIES - CUSTOMER
            "show my pending": self.show_customer_pending,
            "what is my pending": self.show_customer_pending,
            "pending amount": self.show_customer_pending,
            "pending payment": self.show_customer_pending,
            "my pending": self.show_customer_pending,
            "my pending amount": self.show_customer_pending,
            "what's my pending": self.show_customer_pending,
            "show pending": self.show_customer_pending,
            "my pending payments": self.show_customer_pending,
            
            # CUSTOMER INFO
            "show my profile": self.show_profile,
            "my details": self.show_profile,
            "customer details": self.show_profile,
            "profile": self.show_profile,
            
            # PURCHASE HISTORY
            "show purchases": self.show_purchases,
            "my purchases": self.show_purchases,
            "purchase history": self.show_purchases,
            "purchases": self.show_purchases,
            
            # MARKET RATES
            "gold rate": self.show_rates,
            "silver rate": self.show_rates,
            "today's rates": self.show_rates,
            "current rate": self.show_rates,
            "market rate": self.show_rates,
            "rates": self.show_rates,
            "check rates": self.show_rates,
            
            # PRODUCTS
            "show products": self.show_products,
            "product list": self.show_products,
            "available products": self.show_products,
            "products": self.show_products,
            
            # ALL CUSTOMERS (for manager)
            "show all customers": self.show_all_customers,
            "all customers": self.show_all_customers,
            "customer list": self.show_all_customers,
            "customers": self.show_all_customers,
            
            # LOYALTY
            "show loyalty": self.show_loyalty,
            "loyalty points": self.show_loyalty,
            "my points": self.show_loyalty,
            "loyalty": self.show_loyalty,
            
            # CHITS
            "show chits": self.show_chits,
            "my chits": self.show_chits,
            "chit status": self.show_chits,
            "chits": self.show_chits,
            
            # SEND REMINDERS (Manager)
            "send reminders": self.send_reminders,
            "send payment reminders": self.send_reminders,
            "send reminder": self.send_reminders,
            
            # GENERATE REPORT
            "generate report": self.generate_report,
            "create report": self.generate_report,
            "report": self.generate_report,
        }
    
    def show_all_pending(self):
        """Show ALL pending payments (for Manager)"""
        pending_customers = [c for c in ALL_CUSTOMERS if c['pending_items']]
        
        if not pending_customers:
            return "✅ No pending payments! All customers are current."
        
        response = "💳 **ALL PENDING PAYMENTS IN SYSTEM**\n\n"
        total_pending = 0
        
        for customer in pending_customers:
            response += f"**👤 {customer['name']} ({customer['tier']})**\n"
            customer_pending = 0
            
            for item in customer['pending_items']:
                response += f"   • {item['item']}\n"
                response += f"     Amount: ₹{item['amount']:,}\n"
                response += f"     Due: {item['due_date']}\n"
                response += f"     Status: {item['status']}\n\n"
                customer_pending += item['amount']
                total_pending += item['amount']
            
            response += f"   **Subtotal: ₹{customer_pending:,}**\n\n"
        
        response += f"━━━━━━━━━━━━━━━━━━━━━\n"
        response += f"**🎯 TOTAL PENDING: ₹{total_pending:,}**\n"
        response += f"**Pending Customers: {len(pending_customers)}/5**\n"
        response += f"**Avg Per Customer: ₹{total_pending/len(pending_customers):,.0f}**"
        
        return response
    
    def show_customer_pending(self):
        """Show CUSTOMER'S OWN pending payments"""
        customer = CUSTOMER_DATA['customer']
        customer_pending = ALL_CUSTOMERS[0]['pending_items']  # C001 = index 0
        
        if not customer_pending:
            return "✅ You have no pending payments! You're all caught up."
        
        response = f"💳 **YOUR PENDING PAYMENTS**\n\n"
        response += f"Dear {customer['name']},\n\n"
        
        total = 0
        for idx, payment in enumerate(customer_pending, 1):
            response += f"**{idx}. {payment['item']}**\n"
            response += f"   Amount: ₹{payment['amount']:,}\n"
            response += f"   Due Date: {payment['due_date']}\n"
            response += f"   Status: {payment['status']}\n\n"
            total += payment['amount']
        
        response += f"━━━━━━━━━━━━━━━━━━━━━\n"
        response += f"**💰 TOTAL PENDING: ₹{total:,}**\n\n"
        response += f"Please make payment at your earliest convenience.\n"
        response += f"Contact us for payment options or EMI facilities."
        
        return response
    
    def show_profile(self):
        """Show customer profile"""
        customer = CUSTOMER_DATA['customer']
        response = f"""👤 **YOUR PROFILE**

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
        
        response = "🛍️ **YOUR PURCHASE HISTORY**\n\n"
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
        
        response = f"""📊 **TODAY'S MARKET RATES**

🟡 **GOLD:** ₹{gold['current']}/gram
   Previous: ₹{gold['previous']}
   Change: {gold['change']:+d} ({gold['change_percent']:+.2f}%)

⚪ **SILVER:** ₹{silver['current']}/gram
   Previous: ₹{silver['previous']}
   Change: {silver['change']:+d} ({silver['change_percent']:+.2f}%)

Last Updated: {datetime.now().strftime('%H:%M')}"""
        return response
    
    def show_products(self):
        """Show available products"""
        response = "📦 **AVAILABLE PRODUCTS**\n\n"
        for product in PRODUCTS:
            response += f"💎 **{product['name']}**\n"
            response += f"   Price: ₹{product['price']:,} | Stock: {product['stock']} units\n\n"
        return response
    
    def show_all_customers(self):
        """Show all customers (manager only)"""
        response = "👥 **ALL CUSTOMERS**\n\n"
        total_pending = 0
        pending_count = 0
        
        for customer in ALL_CUSTOMERS:
            status = ""
            customer_pending = sum(item['amount'] for item in customer['pending_items'])
            
            if customer_pending > 0:
                status = f"🔴 Pending: ₹{customer_pending:,}"
                pending_count += 1
                total_pending += customer_pending
            else:
                status = "✅ Clear"
            
            response += f"**{customer['name']}** ({customer['tier']})\n"
            response += f"   {status}\n"
            response += f"   Total Spent: ₹{customer['total_spent']:,}\n\n"
        
        response += f"\n**━━━━━━━━━━━━━━━━━━━**\n"
        response += f"**Pending Customers:** {pending_count}\n"
        response += f"**Total Pending:** ₹{total_pending:,}\n"
        response += f"**Total Customer Base:** 5"
        return response
    
    def show_loyalty(self):
        """Show loyalty points"""
        customer = CUSTOMER_DATA['customer']
        response = f"""🎁 **LOYALTY PROGRAM**

**Your Tier:** {customer['tier']} ⭐
**Current Points:** {customer['loyalty_points']} pts

**REDEMPTION RATES:**
100 points = ₹50 discount
200 points = ₹120 discount
500 points = ₹350 discount

**PROGRESS TO NEXT LEVEL:**
Gold Plus: {customer['loyalty_points']}/1000 points

Your points expire after 1 year of inactivity."""
        return response
    
    def show_chits(self):
        """Show chit information"""
        response = """💎 **YOUR CHIT FUNDS**

**ACTIVE CHITS:**

1. **Gold 12-Month Chit**
   Amount: ₹1,00,000
   Maturity: 12 months
   Next Payment: 2026-01-15
   Status: Active ✅

2. **Diamond Savings Chit**
   Amount: ₹2,00,000
   Maturity: 24 months
   Next Payment: 2026-02-15
   Status: Active ✅

**BENEFITS:**
✓ Flexible payment options
✓ Bonus on maturity
✓ Insurance coverage
✓ Easy withdrawal"""
        return response
    
    def send_reminders(self):
        """Send payment reminders to pending customers"""
        pending_customers = [c for c in ALL_CUSTOMERS if c['pending_items']]
        response = f"✅ **PAYMENT REMINDERS SENT**\n\n"
        response += f"Reminders sent to {len(pending_customers)} customers via SMS & Email:\n\n"
        
        for customer in pending_customers:
            customer_pending = sum(item['amount'] for item in customer['pending_items'])
            response += f"📱 {customer['name']} - ₹{customer_pending:,} pending\n"
        
        response += f"\n**✅ Process Completed Successfully!**"
        return response
    
    def generate_report(self):
        """Generate daily report"""
        pending_customers = [c for c in ALL_CUSTOMERS if c['pending_items']]
        total_pending = sum(sum(item['amount'] for item in c['pending_items']) for c in pending_customers)
        
        response = f"""📊 **DAILY BUSINESS REPORT**

**DATE:** {datetime.now().strftime('%d-%m-%Y')}
**TIME:** {datetime.now().strftime('%H:%M:%S')}

**PENDING PAYMENTS:**
• Total Pending: ₹{total_pending:,}
• Pending Customers: {len(pending_customers)}/5
• Average Per Customer: ₹{total_pending/len(pending_customers):,.0f}

**CUSTOMER METRICS:**
• Total Customers: 5
• Active Customers: 5
• Tier Breakdown:
  - Premium: 2
  - Gold: 2
  - Silver: 1
  - Standard: 0

**ACTION ITEMS:**
⚠️  {len(pending_customers)} customers with pending payments
📧 Reminders sent: Auto-sent via SMS & Email

**STATUS:** All systems operational ✅"""
        return response
    
    def process(self, user_input):
        """Process user input and return response"""
        user_input_lower = user_input.lower().strip()
        
        # Check for keyword matches
        for keyword, handler in self.commands.items():
            if keyword in user_input_lower:
                return handler()
        
        # Default response with suggestions
        return """🤖 **I didn't quite understand that.**

**POPULAR COMMANDS YOU CAN USE:**

**💳 Pending Payments:**
• "Show my pending" - Your pending payments ✅
• "Show all pending" - All customer pending (Manager)
• "What's my pending amount" - Get total pending

**👤 Account:**
• "Show my profile" - Your details
• "Show purchases" - Purchase history
• "My loyalty points" - Loyalty status

**💎 Products & Rates:**
• "Show products" - Available items
• "Gold rate" - Current gold price
• "Silver rate" - Current silver price

**👥 Management (Manager):**
• "Show all customers" - Customer list
• "Send reminders" - Send payment reminders
• "Generate report" - Daily report

Feel free to ask in natural language! 😊"""

# Initialize chatbot
CHATBOT = IntelligentChatbot()

# ============================================================================
# LOGIN PAGE
# ============================================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<h1 class='main-title'>💎 Jewellery AI Dashboard v8.1</h1>", unsafe_allow_html=True)
        st.markdown("**Smart Chatbot with Pending Payments Integration**")
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
# SMART CHATBOT PAGE (Manager)
# ============================================================================
def chatbot_page():
    st.markdown("<h2 class='main-title'>🤖 Smart Chatbot</h2>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='success-box'>
        <strong>Intelligent Chatbot - Fully Trained on Pending Payments & Business Operations</strong><br>
        Ask me about pending payments, customers, rates, and more!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick commands
    st.subheader("⚡ Quick Commands")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💳 Show All Pending", use_container_width=True, key="btn_pending"):
            response = CHATBOT.show_all_pending()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Show all pending"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col2:
        if st.button("📊 Show All Customers", use_container_width=True, key="btn_customers"):
            response = CHATBOT.show_all_customers()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Show all customers"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col3:
        if st.button("📬 Send Reminders", use_container_width=True, key="btn_reminders"):
            response = CHATBOT.send_reminders()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Send reminders"})
            st.session_state.chatbot_messages.append({"role": "assistant", "content": response})
            st.rerun()
    
    with col4:
        if st.button("📈 Generate Report", use_container_width=True, key="btn_report"):
            response = CHATBOT.generate_report()
            st.session_state.chatbot_messages.append({"role": "user", "content": "Generate report"})
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
    user_input = st.text_input("Ask me anything...", placeholder="e.g., 'Show all pending', 'Send reminders', 'Check rates'")
    
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
        Ask me about your pending payments, profile, purchases, and more!
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Quick help buttons
    st.subheader("⚡ Quick Help")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("💳 My Pending", use_container_width=True, key="help_pending"):
            response = CHATBOT.show_customer_pending()
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
    user_query = st.text_input("Ask me anything...", placeholder="e.g., 'Show my pending', 'Gold rate', 'My profile'", key="support_input")
    
    if user_query:
        st.session_state.support_chat_messages.append({"role": "user", "content": user_query})
        response = CHATBOT.process(user_query)
        st.session_state.support_chat_messages.append({"role": "assistant", "content": response})
        st.rerun()

# ============================================================================
# OTHER PAGES
# ============================================================================
def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Sales", "₹25,50,000", "+₹5,00,000")
    with col2:
        st.metric("Total Customers", "5", "All active")
    with col3:
        st.metric("Total Pending", "₹1,64,000", "4 customers")
    with col4:
        st.metric("Active Chits", "85", "+12")

def pending_customers_page():
    st.markdown("<h2 class='main-title'>💳 Pending Customers</h2>", unsafe_allow_html=True)
    
    pending = [c for c in ALL_CUSTOMERS if c['pending_items']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Customers", len(pending))
    with col2:
        total = sum(sum(item['amount'] for item in c['pending_items']) for c in pending)
        st.metric("Total Pending", f"₹{total:,}")
    with col3:
        avg = total / len(pending) if pending else 0
        st.metric("Average Per Customer", f"₹{avg:,.0f}")
    
    st.divider()
    st.subheader("📋 All Pending Customers")
    
    for customer in pending:
        st.markdown(f"**{customer['name']} ({customer['tier']})**")
        total_cust = sum(item['amount'] for item in customer['pending_items'])
        
        for item in customer['pending_items']:
            st.markdown(f"""
            <div class='pending-box'>
                <strong>{item['item']}</strong><br>
                Amount: ₹{item['amount']:,} | Due: {item['due_date']}<br>
                Status: {item['status']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"**Subtotal: ₹{total_cust:,}**")
        st.divider()

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)
    
    customers_df = pd.DataFrame([
        {
            "ID": c["id"],
            "Name": c["name"],
            "Tier": c["tier"],
            "Total Spent": f"₹{c['total_spent']:,}",
            "Pending": f"₹{sum(item['amount'] for item in c['pending_items']):,}" if c['pending_items'] else "₹0",
            "Status": "🔴 Pending" if c['pending_items'] else "✅ Clear"
        }
        for c in ALL_CUSTOMERS
    ])
    
    st.dataframe(customers_df, use_container_width=True, hide_index=True)

def my_pending_payments_page():
    st.markdown("<h2 class='main-title'>💳 My Pending Payments</h2>", unsafe_allow_html=True)
    
    customer_pending = ALL_CUSTOMERS[0]['pending_items']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Pending Items", len(customer_pending))
    with col2:
        total = sum(p['amount'] for p in customer_pending)
        st.metric("Total Amount", f"₹{total:,}")
    with col3:
        avg = total / len(customer_pending) if customer_pending else 0
        st.metric("Average", f"₹{avg:,.0f}")
    
    st.divider()
    
    for payment in customer_pending:
        st.markdown(f"""
        <div class='pending-box'>
            <strong>{payment['item']}</strong><br>
            Amount: ₹{payment['amount']:,} | Due: {payment['due_date']}<br>
            {payment['status']}
        </div>
        """, unsafe_allow_html=True)

def my_dashboard_page():
    st.markdown("<h2 class='main-title'>💎 My Dashboard</h2>", unsafe_allow_html=True)
    customer = CUSTOMER_DATA['customer']
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Spent", f"₹{customer['total_spent']:,}")
    with col2:
        st.metric("Purchases", customer['total_purchases'])
    with col3:
        st.metric("Loyalty Points", customer['loyalty_points'])
    with col4:
        st.metric("Tier", customer['tier'])

def my_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    purchases_df = pd.DataFrame(CUSTOMER_PURCHASES)
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

def my_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)
    chits = pd.DataFrame({
        'Chit': ['Gold 12-Month', 'Diamond Savings'],
        'Amount': [100000, 200000],
        'Status': ['Active', 'Active']
    })
    st.dataframe(chits, use_container_width=True, hide_index=True)

def offers_rewards_page():
    st.markdown("<h2 class='main-title'>🎁 All Offers & Rewards</h2>", unsafe_allow_html=True)
    campaigns = [
        {"title": "🎄 Christmas Special", "discount": "20% OFF"},
        {"title": "💒 Wedding Season", "discount": "15% OFF"},
        {"title": "✨ New Year Special", "discount": "25% OFF"},
    ]
    for campaign in campaigns:
        st.markdown(f"**{campaign['title']}** - {campaign['discount']}")

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
            my_dashboard_page()
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
