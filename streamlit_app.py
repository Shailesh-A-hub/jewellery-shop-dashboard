"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v6.0
Complete AI + BI System with Light/Dark Theme
Advanced AI Chatbot with 8 Knowledge Categories
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
# PAGE CONFIG & THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Jewellery AI Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Initialize theme
if "theme" not in st.session_state:
    st.session_state.theme = "light"

# Theme styling
LIGHT_THEME = {
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

DARK_THEME = {
    "bg_color": "#1a1a1a",
    "card_bg": "#2d2d2d",
    "text_color": "#ffffff",
    "text_secondary": "#b0b0b0",
    "border_color": "#444444",
    "primary": "#FFD700",
    "success_bg": "#1e5631",
    "warning_bg": "#663d00",
    "error_bg": "#5a1a1a",
    "info_bg": "#0d3d56"
}

theme = DARK_THEME if st.session_state.theme == "dark" else LIGHT_THEME

# Dynamic CSS Styling
st.markdown(f"""
<style>
    :root {{
        --bg-color: {theme['bg_color']};
        --card-bg: {theme['card_bg']};
        --text-color: {theme['text_color']};
        --text-secondary: {theme['text_secondary']};
        --border-color: {theme['border_color']};
        --primary: {theme['primary']};
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
        color: {theme['primary']}; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }}
    
    .metric-card {{ 
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
        padding: 20px; 
        border-radius: 10px; 
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    
    .success-box {{ 
        background-color: {theme['success_bg']}; 
        border-left: 4px solid #28a745; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}
    
    .warning-box {{ 
        background-color: {theme['warning_bg']}; 
        border-left: 4px solid #ffc107; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}
    
    .error-box {{ 
        background-color: {theme['error_bg']}; 
        border-left: 4px solid #dc3545; 
        padding: 15px; 
        border-radius: 5px;
        color: var(--text-color);
    }}
    
    .info-box {{ 
        background-color: {theme['info_bg']}; 
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
        border: 2px solid {theme['primary']};
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }}
    
    .ai-suggestion {{
        background: linear-gradient(135deg, rgba(255,215,0,0.1), rgba(255,215,0,0.05));
        border-left: 4px solid {theme['primary']};
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
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "💾 Sales Record",
            "🎁 Loyalty Program",
            "⚡ Quick Actions",
            "🤖 AI Assistant"
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
            "👨‍💼 Staff Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant",
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
        
        else:  # Admin
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
# STAFF MANAGEMENT PAGE (NEW)
# ============================================================================

def staff_management_page():
    st.markdown("<h2 class='main-title'>👨‍💼 Staff Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Staff Directory", "➕ Add Staff", "📊 Performance", "💰 Salary & Bonus"])
    
    with tab1:
        st.subheader("Staff Directory")
        
        staff_df = pd.DataFrame({
            'ID': ['S001', 'S002', 'S003', 'S004', 'S005'],
            'Name': ['Amit Verma', 'Priya Kapoor', 'Rajesh Kumar', 'Neha Singh', 'Vikram Patel'],
            'Position': ['Sales Executive', 'Sales Associate', 'Manager', 'Sales Executive', 'Cashier'],
            'Floor': ['Floor 1', 'Floor 1', 'Floor 2', 'Floor 2', 'Ground'],
            'Joining Date': ['2024-01-15', '2024-03-20', '2023-06-10', '2024-05-01', '2024-02-28'],
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
                'Staff': ['Amit Verma', 'Priya Kapoor', 'Rajesh Kumar', 'Neha Singh', 'Vikram Patel'],
                'Sales (₹)': ['12,50,000', '10,80,000', '15,60,000', '9,80,000', '8,40,000'],
                'Target': ['₹12,00,000', '₹10,00,000', '₹15,00,000', '₹9,50,000', '₹8,00,000'],
                'Achievement': ['104%', '108%', '104%', '103%', '105%']
            })
            st.dataframe(perf_df, use_container_width=True, hide_index=True)
        
        with col2:
            fig = px.bar(
                x=['Amit', 'Priya', 'Rajesh', 'Neha', 'Vikram'],
                y=[12.5, 10.8, 15.6, 9.8, 8.4],
                title="Staff Sales Performance (in Lakhs)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("💰 Salary & Bonus Management")
        
        salary_df = pd.DataFrame({
            'Staff': ['Amit Verma', 'Priya Kapoor', 'Rajesh Kumar', 'Neha Singh', 'Vikram Patel'],
            'Base Salary': ['₹25,000', '₹22,000', '₹35,000', '₹20,000', '₹18,000'],
            'Allowance': ['₹5,000', '₹4,000', '₹7,000', '₹3,500', '₹3,000'],
            'Bonus (Dec)': ['₹10,000', '₹8,500', '₹12,000', '₹7,500', '₹6,500'],
            'Total (Dec)': ['₹40,000', '₹34,500', '₹54,000', '₹31,000', '₹27,500']
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
# ADVANCED AI ASSISTANT PAGE (WITH LIGHT/DARK THEME & SMART SUGGESTIONS)
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant Pro</h2>", unsafe_allow_html=True)
    
    # AI Knowledge categories with detailed responses
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
1. 🏆 Rajesh Kumar - ₹15,60,000 (104% of target)
2. 🥈 Amit Verma - ₹12,50,000 (104% of target)
3. 🥉 Priya Kapoor - ₹10,80,000 (108% of target)

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
    
    st.subheader("💬 Chat with AI - 8 Knowledge Categories")
    
    # Quick suggestion buttons
    st.markdown("<h4>Quick Suggestions:</h4>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📦 Stock Status", use_container_width=True, key="ai_stock_btn"):
            st.session_state.ai_prompt = "Check my stock levels"
            st.rerun()
    
    with col2:
        if st.button("💰 Sales Report", use_container_width=True, key="ai_sales_btn"):
            st.session_state.ai_prompt = "Show me sales metrics"
            st.rerun()
    
    with col3:
        if st.button("👥 Customer Analytics", use_container_width=True, key="ai_cust_btn"):
            st.session_state.ai_prompt = "Analyze customers"
            st.rerun()
    
    with col4:
        if st.button("📈 Forecasting", use_container_width=True, key="ai_forecast_btn"):
            st.session_state.ai_prompt = "Predict demand"
            st.rerun()
    
    st.divider()
    
    st.markdown("""
    <div class='info-box'>
    <strong>🤖 AI Capabilities (8 Categories):</strong><br>
    📦 <strong>Stock & Inventory</strong> | 💰 <strong>Sales & Revenue</strong> | 👥 <strong>Customers</strong> | 💎 <strong>Chits</strong> | 
    👨‍💼 <strong>Staff & Team</strong> | 💵 <strong>Tax & Compliance</strong> | 📢 <strong>Campaigns</strong> | 📈 <strong>Forecasting</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant":
                st.markdown(f"""<div class='ai-response'>{message['content']}</div>""", unsafe_allow_html=True)
            else:
                st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about stock, sales, customers, chits, staff, tax, campaigns, or forecasting..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI Response with intelligent matching
        response = "Hello! I'm your AI business assistant. I understand 8 categories:\n\n📦 Stock | 💰 Sales | 👥 Customers | 💎 Chits | 👨‍💼 Staff | 💵 Tax | 📢 Campaigns | 📈 Forecasting\n\nTry asking about any of these!"
        
        keywords_map = {
            "stock": ["stock", "inventory", "items", "quantity", "reorder", "warehouse"],
            "sales": ["sales", "revenue", "income", "earnings", "performance", "turnover"],
            "customer": ["customer", "client", "buyer", "tier", "loyalty", "purchase"],
            "chit": ["chit", "collection", "member", "installment", "payout", "scheme"],
            "staff": ["staff", "employee", "sales person", "performer", "salary", "bonus"],
            "tax": ["tax", "gst", "invoice", "compliance", "filing", "audit"],
            "campaign": ["campaign", "promotion", "sale", "offer", "discount", "roi"],
            "forecast": ["forecast", "predict", "demand", "trend", "seasonal", "trend"]
        }
        
        for category, keywords in keywords_map.items():
            if any(kw in prompt.lower() for kw in keywords):
                response = ai_knowledge[category]["response"]
                break
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        with st.chat_message("assistant"):
            st.markdown(f"""<div class='ai-response'>{response}</div>""", unsafe_allow_html=True)

# ============================================================================
# CUSTOMER PORTAL PAGES
# ============================================================================

def customer_purchases_page():
    st.markdown("<h2 class='main-title'>🛍️ My Purchases</h2>", unsafe_allow_html=True)
    
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
    
    if "customer_messages" not in st.session_state:
        st.session_state.customer_messages = []
    
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
            "help": "I can help with: Purchases, Chits, Loyalty, Offers, Delivery, or Points!"
        }
        
        response = "Thank you for contacting us! How can I help you today?"
        for keyword, ans in support_responses.items():
            if keyword in prompt.lower():
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
        # Sidebar with theme toggle
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}! ({st.session_state.user_role})</h3>", unsafe_allow_html=True)
            st.divider()
            
            # Theme toggle
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Theme:**")
            with col2:
                theme_option = st.radio("", ["☀️ Light", "🌙 Dark"], horizontal=True, key="theme_radio")
                if "Light" in theme_option:
                    st.session_state.theme = "light"
                else:
                    st.session_state.theme = "dark"
            
            st.divider()
            
            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.authenticated = False
                st.rerun()
        
        # Main content routing
        if st.session_state.user_role == "Manager" or st.session_state.user_role == "Admin":
            if selected_page == "📊 Dashboard":
                dashboard_page()
            elif selected_page == "👥 Customers":
                customers_page()
            elif selected_page == "📦 Inventory":
                inventory_page()
            elif selected_page == "💰 Tax & Compliance":
                tax_compliance_page()
            elif selected_page == "👨‍💼 Staff Management":
                staff_management_page()
            elif selected_page == "⚡ Quick Actions":
                quick_actions_page()
            elif selected_page == "🤖 AI Assistant":
                ai_assistant_page()
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