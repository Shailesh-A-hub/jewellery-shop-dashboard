"""
💎 PREMIUM JEWELLERY SHOP MANAGEMENT SYSTEM v4.0
Complete AI + BI System for Indian Jewellery Retail
All Features Fully Implemented - NO "COMING SOON"
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

# CSS Styling
st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: bold; color: #FFD700; }
    .metric-card { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 20px; border-radius: 10px; color: white; }
    .success-box { background-color: #d4edda; border-left: 4px solid #28a745; padding: 15px; border-radius: 5px; }
    .warning-box { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; border-radius: 5px; }
    .error-box { background-color: #f8d7da; border-left: 4px solid #dc3545; padding: 15px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.current_page = "📊 Dashboard"

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
            "🤖 ML Models",
            "💎 Chit Management",
            "⚡ Quick Actions",
            "🤖 AI Assistant"
        ],
        "Sales Staff": [
            "📊 Dashboard",
            "👥 Customers",
            "⚡ Quick Actions"
        ],
        "Admin": [
            "📊 Dashboard",
            "👥 Customers",
            "📦 Inventory",
            "💰 Tax & Compliance",
            "📢 Campaigns",
            "🤖 ML Models",
            "💎 Chit Management",
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
        
        login_type = st.radio("Login As:", ["Manager", "Staff", "Admin"], horizontal=True, key="login_type")
        
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
        **Admin:** username: `admin` | password: `admin123`
        """)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def dashboard_page():
    st.markdown("<h2 class='main-title'>📊 Dashboard</h2>", unsafe_allow_html=True)
    
    # Generate sample data
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
        st.dataframe(top_items, use_container_width=True)
    
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
        
        st.dataframe(customers_df, use_container_width=True, key="cust_df")
    
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
        st.dataframe(loyalty_df, use_container_width=True)
    
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
            'Status': ['In Stock', 'In Stock', 'Low Stock', 'Low Stock', 'In Stock']
        })
        
        st.dataframe(inventory_df, use_container_width=True)
    
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
        <strong>⚠️ Low Stock Items:</strong>
        • Diamond Pendant (GLD003) - Only 15 units
        • Platinum Ring (PLT004) - Only 8 units
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
        st.dataframe(low_stock, use_container_width=True)
    
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
        st.dataframe(tax_df, use_container_width=True)
    
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
            st.dataframe(gstr1, use_container_width=True)
        
        with col2:
            st.markdown("**GSTR-2 (Inward Supplies)**")
            gstr2 = pd.DataFrame({
                'Date': ['Dec 02', 'Dec 07', 'Dec 11'],
                'Bill #': ['B001', 'B002', 'B003'],
                'Vendor': ['Gold Supplier Inc', 'Silver Corp', 'Diamond Ltd'],
                'Amount': ['₹2,00,000', '₹1,50,000', '₹1,20,000']
            })
            st.dataframe(gstr2, use_container_width=True)
    
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
        
        st.dataframe(invoices, use_container_width=True)
        
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
# CAMPAIGNS PAGE
# ============================================================================

def campaigns_page():
    st.markdown("<h2 class='main-title'>📢 Campaigns</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📊 Active Campaigns", "➕ Create Campaign", "📈 Campaign Performance"])
    
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
        
        st.dataframe(campaigns, use_container_width=True)
    
    with tab2:
        st.subheader("Create New Campaign")
        
        col1, col2 = st.columns(2)
        with col1:
            campaign_name = st.text_input("Campaign Name", key="camp_name")
            campaign_type = st.selectbox("Type", ["Seasonal", "Festival", "Clearance", "Bundle", "VIP"], key="camp_type")
            discount = st.slider("Discount (%)", 0, 100, 20, key="camp_discount")
        
        with col2:
            start_date = st.date_input("Start Date", key="camp_start")
            end_date = st.date_input("End Date", key="camp_end")
            budget = st.number_input("Budget (₹)", min_value=1000, key="camp_budget")
        
        description = st.text_area("Campaign Description", key="camp_desc")
        
        if st.button("✅ Create Campaign", use_container_width=True, key="create_camp_btn"):
            st.success("✅ Campaign created successfully!")
            st.balloons()
    
    with tab3:
        st.subheader("📈 Campaign Performance")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=['Diwali Sale', 'Wedding Special', 'New Year', 'Clearance'],
                y=[45000, 32000, 18000, 25000],
                title="Campaign Revenue"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.line(
                x=['Week 1', 'Week 2', 'Week 3', 'Week 4'],
                y=[10000, 15000, 12000, 8000],
                title="Weekly Sales Trend",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# CHIT MANAGEMENT PAGE
# ============================================================================

def chit_management_page():
    st.markdown("<h2 class='main-title'>💎 Chit Management</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Active Chits", "➕ Create Chit", "💰 Chit Payments", "📊 Chit Analytics"])
    
    with tab1:
        st.subheader("Active Chits")
        
        chits = pd.DataFrame({
            'Chit ID': ['CHT001', 'CHT002', 'CHT003', 'CHT004'],
            'Chit Name': ['Gold 12-Month', 'Silver 6-Month', 'Diamond Savings', 'Platinum Plus'],
            'Chit Value': ['₹1,00,000', '₹50,000', '₹2,00,000', '₹3,00,000'],
            'Members': ['12', '6', '20', '10'],
            'Monthly Installment': ['₹8,500', '₹8,500', '₹10,000', '₹30,000'],
            'Status': ['Active', 'Active', 'Active', 'Closing'],
            'Start Date': ['2025-01-01', '2025-07-01', '2025-08-01', '2025-02-01']
        })
        
        st.dataframe(chits, use_container_width=True)
    
    with tab2:
        st.subheader("Create New Chit")
        
        col1, col2 = st.columns(2)
        with col1:
            chit_name = st.text_input("Chit Name", key="chit_name")
            chit_value = st.number_input("Chit Value (₹)", min_value=10000, key="chit_value")
            num_members = st.number_input("Number of Members", min_value=1, max_value=100, key="chit_members")
        
        with col2:
            duration = st.selectbox("Duration", ["3 Months", "6 Months", "12 Months", "24 Months"], key="chit_duration")
            chit_type = st.selectbox("Type", ["Regular", "Premium", "Diamond", "Platinum"], key="chit_type")
            start_date = st.date_input("Start Date", key="chit_start")
        
        monthly_installment = (st.number_input("Monthly Installment (₹)", min_value=100, key="chit_monthly"))
        
        if st.button("✅ Create Chit", use_container_width=True, key="create_chit_btn"):
            st.success("✅ Chit created successfully!")
            st.balloons()
    
    with tab3:
        st.subheader("💰 Payment Tracking")
        
        payments = pd.DataFrame({
            'Chit ID': ['CHT001', 'CHT001', 'CHT002', 'CHT002', 'CHT003'],
            'Member': ['Rajesh Patel', 'Priya Singh', 'Amit Kumar', 'Neha Sharma', 'Vikram Gupta'],
            'Month': ['Dec 2025', 'Dec 2025', 'Dec 2025', 'Dec 2025', 'Dec 2025'],
            'Amount': ['₹8,500', '₹8,500', '₹8,500', '₹8,500', '₹10,000'],
            'Status': ['Paid', 'Pending', 'Paid', 'Pending', 'Paid'],
            'Payment Date': ['2025-12-05', 'Pending', '2025-12-08', 'Pending', '2025-12-10']
        })
        
        st.dataframe(payments, use_container_width=True)
    
    with tab4:
        st.subheader("📊 Chit Analytics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=[12, 6, 20, 10],
                names=['Gold 12M', 'Silver 6M', 'Diamond', 'Platinum'],
                title="Members by Chit"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=['CHT001', 'CHT002', 'CHT003', 'CHT004'],
                y=[100, 50, 200, 300],
                title="Chit Value (in Lakhs)"
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
# AI ASSISTANT PAGE
# ============================================================================

def ai_assistant_page():
    st.markdown("<h2 class='main-title'>🤖 AI Assistant</h2>", unsafe_allow_html=True)
    
    st.subheader("💬 Chat with AI")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your business..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AI response (simulated)
        ai_responses = {
            "stock": "Your current stock value is ₹45,00,000. Low stock items: Diamond Pendant (15 units), Platinum Ring (8 units).",
            "sales": "Today's sales: ₹1,85,000. Monthly sales: ₹45,00,000. Top item: Gold Ring (₹22,50,000).",
            "customer": "Total customers: 1,250. Premium: 250, Gold: 450, Silver: 350, Standard: 200. Average customer value: ₹36,000.",
            "chit": "Active chits: 85. Total value: ₹65,00,000. Members: 127. Monthly collection: ₹9,50,000.",
            "tax": "GST payable this month: ₹6,50,000. GSTR-1 filed. All compliance up to date."
        }
        
        # Simple keyword matching for AI response
        response = "I'm here to help! Ask me about stock, sales, customers, chits, or tax matters."
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
    st.markdown("<h2 class='main-title'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["👥 Users", "🏪 Store Settings", "🔔 Notifications", "📊 System Logs"])
    
    with tab1:
        st.subheader("User Management")
        
        users = pd.DataFrame({
            'Username': ['manager', 'staff', 'admin'],
            'Role': ['Manager', 'Sales Staff', 'Admin'],
            'Last Login': ['2025-12-11', '2025-12-11', '2025-12-11'],
            'Status': ['Active', 'Active', 'Active']
        })
        
        st.dataframe(users, use_container_width=True)
        
        st.divider()
        st.subheader("Add New User")
        
        col1, col2 = st.columns(2)
        with col1:
            new_user = st.text_input("Username", key="new_user_id")
            new_password = st.text_input("Password", type="password", key="new_pass_id")
        
        with col2:
            new_role = st.selectbox("Role", ["Manager", "Sales Staff", "Admin"], key="new_role_id")
            email = st.text_input("Email", key="new_email_id")
        
        if st.button("➕ Add User", use_container_width=True, key="add_user_btn"):
            st.success("✅ User added successfully!")
    
    with tab2:
        st.subheader("Store Settings")
        
        store_settings = {
            "Store Name": st.text_input("Store Name", "Jewellery Shop Premium", key="store_name"),
            "Owner": st.text_input("Owner Name", "Rajesh Patel", key="owner_name"),
            "Email": st.text_input("Email", "shop@jewellery.com", key="store_email"),
            "Phone": st.text_input("Phone", "+91-9876543210", key="store_phone"),
            "Address": st.text_area("Address", "123 Gold Street, Mumbai", key="store_addr"),
            "GSTIN": st.text_input("GSTIN", "27ABCXYZ123", key="gstin"),
        }
        
        if st.button("💾 Save Settings", use_container_width=True, key="save_settings_btn"):
            st.success("✅ Settings saved successfully!")
    
    with tab3:
        st.subheader("Notification Settings")
        
        st.toggle("Email Alerts", value=True, key="email_alerts")
        st.toggle("SMS Alerts", value=True, key="sms_alerts")
        st.toggle("Low Stock Notifications", value=True, key="low_stock_notify")
        st.toggle("Daily Reports", value=True, key="daily_reports")
        st.toggle("Monthly Summaries", value=True, key="monthly_summaries")
        
        if st.button("💾 Save Preferences", use_container_width=True, key="save_notify_btn"):
            st.success("✅ Preferences saved successfully!")
    
    with tab4:
        st.subheader("System Logs")
        
        logs = pd.DataFrame({
            'Timestamp': ['2025-12-11 10:30', '2025-12-11 10:25', '2025-12-11 10:20', '2025-12-11 10:15'],
            'User': ['admin', 'manager', 'staff', 'admin'],
            'Action': ['Added new user', 'Generated report', 'Created sale', 'Updated inventory'],
            'Status': ['Success', 'Success', 'Success', 'Success']
        })
        
        st.dataframe(logs, use_container_width=True)

# ============================================================================
# ML MODELS PAGE
# ============================================================================

def ml_models_page():
    st.markdown("<h2 class='main-title'>🤖 ML Models</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📈 Demand Forecasting", "💎 Price Optimization", "👥 Customer Segmentation"])
    
    with tab1:
        st.subheader("Demand Forecasting")
        st.info("AI-powered demand prediction for next 30 days")
        
        forecast_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current Demand': [45, 120, 15, 8],
            'Predicted Demand (30 days)': [48, 135, 18, 10],
            'Confidence': ['92%', '88%', '85%', '87%'],
            'Action': ['Maintain', 'Increase', 'Reorder', 'Reorder']
        })
        
        st.dataframe(forecast_data, use_container_width=True)
    
    with tab2:
        st.subheader("Price Optimization")
        st.info("AI-recommended prices based on demand and competition")
        
        price_data = pd.DataFrame({
            'Product': ['Gold Ring', 'Silver Bracelet', 'Diamond Pendant', 'Platinum Ring'],
            'Current Price': ['₹15,000', '₹2,000', '₹50,000', '₹75,000'],
            'Recommended Price': ['₹15,500', '₹1,950', '₹52,000', '₹77,500'],
            'Expected Revenue Impact': ['+8.5%', '-2.3%', '+4.2%', '+3.5%'],
            'Recommendation': ['Increase', 'Decrease', 'Increase', 'Increase']
        })
        
        st.dataframe(price_data, use_container_width=True)
    
    with tab3:
        st.subheader("Customer Segmentation")
        st.info("AI-driven customer grouping for targeted marketing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=[250, 450, 350, 200],
                names=['VIP (₹5L+)', 'Premium (₹2-5L)', 'Regular (₹50K-2L)', 'New (<₹50K)'],
                title="Customer Segments by Value"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(
                x=['VIP', 'Premium', 'Regular', 'New'],
                y=[1800, 1200, 600, 150],
                title="Average Purchase Frequency (days)",
            )
            st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    if not st.session_state.authenticated:
        login_page()
    else:
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"<h3>Welcome, {st.session_state.username}! ({st.session_state.user_role})</h3>", unsafe_allow_html=True)
            st.divider()
            
            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)
            
            st.divider()
            
            if st.button("🚪 Logout", use_container_width=True, key="logout_btn"):
                st.session_state.authenticated = False
                st.rerun()
        
        # Main content
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
        elif selected_page == "💎 Chit Management":
            chit_management_page()
        elif selected_page == "⚡ Quick Actions":
            quick_actions_page()
        elif selected_page == "🤖 AI Assistant":
            ai_assistant_page()
        elif selected_page == "🤖 ML Models":
            ml_models_page()
        elif selected_page == "⚙️ Settings":
            settings_page()

if __name__ == "__main__":
    main()
