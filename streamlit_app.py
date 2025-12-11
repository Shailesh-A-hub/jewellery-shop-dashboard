import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user_role' not in st.session_state:
        st.session_state.user_role = None
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    if 'page' not in st.session_state:
        st.session_state.page = 'Login'


# ============================================================================
# LOGIN PAGE
# ============================================================================

def render_login_page():
    """Render login page"""
    st.set_page_config(page_title="Jewelry Management - Login", layout="centered")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.title("💎 Jewelry Shop")
        st.markdown("### Management System")
        st.divider()
        
        login_type = st.radio("Login As:", ["Manager", "Staff", "Customer"], horizontal=True)
        
        if login_type == "Manager":
            st.subheader("👨‍💼 Manager Login")
            username = st.text_input("Username", key="manager_user")
            password = st.text_input("Password", type="password", key="manager_pass")
            
            if st.button("🔓 Login", use_container_width=True):
                # Hardcoded manager credentials
                if username == "manager_user" and password == "manager123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Manager"
                    st.session_state.user_data = {"name": "Manager", "id": "MGR001"}
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        elif login_type == "Staff":
            st.subheader("👨‍💼 Staff Login")
            username = st.text_input("Username", key="staff_user")
            password = st.text_input("Password", type="password", key="staff_pass")
            
            if st.button("🔓 Login", use_container_width=True):
                # Hardcoded staff credentials
                if username == "RAJESH_2001" and password == "staff123":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Staff"
                    st.session_state.user_data = {"name": "Rajesh", "id": "STF001"}
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials")
        
        else:  # Customer
            st.subheader("👤 Customer Login")
            mobile = st.text_input("Mobile Number", key="customer_mobile")
            otp = st.text_input("OTP", key="customer_otp")
            
            if st.button("🔓 Login", use_container_width=True):
                # Hardcoded customer credentials
                if mobile == "9876543200" and otp == "3200":
                    st.session_state.authenticated = True
                    st.session_state.user_role = "Customer"
                    st.session_state.user_data = {"name": "Rajesh Patel", "mobile": mobile}
                    st.success("✅ Login Successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid mobile or OTP")


# ============================================================================
# MANAGER DASHBOARD
# ============================================================================

def render_manager_dashboard():
    """Manager Dashboard"""
    st.set_page_config(page_title="Manager Dashboard", layout="wide", page_icon="👨‍💼")
    
    # Header with logout
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        st.title("👨‍💼 Manager Dashboard")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    # Navigation tabs
    tabs = st.tabs([
        "📊 Dashboard",
        "👥 Customers",
        "👨‍💼 Staff",
        "💰 Bonus & Sales",
        "📦 Inventory",
        "💎 Chits"
    ])
    
    # Tab 1: Dashboard Overview
    with tabs[0]:
        st.subheader("📊 Dashboard Overview")
        
        try:
            customers_df = pd.read_csv('customers.csv')
            staff_df = pd.read_csv('staff.csv')
            sales_df = pd.read_csv('sales.csv')
            transactions_df = pd.read_csv('transactions.csv')
        except FileNotFoundError:
            customers_df = pd.DataFrame()
            staff_df = pd.DataFrame()
            sales_df = pd.DataFrame()
            transactions_df = pd.DataFrame()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("👥 Total Customers", len(customers_df) if not customers_df.empty else 0)
        with col2:
            st.metric("👨‍💼 Total Staff", len(staff_df) if not staff_df.empty else 0)
        with col3:
            if not sales_df.empty:
                total = sales_df['daily_sales'].sum()
                st.metric("💰 Total Sales", f"₹{total:,.0f}")
            else:
                st.metric("💰 Total Sales", "₹0")
        with col4:
            if not transactions_df.empty:
                count = len(transactions_df)
                st.metric("📈 Total Transactions", count)
            else:
                st.metric("📈 Total Transactions", 0)
        
        st.divider()
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Sales Trend")
            if not sales_df.empty and len(sales_df) > 0:
                try:
                    st.line_chart(sales_df.set_index('date')['daily_sales'].tail(30))
                except:
                    st.info("Sales chart data not available")
            else:
                st.info("No sales data available")
        
        with col2:
            st.markdown("#### Customer Tiers")
            if not customers_df.empty:
                try:
                    tier_counts = customers_df['tier'].value_counts()
                    st.bar_chart(tier_counts)
                except:
                    st.info("Customer tier data not available")
            else:
                st.info("No customer data available")
    
    # Tab 2: Customer Management
    with tabs[1]:
        st.subheader("👥 Customer Management")
        
        try:
            customers_df = pd.read_csv('customers.csv')
            if not customers_df.empty:
                st.dataframe(customers_df, use_container_width=True)
            else:
                st.info("No customers found")
        except FileNotFoundError:
            st.error("customers.csv not found")
    
    # Tab 3: Staff Management
    with tabs[2]:
        st.subheader("👨‍💼 Staff Management")
        
        try:
            staff_df = pd.read_csv('staff.csv')
            if not staff_df.empty:
                st.dataframe(staff_df, use_container_width=True)
            else:
                st.info("No staff found")
        except FileNotFoundError:
            st.error("staff.csv not found")
        
        st.divider()
        st.markdown("### Add New Staff Member")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Name")
            mobile = st.text_input("Mobile (10 digits)")
            email = st.text_input("Email")
        with col2:
            floor = st.selectbox("Floor", ["Main Floor", "First Floor", "Second Floor"])
            role = st.selectbox("Role", ["Sales", "Customer Service", "Cashier", "Delivery"])
            salary = st.number_input("Daily Salary (₹)", value=1000, min_value=500)
        
        if st.button("✅ Add Staff", use_container_width=True):
            st.success("✅ Staff member added successfully!")
    
    # Tab 4: Bonus & Sales
    with tabs[3]:
        st.subheader("💰 Bonus & Sales Management")
        
        sub_tabs = st.tabs(["📊 Record Sales", "🤖 Suggestions", "📈 Analytics"])
        
        with sub_tabs[0]:
            st.markdown("### Record Daily Sales")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                sales_date = st.date_input("Date", key="sales_date_1")
            with col2:
                daily_sales = st.number_input("Daily Sales (₹)", value=100000, min_value=0, key="daily_sales_1")
            with col3:
                staff_count = st.number_input("Staff Count", value=3, min_value=1, key="staff_count_1")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                gold = st.number_input("Gold Sales (₹)", value=50000, min_value=0, key="gold_1")
            with col2:
                silver = st.number_input("Silver Sales (₹)", value=30000, min_value=0, key="silver_1")
            with col3:
                diamond = st.number_input("Diamond Sales (₹)", value=20000, min_value=0, key="diamond_1")
            
            if st.button("💾 Save Sales Data", use_container_width=True):
                st.success("✅ Sales data saved successfully!")
        
        with sub_tabs[1]:
            st.markdown("### Bonus Suggestions")
            st.info("Based on sales performance, here are bonus recommendations:")
            
            # Dummy suggestions
            suggestions = [
                {"name": "Rajesh Patel", "sales": 150000, "bonus": 12000, "eligible": True},
                {"name": "Priya Singh", "sales": 120000, "bonus": 9600, "eligible": True},
                {"name": "Amit Kumar", "sales": 180000, "bonus": 14400, "eligible": True},
            ]
            
            for sugg in suggestions:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.write(f"**{sugg['name']}**")
                with col2:
                    st.write(f"Sales: ₹{sugg['sales']:,}")
                with col3:
                    st.write(f"Bonus: ₹{sugg['bonus']:,.0f}")
                with col4:
                    st.write("✅ Eligible" if sugg['eligible'] else "⏳ Not Yet")
        
        with sub_tabs[2]:
            st.markdown("### Sales Analytics")
            try:
                sales_df = pd.read_csv('sales.csv')
                if not sales_df.empty:
                    st.line_chart(sales_df.set_index('date')['daily_sales'])
                else:
                    st.info("No sales data available")
            except FileNotFoundError:
                st.info("sales.csv not found")
    
    # Tab 5: Inventory
    with tabs[4]:
        st.subheader("📦 Inventory Management")
        st.info("🔧 Inventory management module coming soon...")
    
    # Tab 6: Chits
    with tabs[5]:
        st.subheader("💎 Chit Management")
        st.info("🔧 Chit management module coming soon...")


# ============================================================================
# STAFF DASHBOARD
# ============================================================================

def render_staff_dashboard():
    """Staff Dashboard"""
    st.set_page_config(page_title="Staff Dashboard", layout="wide", page_icon="👨‍💼")
    
    # Header with logout
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        st.title(f"👨‍💼 Welcome, {st.session_state.user_data.get('name', 'Staff')}")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    tabs = st.tabs(["📊 Dashboard", "📅 Attendance", "💰 Salary", "🎉 Performance"])
    
    with tabs[0]:
        st.subheader("📊 My Dashboard")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("✅ Present Days", "22")
        with col2:
            st.metric("❌ Absent Days", "2")
        with col3:
            st.metric("🏥 Leave Days", "1")
    
    with tabs[1]:
        st.subheader("📅 Attendance Tracking")
        try:
            attendance_df = pd.read_csv('attendance.csv')
            st.dataframe(attendance_df.head(10), use_container_width=True)
        except FileNotFoundError:
            st.info("No attendance data available")
    
    with tabs[2]:
        st.subheader("💰 Salary Information")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Monthly Salary", "₹25,000")
        with col2:
            st.metric("Bonus This Month", "₹3,500")
    
    with tabs[3]:
        st.subheader("🎉 Performance Metrics")
        st.info("Performance tracking coming soon...")


# ============================================================================
# CUSTOMER DASHBOARD
# ============================================================================

def render_customer_dashboard():
    """Customer Dashboard"""
    st.set_page_config(page_title="Customer Dashboard", layout="wide", page_icon="💎")
    
    # Header with logout
    col1, col2, col3 = st.columns([3, 3, 1])
    with col1:
        st.title(f"💎 Welcome, {st.session_state.user_data.get('name', 'Customer')}")
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    tabs = st.tabs(["🛍️ Purchases", "💍 Chits", "🎁 Offers", "📊 Summary"])
    
    with tabs[0]:
        st.subheader("🛍️ Your Purchases")
        st.info("You have made 12 purchases worth ₹1,45,000")
        
        # Dummy purchase data
        purchases = {
            "Date": ["2025-12-01", "2025-11-15", "2025-11-01"],
            "Item": ["Gold Ring", "Diamond Necklace", "Silver Bracelet"],
            "Amount": ["₹25,000", "₹85,000", "₹15,000"],
            "Status": ["Delivered", "Delivered", "Delivered"]
        }
        st.dataframe(pd.DataFrame(purchases), use_container_width=True)
    
    with tabs[1]:
        st.subheader("💍 My Chits")
        st.info("Active Chits: 2")
        
        # Dummy chit data
        chits = {
            "Chit Name": ["Gold 12-Month", "Silver 6-Month"],
            "Total Value": ["₹1,00,000", "₹50,000"],
            "Installment": ["₹8,500", "₹8,500"],
            "Status": ["Active", "Active"]
        }
        st.dataframe(pd.DataFrame(chits), use_container_width=True)
    
    with tabs[2]:
        st.subheader("🎁 Current Offers")
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("**🎉 Discount: 15% Off on Gold**\nValid till: Dec 31, 2025")
        with col2:
            st.info("**💝 Free Gifts**\nOn purchases above ₹50,000")
    
    with tabs[3]:
        st.subheader("📊 Your Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Spent", "₹1,45,000")
        with col2:
            st.metric("Tier Status", "Gold")
        with col3:
            st.metric("Loyalty Points", "1,450")
        with col4:
            st.metric("Active Chits", "2")


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main Application Entry Point"""
    
    # Initialize session state
    init_session_state()
    
    # Route to appropriate page
    if not st.session_state.authenticated:
        render_login_page()
    else:
        user_role = st.session_state.user_role
        
        if user_role == "Manager":
            render_manager_dashboard()
        elif user_role == "Staff":
            render_staff_dashboard()
        elif user_role == "Customer":
            render_customer_dashboard()
        else:
            st.error("Unknown user role")


if __name__ == "__main__":
    main()
