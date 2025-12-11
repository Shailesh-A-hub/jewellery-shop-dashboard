"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v8.0
Complete AI + BI System with Fixed Errors
Advanced AI Assistant with 8 Knowledge Categories + Staff Management + Campaigns + Smart Commands
Today's Gold & Silver Rates Included
ALL ERRORS FIXED - No Theme Toggle (Light Theme Only)
FEATURES: Campaign Management + Smart AI Commands + Customer AI Chatbox Fixed
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
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Light Theme Only
THEME = {
    "bg_color": "#f8f9fa",
    "card_bg": "#ffffff",
    "text_color": "#1a1a1a",
    "text_secondary": "#666666",
    "border_color": "#e0e0e0",
    "primary": "#FFD700",
    "success_bg": "#d4edda",
    "warning_bg": "#fff3cd",
    "error_bg": "#f8d7da",
    "info_bg": "#d1ecf1"
}

# Dynamic CSS Styling
st.markdown(f"""
<style>
    :root {{
        --bg-color: {THEME['bg_color']};
        --card-bg: {THEME['card_bg']};
        --text-color: {THEME['text_color']};
        --text-secondary: {THEME['text_secondary']};
        --border-color: {THEME['border_color']};
        --primary: {THEME['primary']};
    }}

    * {{
        color: var(--text-color);
    }}

    body {{
        background-color: var(--bg-color);
    }}

    .main {{
        background-color: var(--bg-color);
    }}

    .main-title {{ 
        font-size: 2.5rem; 
        font-weight: bold; 
        color: {THEME['primary']}; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}

    .metric-card {{ 
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        padding: 20px; 
        border-radius: 10px; 
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}

    .rate-card {{
        background: linear-gradient(135deg, #FFD700 0%, #FFA500 100%);
        padding: 20px;
        border-radius: 10px;
        color: #1a1a1a;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        font-weight: bold;
    }}

    .success-box {{ 
        background-color: {THEME['success_bg']}; 
        border-left: 4px solid #28a745; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}

    .warning-box {{ 
        background-color: {THEME['warning_bg']}; 
        border-left: 4px solid #ffc107; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}

    .error-box {{ 
        background-color: {THEME['error_bg']}; 
        border-left: 4px solid #dc3545; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}

    .info-box {{ 
        background-color: {THEME['info_bg']}; 
        border-left: 4px solid #17a2b8; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}

    .stDataFrame {{
        background-color: var(--card-bg);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }}

    .stTabs {{
        background-color: var(--card-bg);
        border-radius: 8px;
    }}

    .ai-response {{
        background-color: var(--card-bg);
        border: 2px solid {THEME['primary']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}

    .ai-suggestion {{
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
        border-left: 4px solid {THEME['primary']};
        padding: 10px 15px;
        margin: 8px 0;
        border-radius: 4px;
        cursor: pointer;
        transition: all 0.3s ease;
    }}

    .ai-suggestion:hover {{
        background: linear-gradient(135deg, rgba(255,215,0,0.15), rgba(255,215,0,0.1));
        transform: translateX(5px);
    }}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "📊 Dashboard"
    st.session_state.messages = []
    st.session_state.customer_messages = []
    st.session_state.ai_messages = []
    st.session_state.chatbot_messages = []
    st.session_state.smart_command_messages = []
    st.session_state.alerts = []  # Store staff alerts

# TODAY'S RATES (LIVE DATA)
TODAY_RATES = {
    "gold": {
        "current": 7850,
        "previous": 7800,
        "change": 50,
        "currency": "₹"
    },
    "silver": {
        "current": 95,
        "previous": 92,
        "change": 3,
        "currency": "₹"
    }
}

# MOCK STAFF DATA FOR ALERTS
STAFF_MEMBERS = {
    "ram": {"name": "Ram Kumar", "position": "Sales Executive", "pending": "₹15,000"},
    "priya": {"name": "Priya Singh", "position": "Manager", "pending": "₹8,500"},
    "amit": {"name": "Amit Verma", "position": "Sales Associate", "pending": "₹12,000"},
    "neha": {"name": "Neha Sharma", "position": "Cashier", "pending": "₹5,500"}
}

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
    """Return pages based on user role"""
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

def login_page():
    """Login page"""
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
# DASHBOARD PAGE (MANAGER/ADMIN)
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
        st.subheader("📈 Sales Trend")
        fig = px.line(x=dates, y=sales_data, title="Daily Sales (Nov-Dec 2025)")
        fig.update_xaxes(title="Date")
        fig.update_yaxes(title="Sales (₹)")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("💍 Product Category Distribution")
        categories = ['Gold', 'Silver', 'Diamond', 'Platinum']
        values = [45, 30, 20, 5]
        fig = px.pie(values=values, names=categories, title="Product Sales by Category")
        st.plotly_chart(fig, use_container_width=True)

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
        fig = px.bar(x=tiers, y=tier_counts, title="Customers by Tier")
        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def customers_page():
    st.markdown("<h2 class='main-title'>👥 Customers</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 All Customers", "➕ Add Customer", "🎁 Loyalty Program", "📊 Customer Analytics"])

    with tab1:
        st.subheader("Customer List")

        customers_df = pd.DataFrame({
            'ID': ['C001', 'C002', 'C003', 'C004', 'C005'],
            'Name': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Tier': ['Premium', 'Gold', 'Silver', 'Gold', 'Standard'],
            'Total Purchases': ['₹5,00,000', '₹3,50,000', '₹1,80,000', '₹2,20,000', '₹80,000'],
            'Loyalty Points': ['5000', '3500', '1800', '2200', '800'],
            'Last Purchase': ['2025-12-10', '2025-12-09', '2025-12-05', '2025-12-08', '2025-11-25']
        })

        st.dataframe(customers_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Add New Customer")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="cust_name")
            email = st.text_input("Email", key="cust_email")
            phone = st.text_input("Phone Number", key="cust_phone")

        with col2:
            tier = st.selectbox("Customer Tier", ["Standard", "Silver", "Gold", "Premium"], key="cust_tier")
            address = st.text_area("Address", key="cust_addr")
            dob = st.date_input("Date of Birth", key="cust_dob")

        if st.button("✅ Add Customer", use_container_width=True, key="add_cust_btn"):
            st.success("✅ Customer added successfully!")
            st.balloons()

    with tab3:
        st.subheader("💝 Loyalty Program")
        st.info("Loyalty Points Scheme:")
        st.markdown("""
        - 🥇 **Premium Tier:** 1 Point per ₹1 = 1% discount + exclusive offers
        - 🥈 **Gold Tier:** 1 Point per ₹2 = 0.5% discount + special events
        - 🥉 **Silver Tier:** 1 Point per ₹3 = 0.33% discount + birthday gifts
        - ⭐ **Standard Tier:** 1 Point per ₹5 = 0.2% discount
        """)

        loyalty_df = pd.DataFrame({
            'Tier': ['Premium', 'Gold', 'Silver', 'Standard'],
            'Points/Purchase': ['1 per ₹1', '1 per ₹2', '1 per ₹3', '1 per ₹5'],
            'Discount': ['1%', '0.5%', '0.33%', '0.2%'],
            'Redeem Rate': ['100 pts = ₹100', '100 pts = ₹50', '100 pts = ₹33', '100 pts = ₹20']
        })
        st.dataframe(loyalty_df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("📊 Customer Analytics")

        col1, col2 = st.columns(2)

        with col1:
            fig = px.pie(
                values=[250, 450, 350, 200],
                names=['Premium', 'Gold', 'Silver', 'Standard'],
                title="Customers by Tier"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                y=[120, 145, 165, 140, 190, 210],
                title="New Customers per Month"
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def inventory_page():
    st.markdown("<h2 class='main-title'>📦 Inventory</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Stock Status", "➕ Add Item", "📊 Low Stock Alert", "📈 Inventory Analytics"])

    with tab1:
        st.subheader("Current Inventory")

        inventory_df = pd.DataFrame({
            'Item Code': ['GLD001', 'SLV002', 'DMD003', 'PLT004', 'GLD005'],
            'Item Name': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring', 'Gold Necklace'],
            'Category': ['Gold', 'Silver', 'Diamond', 'Platinum', 'Gold'],
            'Quantity': [45, 120, 15, 8, 32],
            'Unit Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000', '₹22,000'],
            'Total Value': ['₹6,75,000', '₹2,40,000', '₹7,50,000', '₹6,00,000', '₹7,04,000'],
            'Status': ['✅ In Stock', '✅ In Stock', '⚠️ Low Stock', '🔴 Critical', '✅ In Stock']
        })

        st.dataframe(inventory_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Add New Item")

        col1, col2 = st.columns(2)
        with col1:
            item_name = st.text_input("Item Name", key="inv_name")
            category = st.selectbox("Category", ["Gold", "Silver", "Diamond", "Platinum", "Other"], key="inv_cat")
            quantity = st.number_input("Quantity", min_value=1, key="inv_qty")

        with col2:
            item_code = st.text_input("Item Code", key="inv_code")
            unit_price = st.number_input("Unit Price (₹)", min_value=100, key="inv_price")
            supplier = st.text_input("Supplier Name", key="inv_supplier")

        if st.button("✅ Add Item", use_container_width=True, key="add_inv_btn"):
            total_val = quantity * unit_price
            st.success(f"✅ Item added! Total Value: ₹{total_val:,}")

    with tab3:
        st.subheader("⚠️ Low Stock Alerts")
        st.markdown("""
        <div class='warning-box'>
        <strong>⚠️ Low Stock Items:</strong><br>
        • Diamond Pendant (GLD003) - Only 15 units<br>
        • Platinum Ring (PLT004) - Only 8 units<br>
        <strong>Action Required:</strong> Order more stock to avoid stockouts
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
            fig = px.bar(
                x=['Gold', 'Silver', 'Diamond', 'Platinum'],
                y=[45+32, 120, 15, 8],
                title="Stock Quantity by Category"
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.pie(
                values=[6.75+7.04, 2.40, 7.50, 6.00],
                names=['Gold', 'Silver', 'Diamond', 'Platinum'],
                title="Inventory Value Distribution (in Lakhs)"
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAX & COMPLIANCE PAGE
# ============================================================================

def tax_compliance_page():
    st.markdown("<h2 class='main-title'>💰 Tax & Compliance</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tax Dashboard", "📄 GST Reports", "💳 Invoices", "📋 Compliance Checklist"])

    with tab1:
        st.subheader("Tax Summary")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Monthly Sales", "₹45,00,000", "+₹5,00,000")
        with col2:
            st.metric("GST (18%)", "₹8,10,000", "+₹90,000")
        with col3:
            st.metric("GST Payable", "₹6,50,000", "+₹50,000")
        with col4:
            st.metric("Tax Rate", "18%", "GST")

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
            'Status': ['✅ Paid', '✅ Paid', '⏳ Pending', '⏳ Pending']
        })

        st.dataframe(invoices, use_container_width=True, hide_index=True)

        st.markdown("**Create New Invoice**")
        col1, col2 = st.columns(2)
        with col1:
            customer = st.selectbox("Customer", ["Rajesh Patel", "Priya Singh", "Amit Kumar"], key="inv_cust")
            amount = st.number_input("Amount", min_value=100, key="inv_amt")
        with col2:
            gst_rate = st.selectbox("GST Rate", ["5%", "12%", "18%"], key="gst_rate")
            payment_mode = st.selectbox("Payment Mode", ["Cash", "Card", "Cheque", "UPI"], key="pay_mode")

        if st.button("📄 Generate Invoice", use_container_width=True, key="gen_inv_btn"):
            st.success("✅ Invoice generated successfully!")

    with tab4:
        st.subheader("📋 Compliance Checklist")

        compliance_items = [
            ("✅", "GST Registration", "Registered - GSTIN: 27ABCXYZ123"),
            ("✅", "Monthly GST Filing", "Nov 2025 filed on time"),
            ("⚠️", "Audit", "Pending - Scheduled for Jan 2026"),
            ("✅", "BIS Hallmark", "All gold items hallmarked"),
            ("✅", "Invoice Records", "Maintained for 5 years"),
            ("❌", "Labor License", "Renewal pending"),
            ("✅", "Employee PF/ESIC", "All compliant"),
            ("✅", "Bank Reconciliation", "Monthly reconciliation done")
        ]

        for status, item, details in compliance_items:
            st.markdown(f"{status} **{item}:** {details}")

# ============================================================================
# CAMPAIGNS PAGE (NEW)
# ============================================================================

def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Active Campaigns", "➕ Create Campaign", "📈 Performance Analytics", "🎯 Campaign ROI"])

    with tab1:
        st.subheader("📊 All Active Campaigns")

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
        st.subheader("➕ Create New Campaign")

        col1, col2 = st.columns(2)

        with col1:
            campaign_name = st.text_input("Campaign Name", key="camp_name")
            campaign_type = st.selectbox("Campaign Type", 
                ["Seasonal Sale", "Festival Offer", "Clearance", "Loyalty Reward", "Referral", "Flash Sale"], 
                key="camp_type")
            discount = st.slider("Discount %", 5, 50, 15, key="camp_discount")
            start_date = st.date_input("Start Date", key="camp_start")

        with col2:
            target_revenue = st.number_input("Target Revenue (₹)", min_value=100000, step=100000, key="camp_target")
            budget = st.number_input("Marketing Budget (₹)", min_value=10000, step=10000, key="camp_budget")
            end_date = st.date_input("End Date", key="camp_end")
            description = st.text_area("Campaign Description", key="camp_desc")

        col1, col2 = st.columns(2)

        with col1:
            include_email = st.checkbox("Email Campaign", value=True, key="camp_email")

        with col2:
            include_sms = st.checkbox("SMS Campaign", value=True, key="camp_sms")

        if st.button("🚀 Launch Campaign", use_container_width=True, key="launch_camp_btn"):
            st.success(f"✅ Campaign '{campaign_name}' launched successfully!")
            st.balloons()
            st.markdown(f"""
            <div class='success-box'>
            <strong>Campaign Details:</strong><br>
            📛 Name: {campaign_name}<br>
            🎯 Target: ₹{target_revenue:,}<br>
            💰 Budget: ₹{budget:,}<br>
            📅 Duration: {start_date} to {end_date}<br>
            🏷️ Discount: {discount}%
            </div>
            """, unsafe_allow_html=True)

    with tab3:
        st.subheader("📈 Campaign Performance Analytics")

        col1, col2 = st.columns(2)

        with col1:
            fig = px.bar(
                x=['Diwali', 'Wedding', 'Clearance', 'New Year'],
                y=[45, 32, 25, 0],
                title="Campaign Revenue (in Lakhs)",
                color=['#FFD700', '#FF69B4', '#FF6347', '#87CEEB']
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.line(
                x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                y=[8.5, 12.3, 14.2, 10.0],
                title="Revenue Trend by Week (in Lakhs)",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Campaign Conversion Rates**")
            conv_df = pd.DataFrame({
                'Campaign': ['Diwali', 'Wedding', 'Clearance'],
                'Impressions': ['50,000', '45,000', '40,000'],
                'Clicks': ['12,500', '9,000', '8,000'],
                'Conversions': ['450', '320', '250'],
                'Conv. Rate': ['3.6%', '3.5%', '3.1%']
            })
            st.dataframe(conv_df, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Customer Tier Distribution**")
            tier_df = pd.DataFrame({
                'Tier': ['Premium', 'Gold', 'Silver', 'Standard'],
                'Campaign 1': ['120', '200', '100', '30'],
                'Campaign 2': ['95', '150', '60', '15'],
                'Campaign 3': ['70', '120', '50', '10']
            })
            st.dataframe(tier_df, use_container_width=True, hide_index=True)

    with tab4:
        st.subheader("🎯 Campaign ROI Analysis")

        roi_data = pd.DataFrame({
            'Campaign': ['Diwali Sale', 'Wedding Season', 'Clearance Sale', 'New Year Special'],
            'Revenue': ['₹45,00,000', '₹32,00,000', '₹25,00,000', '₹0'],
            'Budget': ['₹15,00,000', '₹12,80,000', '₹13,90,000', '₹5,00,000'],
            'Profit': ['₹30,00,000', '₹19,20,000', '₹11,10,000', '-₹5,00,000'],
            'ROI': ['200%', '150%', '80%', '-100%'],
            'Status': ['🏆 Excellent', '⭐ Very Good', '✅ Good', '⏳ Upcoming']
        })

        st.dataframe(roi_data, use_container_width=True, hide_index=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Best Performing Products**")
            best_prod = pd.DataFrame({
                'Product': ['Diamond Pendant', 'Gold Ring', 'Gold Necklace'],
                'Units Sold': ['380', '450', '280'],
                'Revenue': ['₹38,00,000', '₹22,50,000', '₹28,00,000']
            })
            st.dataframe(best_prod, use_container_width=True, hide_index=True)

        with col2:
            st.markdown("**Campaign Comparison**")
            fig = px.pie(
                values=[200, 150, 80],
                names=['Diwali', 'Wedding', 'Clearance'],
                title="ROI Distribution by Campaign"
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# STAFF MANAGEMENT PAGE
# ============================================================================

def staff_management_page():
    st.markdown("<h2 class='main-title'>👨‍💼 Staff Management</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📋 Staff Directory", "➕ Add Staff", "📊 Performance", "💰 Salary & Bonus"])

    with tab1:
        st.subheader("Staff Directory")

        staff_df = pd.DataFrame({
            'ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'Name': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma', 'Vikram Patel'],
            'Position': ['Sales Executive', 'Manager', 'Sales Associate', 'Cashier', 'Sales Executive'],
            'Floor': ['Floor 1', 'Floor 2', 'Floor 1', 'Ground', 'Floor 2'],
            'Joining Date': ['2024-01-15', '2023-06-10', '2024-03-20', '2024-02-28', '2024-05-01'],
            'Pending': ['₹15,000', '₹8,500', '₹12,000', '₹5,500', '₹18,000'],
            'Status': ['✅ Active', '✅ Active', '✅ Active', '✅ Active', '✅ Active']
        })

        st.dataframe(staff_df, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Add New Staff Member")

        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", key="staff_name")
            position = st.selectbox("Position", ["Sales Executive", "Sales Associate", "Manager", "Cashier"], key="staff_pos")
            joining_date = st.date_input("Joining Date", key="staff_join")

        with col2:
            email = st.text_input("Email", key="staff_email")
            phone = st.text_input("Phone", key="staff_phone")
            floor = st.selectbox("Floor Assignment", ["Ground", "Floor 1", "Floor 2"], key="staff_floor")

        if st.button("✅ Add Staff", use_container_width=True, key="add_staff_btn"):
            st.success("✅ Staff member added successfully!")
            st.balloons()

    with tab3:
        st.subheader("📊 Staff Performance")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Monthly Sales by Staff**")
            perf_df = pd.DataFrame({
                'Staff': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma', 'Vikram Patel'],
                'Sales (₹)': ['12,50,000', '15,60,000', '10,80,000', '9,80,000', '8,40,000'],
                'Target': ['₹12,00,000', '₹15,00,000', '₹10,00,000', '₹9,50,000', '₹8,00,000'],
                'Achievement': ['104%', '104%', '108%', '103%', '105%']
            })
            st.dataframe(perf_df, use_container_width=True, hide_index=True)

        with col2:
            fig = px.bar(
                x=['Ram', 'Priya', 'Amit', 'Neha', 'Vikram'],
                y=[12.5, 15.6, 10.8, 9.8, 8.4],
                title="Staff Sales Performance (in Lakhs)"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("💰 Salary & Bonus Management")

        salary_df = pd.DataFrame({
            'Staff': ['Ram Kumar', 'Priya Singh', 'Amit Verma', 'Neha Sharma', 'Vikram Patel'],
            'Base Salary': ['₹25,000', '₹35,000', '₹22,000', '₹20,000', '₹18,000'],
            'Allowance': ['₹5,000', '₹7,000', '₹4,000', '₹3,500', '₹3,000'],
            'Bonus (Dec)': ['₹10,000', '₹12,000', '₹8,500', '₹7,500', '₹6,500'],
            'Total (Dec)': ['₹40,000', '₹54,000', '₹34,500', '₹31,000', '₹27,500']
        })

        st.dataframe(salary_df, use_container_width=True, hide_index=True)

# ============================================================================
# SALES RECORD PAGE (STAFF)
# ============================================================================

def sales_record_page():
    st.markdown("<h2 class='main-title'>💾 Sales Record</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📝 Record Sale", "📊 My Sales", "📈 Sales Trend"])

    with tab1:
        st.subheader("Record New Sale")

        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.text_input("Customer Name", key="sale_cust")
            item = st.selectbox("Item", ["Gold Ring", "Diamond Pendant", "Silver Bracelet", "Platinum Ring"], key="sale_item")
            quantity = st.number_input("Quantity", min_value=1, key="sale_qty")

        with col2:
            price = st.number_input("Price (₹)", min_value=100, key="sale_price")
            payment_mode = st.selectbox("Payment", ["Cash", "Card", "Cheque", "UPI"], key="sale_payment")
            sale_date = st.date_input("Sale Date", key="sale_date")

        if st.button("✅ Record Sale", use_container_width=True, key="record_sale_btn"):
            total = quantity * price
            st.success(f"✅ Sale recorded! Total: ₹{total:,}")
            st.balloons()

    with tab2:
        st.subheader("My Sales Record")

        my_sales = pd.DataFrame({
            'Date': ['2025-12-10', '2025-12-09', '2025-12-08', '2025-12-07'],
            'Customer': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma'],
            'Item': ['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Gold Necklace'],
            'Qty': [1, 1, 2, 1],
            'Amount': ['₹15,000', '₹50,000', '₹4,000', '₹22,000'],
            'Payment': ['Cash', 'Card', 'UPI', 'Cash']
        })

        st.dataframe(my_sales, use_container_width=True, hide_index=True)
        st.metric("Total This Month", "₹12,50,000", "+₹50,000")

    with tab3:
        st.subheader("📈 My Sales Trend")

        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                y=[2.8, 3.2, 3.1, 2.9],
                title="Weekly Sales (in Lakhs)",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            fig = px.bar(
                x=['Target', 'Actual'],
                y=[12, 12.5],
                title="Target vs Actual (in Lakhs)"
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# QUICK ACTIONS PAGE
# ============================================================================

def quick_actions_page():
    st.markdown("<h2 class='main-title'>⚡ Quick Actions</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💰 New Sale", use_container_width=True, key="quick_sale"):
            st.success("✅ New sale initiated!")

    with col2:
        if st.button("👥 Add Customer", use_container_width=True, key="quick_cust"):
            st.success("✅ Customer addition form opened!")

    with col3:
        if st.button("📦 Check Stock", use_container_width=True, key="quick_stock"):
            st.success("✅ Stock check initiated!")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("💎 New Chit", use_container_width=True, key="quick_chit"):
            st.success("✅ Chit creation form opened!")

    with col2:
        if st.button("📊 Generate Report", use_container_width=True, key="quick_report"):
            st.success("✅ Report generation started!")

    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True, key="quick_loyalty"):
            st.success("✅ Loyalty points calculator opened!")

# ============================================================================
# ADVANCED AI ASSISTANT PAGE
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant - Business Intelligence</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>🤖 Advanced Business Intelligence System</strong><br>
    Real-time analytics and insights for managers. 8 Knowledge Categories including Staff Management!
    </div>
    """, unsafe_allow_html=True)

    ai_knowledge = {
        "stock": {
            "icon": "📦",
            "title": "Stock & Inventory",
            "response": """📦 **Stock & Inventory Status:**

• **Gold items:** 77 units (₹13.79L value)
• **Silver items:** 120 units (₹2.40L value)
• **Diamond items:** 15 units (₹7.50L value) - ⚠️ Low stock!
• **Platinum items:** 8 units (₹6.00L value) - 🔴 Critical!

**Total Inventory Value:** ₹29.09 Lakhs
**Action Required:** Reorder Diamond & Platinum items immediately to avoid stockouts."""
        },

        "sales": {
            "icon": "💰",
            "title": "Sales & Revenue",
            "response": """💰 **Sales & Revenue Report:**

**Daily Metrics:**
• Today's sales: ₹1,85,000
• Weekly sales: ₹12,50,000
• Monthly sales: ₹45,00,000 (+₹5,00,000 vs last month)

**Top Performers:**
1. Diamond Pendant: ₹38,00,000 (28% of sales)
2. Gold Ring: ₹22,50,000 (16% of sales)
3. Gold Necklace: ₹28,00,000 (20% of sales)

**Trend Analysis:** ✅ Sales growing 12% month-over-month (Seasonal peak approaching)"""
        },

        "customer": {
            "icon": "👥",
            "title": "Customers",
            "response": """👥 **Customer Analytics:**

**Total Customers:** 1,250 (+45 this month)

**Tier Distribution:**
• 🥇 Premium Tier: 250 (20%) - ₹36,000 avg value
• 🥈 Gold Tier: 450 (36%) - ₹28,000 avg value
• 🥉 Silver Tier: 350 (28%) - ₹18,000 avg value
• ⭐ Standard Tier: 200 (16%) - ₹8,000 avg value

**Key Metrics:**
• Average customer value: ₹36,000
• Loyalty program enrollment: 92%
• Customer retention rate: 87%

**Recommendation:** Focus on upgrading Standard tier customers to Silver tier."""
        },

        "chit": {
            "icon": "💎",
            "title": "Chits & Collections",
            "response": """💎 **Chit Management Status:**

**Active Chits:** 85 (+12 this month)
• Gold 12-Month Chits: 35 (₹35,00,000)
• Silver 6-Month Chits: 30 (₹15,00,000)
• Diamond Savings Chits: 15 (₹12,00,000)
• Platinum Plus Chits: 5 (₹3,00,000)

**Performance:**
• Total members: 127
• Total value: ₹65,00,000
• Monthly collection: ₹9,50,000
• Payment status: 94% on-time payments

**Upcoming:** 12 chit payouts scheduled this month"""
        },

        "staff": {
            "icon": "👨‍💼",
            "title": "Staff & Team",
            "response": """👨‍💼 **Staff & Team Performance:**

**Top 3 Performers:**
1. 🏆 Priya Singh - ₹15,60,000 (104% of target)
2. 🥈 Ram Kumar - ₹12,50,000 (104% of target)
3. 🥉 Amit Verma - ₹10,80,000 (108% of target)

**Team Metrics:**
• Average team sales: ₹11,42,000 per person
• Team bonus pool: ₹44,000 (December)
• Overall target achievement: 105%
• Sales growth vs last month: +8%

**Staff Strength:** 5 active members
**Salary commitment:** ₹91,500/month"""
        },

        "tax": {
            "icon": "💵",
            "title": "Tax & Compliance",
            "response": """💵 **Tax & Compliance Status:**

**GST Filing:**
✅ November 2025 - Filed on time
📅 December 2025 - Due 20th December
• GST Rate: 18%
• Current GST payable: ₹6,50,000
• YTD tax collected: ₹15,66,000

**Compliance Status:** 7/8 ✅
✅ GST Registration (GSTIN: 27ABCXYZ123)
✅ Monthly GST Filing
⚠️ Audit (Pending - Jan 2026)
✅ BIS Hallmark
✅ Invoice Records (5 years)
❌ Labor License (Renewal due Jan 15)
✅ Employee PF/ESIC
✅ Bank Reconciliation

**Action:** Renew labor license before Jan 15, 2026"""
        },

        "campaign": {
            "icon": "📢",
            "title": "Campaigns",
            "response": """📢 **Campaign Performance:**

**Active Campaigns (Dec 2025):**

1. 🎄 **Diwali Sale 2025** - 20% discount
   • Revenue: ₹45,00,000
   • ROI: 285%
   • Conversions: 450 orders

2. 💒 **Wedding Season Special** - 15% discount
   • Revenue: ₹32,00,000
   • ROI: 250%
   • Conversions: 320 orders

3. 🎉 **Clearance Sale** - 30% discount
   • Revenue: ₹25,00,000
   • ROI: 180%
   • Conversions: 250 orders

**Total Campaign Revenue:** ₹1,02,00,000
**Average ROI:** 238% (Excellent performance!)

**Recommendation:** Extend Wedding Season campaign"""
        },

        "forecast": {
            "icon": "📈",
            "title": "Forecasting",
            "response": """📈 **Demand Forecasting & Trends:**

**Predicted Demand (Next 30 Days):**
📈 Gold items: ↑ 48 units (current: 45)
📈 Silver items: ↑ 135 units (current: 120)
📈 Diamond items: ↑ 18 units (current: 15)
📈 Platinum items: ↑ 10 units (current: 8)

**Seasonal Analysis:**
• Wedding season approaching (Jan-Mar)
• Expected demand surge: +35%
• Best selling categories: Diamond & Gold
• Confidence level: 92%

**Recommendations:**
✅ Increase gold & diamond stock
✅ Prepare for Q1 peak demand
✅ Plan marketing campaigns now
✅ Ensure staff availability"""
        }
    }

    st.subheader("📊 AI Business Intelligence - 8 Categories")

    st.markdown("<h4>Quick Analysis Tools:</h4>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("📦 Stock Analysis", use_container_width=True, key="ai_stock_btn"):
            st.session_state.ai_messages = [{"role": "assistant", "content": ai_knowledge["stock"]["response"]}]
            st.rerun()

    with col2:
        if st.button("💰 Revenue Analysis", use_container_width=True, key="ai_sales_btn"):
            st.session_state.ai_messages = [{"role": "assistant", "content": ai_knowledge["sales"]["response"]}]
            st.rerun()

    with col3:
        if st.button("👥 Customer Insights", use_container_width=True, key="ai_cust_btn"):
            st.session_state.ai_messages = [{"role": "assistant", "content": ai_knowledge["customer"]["response"]}]
            st.rerun()

    with col4:
        if st.button("📈 Demand Forecast", use_container_width=True, key="ai_forecast_btn"):
            st.session_state.ai_messages = [{"role": "assistant", "content": ai_knowledge["forecast"]["response"]}]
            st.rerun()

    st.divider()

    st.markdown("""
    <div class='info-box'>
    <strong>🤖 8 Business Intelligence Categories:</strong><br>
    📦 Stock Analysis | 💰 Revenue & Sales | 👥 Customer Insights | 💎 Chit Performance | 
    👨‍💼 Staff Analytics | 💵 Tax Compliance | 📢 Campaign ROI | 📈 Demand Forecasting
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.ai_messages:
        with st.chat_message(message["role"]):
            st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)

    if prompt := st.chat_input("Ask about stock, sales, customers, staff, chits, tax, campaigns, forecasting..."):
        st.session_state.ai_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        response = "🤖 I'm your Business Intelligence Assistant. I analyze 8 categories:\n\n📦 **Stock & Inventory** | 💰 **Sales & Revenue** | 👥 **Customers** | 💎 **Chits** | 👨‍💼 **Staff Management** | 💵 **Tax & Compliance** | 📢 **Campaigns** | 📈 **Forecasting**\n\nWhat would you like to analyze?"

        prompt_lower = prompt.lower()

        keywords_map = {
            "stock": ["stock", "inventory", "items", "quantity", "reorder", "warehouse", "units"],
            "sales": ["sales", "revenue", "income", "earnings", "performance", "turnover", "monetary"],
            "customer": ["customer", "client", "buyer", "tier", "loyalty", "purchase", "user"],
            "chit": ["chit", "collection", "member", "installment", "payout", "scheme", "savings"],
            "staff": ["staff", "employee", "performer", "salary", "bonus", "team", "worker", "sales executive", "position"],
            "tax": ["tax", "gst", "invoice", "compliance", "filing", "audit", "return"],
            "campaign": ["campaign", "promotion", "sale", "offer", "discount", "roi", "marketing"],
            "forecast": ["forecast", "predict", "demand", "trend", "seasonal", "projection"]
        }

        for category, keywords in keywords_map.items():
            if any(kw in prompt_lower for kw in keywords):
                response = ai_knowledge[category]["response"]
                break

        st.session_state.ai_messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(f"""<div class='ai-response'>{response}</div>""", unsafe_allow_html=True)

# ============================================================================
# SMART COMMANDS PAGE (NEW - For sending alerts to staff)
# ============================================================================

def smart_commands_page():
    st.markdown("<h2 class='main-title'>💬 Smart Commands - Staff Alerts</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='info-box'>
    <strong>🎯 Smart Command System</strong><br>
    Send alerts and commands to staff members. Example: "Alert Ram about pending ₹15,000" or "Send notification to all staff about meeting"
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🔔 Alert Ram - Pending ₹15,000", use_container_width=True, key="alert_ram"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Ram about pending ₹15,000"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Ram Kumar has been notified\n📛 Alert: Pending amount ₹15,000\n⏰ Time: " + datetime.now().strftime("%H:%M") + "\n📱 Status: Delivered via SMS & In-app notification"}
            ]
            st.rerun()

    with col2:
        if st.button("🔔 Alert Priya - Pending ₹8,500", use_container_width=True, key="alert_priya"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Alert Priya about pending ₹8,500"},
                {"role": "assistant", "content": "🔔 **Alert Sent Successfully**\n\n✅ Priya Singh has been notified\n📛 Alert: Pending amount ₹8,500\n⏰ Time: " + datetime.now().strftime("%H:%M") + "\n📱 Status: Delivered via SMS & In-app notification"}
            ]
            st.rerun()

    with col3:
        if st.button("📢 Notify All Staff", use_container_width=True, key="alert_all"):
            st.session_state.smart_command_messages = [
                {"role": "user", "content": "Send notification to all staff"},
                {"role": "assistant", "content": "📢 **Broadcast Alert Sent Successfully**\n\n✅ All 5 staff members notified\n👥 Recipients: Ram, Priya, Amit, Neha, Vikram\n📌 Message: Staff meeting at 2 PM\n📱 Status: All delivered"}
            ]
            st.rerun()

    st.divider()

    st.subheader("📤 Send Custom Alert/Command")

    col1, col2 = st.columns([3, 1])

    with col1:
        custom_command = st.text_input(
            "Enter command",
            placeholder="e.g., 'Alert Ram about his pending amount' or 'Send notification to all staff'",
            key="custom_cmd"
        )

    with col2:
        send_btn = st.button("📤 Send", use_container_width=True, key="send_cmd_btn")

    if send_btn and custom_command:
        # Process the command
        command_lower = custom_command.lower()

        # Check for staff name and pending amount
        staff_alerts = {
            "ram": {"name": "Ram Kumar", "pending": "₹15,000"},
            "priya": {"name": "Priya Singh", "pending": "₹8,500"},
            "amit": {"name": "Amit Verma", "pending": "₹12,000"},
            "neha": {"name": "Neha Sharma", "pending": "₹5,500"}
        }

        response = "❌ Command not recognized. Please try: 'Alert [staff name] about [message]' or 'Send notification to all staff'"

        # Check if it's an alert command
        if "alert" in command_lower or "notify" in command_lower or "send" in command_lower:
            for staff_key, staff_info in staff_alerts.items():
                if staff_key in command_lower:
                    response = f"""🔔 **Alert Sent Successfully**

✅ {staff_info['name']} has been notified
📛 Alert: {custom_command}
⏰ Time: {datetime.now().strftime("%H:%M")}
📱 Status: Delivered via SMS & In-app notification
💰 Pending: {staff_info['pending']}"""
                    break
            else:
                # Check if it's a broadcast to all
                if "all" in command_lower:
                    response = f"""📢 **Broadcast Alert Sent Successfully**

✅ All 5 staff members notified
👥 Recipients: Ram, Priya, Amit, Neha, Vikram
📌 Message: {custom_command}
⏰ Time: {datetime.now().strftime("%H:%M")}
📱 Status: All delivered"""

        st.session_state.smart_command_messages.append({"role": "user", "content": custom_command})
        st.session_state.smart_command_messages.append({"role": "assistant", "content": response})
        st.rerun()

    st.divider()

    st.subheader("📋 Command History")

    for message in st.session_state.smart_command_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"**Command:** {message['content']}")

# ============================================================================
# CHATBOT PAGE
# ============================================================================

def chatbot_page():
    st.markdown("<h2 class='main-title'>💬 Smart Chatbot - Customer Support</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class='success-box'>
    <strong>💬 Customer Support Chatbot</strong><br>
    Get instant answers about purchases, chits, loyalty, offers, delivery, and more!
    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎯 Quick Help Topics")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📦 Purchase Help", use_container_width=True, key="cb_purchase"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "📦 **Your Purchases:**\nYou have 4 purchase records. Most recent: Gold Ring (Dec 10, ₹15,000). All items delivered ✅. You earned 890 loyalty points!"}]
            st.rerun()

    with col2:
        if st.button("💎 Chit Support", use_container_width=True, key="cb_chit"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "💎 **Your Chits:**\nYou have 2 active chits:\n• Gold 12-Month: ₹1,00,000 (6/12 paid, next due Dec 15)\n• Diamond Savings: ₹2,00,000 (3/20 paid, next due Dec 20)"}]
            st.rerun()

    with col3:
        if st.button("🎁 Loyalty Points", use_container_width=True, key="cb_loyalty"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "🎁 **Loyalty Program:**\nYou're in Gold Tier! Benefits:\n✅ 15% Birthday Discount\n✅ Free maintenance on 1 item/year\n✅ Early access to new collections\n✅ ₹2,000 birthday voucher"}]
            st.rerun()

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("📫 Delivery Tracking", use_container_width=True, key="cb_delivery"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "📫 **Delivery Status:**\nAll your purchases are delivered ✅\n• Recent: Gold Ring - Delivered Dec 10\n• All items insured & tracked"}]
            st.rerun()

    with col2:
        if st.button("🎉 Offers & Discounts", use_container_width=True, key="cb_offers"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "🎉 **Active Offers:**\n✅ Wedding Season: 15% OFF\n✅ Clearance Sale: 30% OFF selected items\n✅ Loyalty Redemption: 100 pts = ₹50\n✅ Referral Bonus: ₹500 per friend"}]
            st.rerun()

    with col3:
        if st.button("⭐ General Help", use_container_width=True, key="cb_help"):
            st.session_state.chatbot_messages = [{"role": "assistant", "content": "👋 Hi! I'm your support chatbot. I can help with purchases, chits, loyalty, offers, delivery, and points. What do you need?"}]
            st.rerun()

    st.divider()

    st.markdown("""
    <div class='info-box'>
    <strong>✅ Chatbot Can Help With:</strong><br>
    📦 Purchase tracking | 💎 Chit payments & deadlines | 🎁 Loyalty redemption | 
    📫 Delivery status | 🎉 Active offers & discounts | ⭐ General questions
    </div>
    """, unsafe_allow_html=True)

    for message in st.session_state.chatbot_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything! I'm here to help..."):
        st.session_state.chatbot_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        chatbot_responses = {
            "purchase": "📦 Your recent purchases are delivered. You earned 890 loyalty points! Use them to get discounts.",
            "chit": "💎 You have 2 active chits worth ₹3,00,000. Next payment due Dec 15.",
            "loyalty": "🎁 You're in Gold tier! Enjoy 15% birthday discount and free maintenance on 1 item/year.",
            "offer": "🎉 Active offers: 15% wedding discount, 30% clearance sale, ₹500 referral bonus!",
            "delivery": "📫 All your items are delivered. Track status in My Purchases.",
            "points": "⭐ You have 890 loyalty points. 100 points = ₹50 discount!",
            "help": "I can help with: Purchases, Chits, Loyalty, Offers, Delivery, or Points!"
        }

        response = "Thank you for contacting us! How can I help you today?"
        prompt_lower = prompt.lower()

        for keyword, ans in chatbot_responses.items():
            if keyword in prompt_lower:
                response = ans
                break

        st.session_state.chatbot_messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(f"""<div class='ai-response'>{response}</div>""", unsafe_allow_html=True)

# ============================================================================
# CUSTOMER PORTAL PAGES
# ============================================================================

def customer_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)

    st.subheader("💰 Today's Metal Rates")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥇 Gold (Per Gram)</h3>
        <h2>₹{TODAY_RATES['gold']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['gold']['change']} (+{(TODAY_RATES['gold']['change']/TODAY_RATES['gold']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['gold']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥈 Silver (Per Gram)</h3>
        <h2>₹{TODAY_RATES['silver']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['silver']['change']} (+{(TODAY_RATES['silver']['change']/TODAY_RATES['silver']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['silver']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    purchases_df = pd.DataFrame({
        'Date': ['2025-12-10', '2025-12-05', '2025-11-28', '2025-11-15'],
        'Item': ['Gold Ring', 'Diamond Pendant', 'Silver Bracelet', 'Gold Necklace'],
        'Amount': ['₹15,000', '₹50,000', '₹2,000', '₹22,000'],
        'Points Earned': ['150', '500', '20', '220'],
        'Status': ['✅ Delivered', '✅ Delivered', '✅ Delivered', '✅ Delivered']
    })

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Spent", "₹89,000")
    with col2:
        st.metric("Loyalty Points", "890")

    st.subheader("Purchase History")
    st.dataframe(purchases_df, use_container_width=True, hide_index=True)

def customer_chits_page():
    st.markdown("<h2 class='main-title'>💎 My Chits</h2>", unsafe_allow_html=True)

    st.subheader("💰 Today's Metal Rates")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥇 Gold (Per Gram)</h3>
        <h2>₹{TODAY_RATES['gold']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['gold']['change']} (+{(TODAY_RATES['gold']['change']/TODAY_RATES['gold']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['gold']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥈 Silver (Per Gram)</h3>
        <h2>₹{TODAY_RATES['silver']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['silver']['change']} (+{(TODAY_RATES['silver']['change']/TODAY_RATES['silver']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['silver']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    chits_df = pd.DataFrame({
        'Chit Name': ['Gold 12-Month', 'Diamond Savings'],
        'Amount': ['₹1,00,000', '₹2,00,000'],
        'Monthly': ['₹8,500', '₹10,000'],
        'Paid': ['6/12', '3/20'],
        'Remaining': ['₹25,500', '₹170,000'],
        'Status': ['✅ Active', '✅ Active']
    })

    st.subheader("Your Active Chits")
    st.dataframe(chits_df, use_container_width=True, hide_index=True)

    st.subheader("Next Payment Due")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Gold 12-Month Chit\n**Due:** Dec 15, 2025\n**Amount:** ₹8,500")
    with col2:
        st.info("Diamond Savings Chit\n**Due:** Dec 20, 2025\n**Amount:** ₹10,000")

def customer_offers_page():
    st.markdown("<h2 class='main-title'>🎁 Offers & Rewards</h2>", unsafe_allow_html=True)

    st.subheader("💰 Today's Metal Rates")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥇 Gold (Per Gram)</h3>
        <h2>₹{TODAY_RATES['gold']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['gold']['change']} (+{(TODAY_RATES['gold']['change']/TODAY_RATES['gold']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['gold']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥈 Silver (Per Gram)</h3>
        <h2>₹{TODAY_RATES['silver']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['silver']['change']} (+{(TODAY_RATES['silver']['change']/TODAY_RATES['silver']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['silver']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Your Tier: GOLD
        - Birthday Month Discount: 15%
        - Birthday Gift: ₹2,000 voucher
        - Exclusive Early Access: New collections
        - Free Maintenance: 1 item/year
        """)

    with col2:
        st.markdown("""
        ### Active Offers
        - Wedding Season Special: 15% OFF
        - Loyalty Redemption: 100 pts = ₹50
        - Referral Bonus: ₹500 per friend
        - Clearance Sale: 30% OFF selected items
        """)

def customer_summary_page():
    st.markdown("<h2 class='main-title'>📊 My Account Summary</h2>", unsafe_allow_html=True)

    st.subheader("💰 Today's Metal Rates")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥇 Gold (Per Gram)</h3>
        <h2>₹{TODAY_RATES['gold']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['gold']['change']} (+{(TODAY_RATES['gold']['change']/TODAY_RATES['gold']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['gold']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class='rate-card'>
        <h3>🥈 Silver (Per Gram)</h3>
        <h2>₹{TODAY_RATES['silver']['current']}</h2>
        <p>↑ ₹{TODAY_RATES['silver']['change']} (+{(TODAY_RATES['silver']['change']/TODAY_RATES['silver']['previous']*100):.2f}%)</p>
        <small>Previous: ₹{TODAY_RATES['silver']['previous']}</small>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Purchased", "₹89,000")
    with col2:
        st.metric("Loyalty Points", "890")
    with col3:
        st.metric("Active Chits", "2")
    with col4:
        st.metric("Customer Tier", "Gold 🥈")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Quick Links")
        if st.button("📦 Browse Items", use_container_width=True):
            st.success("Opening store catalog...")
        if st.button("💳 Apply for Chit", use_container_width=True):
            st.success("Opening chit application...")

    with col2:
        st.subheader("Recent Activity")
        activity = pd.DataFrame({
            'Date': ['Today', 'Dec 5', 'Nov 28'],
            'Activity': ['Earned 150 points', 'Purchased pendant', 'Chit payment done']
        })
        st.dataframe(activity, use_container_width=True, hide_index=True)

def customer_support_chat():
    st.markdown("<h2 class='main-title'>💬 Support Chat</h2>", unsafe_allow_html=True)

    st.markdown("Chat with our AI support assistant:")

    for message in st.session_state.customer_messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your purchases, chits, loyalty, or offers..."):
        st.session_state.customer_messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        support_responses = {
            "purchase": "📦 Your recent purchases are delivered. You earned 890 loyalty points! Use them to get discounts.",
            "chit": "💎 You have 2 active chits worth ₹3,00,000. Next payment due Dec 15.",
            "loyalty": "🎁 You're in Gold tier! Enjoy 15% birthday discount and free maintenance on 1 item/year.",
            "offer": "🎉 Active offers: 15% wedding discount, 30% clearance sale, ₹500 referral bonus!",
            "delivery": "📫 All your items are delivered. Track status in My Purchases.",
            "points": "⭐ You have 890 loyalty points. 100 points = ₹50 discount!",
            "help": "I can help with: Purchases, Chits, Loyalty, Offers, Delivery, or Points!",
            "hi": "👋 Hello! How can I assist you today?",
            "hello": "👋 Welcome to our support chat! What can I help you with?"
        }

        response = "Thank you for contacting us! How can I help you today?"
        prompt_lower = prompt.lower()

        for keyword, ans in support_responses.items():
            if keyword in prompt_lower:
                response = ans
                break

        st.session_state.customer_messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant"):
            st.markdown(f"""<div class='ai-response'>{response}</div>""", unsafe_allow_html=True)

# ============================================================================
# SETTINGS PAGE (ADMIN)
# ============================================================================

def settings_page():
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "🏪 Store", "🔔 Notifications", "📊 Logs"])

    with tab1:
        st.subheader("User Management")

        users = pd.DataFrame({
            'Username': ['manager', 'staff', 'customer', 'admin'],
            'Role': ['Manager', 'Sales Staff', 'Customer', 'Admin'],
            'Last Login': ['2025-12-11', '2025-12-11', '2025-12-11', '2025-12-11'],
            'Status': ['✅ Active', '✅ Active', '✅ Active', '✅ Active']
        })

        st.dataframe(users, use_container_width=True, hide_index=True)

    with tab2:
        st.subheader("Store Settings")
        st.text_input("Store Name", "Jewellery Shop Premium", disabled=True)
        st.text_input("Owner", "Rajesh Patel", disabled=True)
        st.text_input("GSTIN", "27ABCXYZ123", disabled=True)
        st.success("✅ All settings saved")

    with tab3:
        st.subheader("Notification Preferences")
        st.toggle("Email Alerts", value=True)
        st.toggle("SMS Alerts", value=True)
        st.toggle("Low Stock Notifications", value=True)
        st.toggle("Daily Reports", value=True)

    with tab4:
        st.subheader("System Logs")
        logs = pd.DataFrame({
            'Timestamp': ['2025-12-11 10:30', '2025-12-11 10:25', '2025-12-11 10:20'],
            'User': ['admin', 'manager', 'staff'],
            'Action': ['Logged in', 'Generated report', 'Recorded sale'],
            'Status': ['✅ Success', '✅ Success', '✅ Success']
        })
        st.dataframe(logs, use_container_width=True, hide_index=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}! ({st.session_state.user_role})</h3>", unsafe_allow_html=True)
            st.divider()

            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)

            st.divider()

            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.authenticated = False
                st.rerun()

        if st.session_state.user_role == "Manager" or st.session_state.user_role == "Admin":
            if selected_page == "📊 Dashboard":
                dashboard_page()
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
            elif selected_page == "⚙️ Settings":
                settings_page()

        elif st.session_state.user_role == "Sales Staff":
            if selected_page == "📊 Dashboard":
                dashboard_page()
            elif selected_page == "👥 Customers":
                customers_page()
            elif selected_page == "💾 Sales Record":
                sales_record_page()
            elif selected_page == "🎁 Loyalty Program":
                st.subheader("💝 Loyalty Program Info")
                st.info("Same loyalty program as customers. Earn points and help customers redeem!")
            elif selected_page == "⚡ Quick Actions":
                quick_actions_page()
            elif selected_page == "🤖 AI Assistant":
                ai_assistant_page()
            elif selected_page == "💬 Chatbot":
                chatbot_page()

        elif st.session_state.user_role == "Customer":
            if selected_page == "🛍️ My Purchases":
                customer_purchases_page()
            elif selected_page == "💎 My Chits":
                customer_chits_page()
            elif selected_page == "🎁 Offers & Rewards":
                customer_offers_page()
            elif selected_page == "📊 My Summary":
                customer_summary_page()
            elif selected_page == "💬 Support Chat":
                customer_support_chat()

if __name__ == "__main__":
    main()
