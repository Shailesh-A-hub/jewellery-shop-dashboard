# ============================================================================
# 📤 STREAMLIT_APP.PY INTEGRATION - EXACT CODE TO ADD
# ============================================================================

"""
This file shows EXACTLY where and how to integrate the 4 new modules
into your existing streamlit_app.py file.

Read this carefully and follow the sections!
"""

# ============================================================================
# SECTION 1: ADD THESE IMPORTS AT THE TOP OF YOUR FILE
# ============================================================================

# AFTER your existing imports, ADD:

from auth_system import (
    render_login_page,
    render_registration_page,
    init_session_state,
    logout,
    AuthenticationSystem
)

from customer_dashboard import render_customer_dashboard

from staff_management import (
    StaffManagementSystem,
    render_staff_login,
    render_staff_dashboard
)

from bonus_system import (
    BonusManagementSystem,
    render_sales_tracking,
    render_bonus_suggestions,
    render_bonus_analytics,
    render_staff_bonus_view
)


# ============================================================================
# SECTION 2: MODIFY YOUR MAIN() FUNCTION
# ============================================================================

# CURRENT STRUCTURE (what you probably have):
"""
def main():
    # Your existing code...
    if authenticated:
        if user_role == "Manager":
            # Manager pages
        elif user_role == "Sales Staff":
            # Staff pages
"""

# NEW STRUCTURE (what to change it to):
"""
def main():
    # Initialize session
    init_session_state()
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        
        # CUSTOMER REGISTRATION/LOGIN
        if st.session_state.get('page') == 'Register':
            try:
                users_df = pd.read_csv('users.csv')
                customers_df = pd.read_csv('customers.csv')
            except FileNotFoundError:
                st.warning("Customer data files not found")
                return
            
            auth = AuthenticationSystem(users_df, customers_df)
            render_registration_page(auth)
        
        # CUSTOMER/STAFF LOGIN PAGE
        else:
            render_login_page()
    
    else:
        # USER IS AUTHENTICATED
        user_role = st.session_state.get('user_role')
        
        if user_role == 'customer':
            # ============ CUSTOMER DASHBOARD ============
            render_customer_dashboard(st.session_state.user_data)
        
        elif user_role == 'Staff':
            # ============ STAFF DASHBOARD ============
            try:
                staff_df = pd.read_csv('staff.csv')
                attendance_df = pd.read_csv('attendance.csv')
            except FileNotFoundError:
                st.error("Staff data files not found")
                return
            
            staff_mgmt = StaffManagementSystem(staff_df, attendance_df)
            render_staff_dashboard(st.session_state.user_data, staff_mgmt)
        
        elif user_role == 'Manager':
            # ============ MANAGER DASHBOARD ============
            render_manager_dashboard()
        
        else:
            st.error(f"Unknown role: {user_role}")
"""


# ============================================================================
# SECTION 3: ADD MANAGER DASHBOARD FUNCTION
# ============================================================================

def render_manager_dashboard():
    """Manager's main dashboard with all features"""
    
    st.set_page_config(
        page_title="Manager Dashboard",
        layout="wide",
        page_icon="👨‍💼"
    )
    
    # Header
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        st.title("👨‍💼 Manager Dashboard")
    
    with col3:
        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()
    
    st.divider()
    
    # Main navigation
    manager_tabs = st.tabs([
        "📊 Dashboard",
        "👥 Customers",
        "👨‍💼 Staff Management",
        "💰 Bonus & Sales",
        "📦 Inventory",
        "💎 Chits"
    ])
    
    with manager_tabs[0]:
        render_manager_summary()
    
    with manager_tabs[1]:
        render_customers_page()
    
    with manager_tabs[2]:
        render_manager_staff_management()
    
    with manager_tabs[3]:
        render_manager_bonus_management()
    
    with manager_tabs[4]:
        st.subheader("📦 Inventory Management")
        st.info("Inventory module content here")
    
    with manager_tabs[5]:
        st.subheader("💎 Chit Management")
        st.info("Chit management content here")


def render_manager_summary():
    """Manager dashboard summary"""
    st.subheader("📊 Dashboard Overview")
    
    try:
        customers_df = pd.read_csv('customers.csv')
        transactions_df = pd.read_csv('transactions.csv')
        staff_df = pd.read_csv('staff.csv')
        sales_df = pd.read_csv('sales.csv')
    except FileNotFoundError:
        st.warning("Some data files missing")
        return
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(customers_df))
    
    with col2:
        st.metric("Total Staff", len(staff_df))
    
    with col3:
        if not transactions_df.empty:
            total_sales = transactions_df['amount'].sum()
            st.metric("Total Sales", f"₹{total_sales:,.0f}")
        else:
            st.metric("Total Sales", "₹0")
    
    with col4:
        if not sales_df.empty:
            avg_daily = sales_df['daily_sales'].mean()
            st.metric("Avg Daily Sales", f"₹{avg_daily:,.0f}")
        else:
            st.metric("Avg Daily Sales", "₹0")


def render_customers_page():
    """Customer management page"""
    st.subheader("👥 Customer Management")
    
    try:
        customers_df = pd.read_csv('customers.csv')
    except FileNotFoundError:
        st.error("customers.csv not found")
        return
    
    # Display customers
    st.dataframe(customers_df, use_container_width=True)
    
    # Add customer button
    if st.button("➕ Add New Customer", use_container_width=True):
        st.info("Use customer registration feature for new customers")


def render_manager_staff_management():
    """Manager's staff management interface"""
    
    st.subheader("👨‍💼 Staff Management")
    
    try:
        staff_df = pd.read_csv('staff.csv')
        attendance_df = pd.read_csv('attendance.csv')
    except FileNotFoundError:
        st.error("Staff data files not found")
        return
    
    staff_mgmt = StaffManagementSystem(staff_df, attendance_df)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "➕ Add Staff",
        "📅 Mark Attendance",
        "📊 View Attendance",
        "💰 Salary Calculation",
        "🎉 Festival Roles"
    ])
    
    with tab1:
        st.markdown("### Add New Staff Member")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            mobile = st.text_input("Mobile (10 digits)")
            email = st.text_input("Email")
        
        with col2:
            floor = st.selectbox("Floor", ["Main Floor", "First Floor", "Second Floor"])
            role = st.selectbox("Role", ["Sales", "Customer Service", "Cashier", "Delivery"])
            salary_per_day = st.number_input("Daily Salary", value=1000, min_value=500)
        
        password = st.text_input("Password", type="password")
        
        if st.button("✅ Add Staff", use_container_width=True):
            staff_data = {
                'name': name,
                'mobile': mobile,
                'email': email,
                'floor': floor,
                'role': role,
                'salary_per_day': salary_per_day,
                'password': password
            }
            
            success, message = staff_mgmt.add_staff(staff_data)
            
            if success:
                st.success(message)
            else:
                st.error(message)
    
    with tab2:
        st.markdown("### Mark Attendance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            staff = st.selectbox(
                "Select Staff",
                options=staff_df['name'].tolist() if not staff_df.empty else []
            )
        
        with col2:
            date = st.date_input("Date")
        
        with col3:
            status = st.selectbox("Status", ["present", "absent", "leave", "half_day"])
        
        remarks = st.text_area("Remarks (optional)")
        
        if st.button("📝 Mark Attendance", use_container_width=True):
            
            # Get staff ID
            staff_row = staff_df[staff_df['name'] == staff]
            if not staff_row.empty:
                staff_id = staff_row.iloc[0]['staff_id']
                
                success, message = staff_mgmt.mark_attendance(
                    staff_id,
                    date.strftime('%Y-%m-%d'),
                    status,
                    remarks
                )
                
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    with tab3:
        st.markdown("### View Attendance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            staff = st.selectbox(
                "Select Staff",
                options=staff_df['name'].tolist() if not staff_df.empty else [],
                key="view_staff"
            )
        
        with col2:
            year = st.selectbox("Year", range(2024, 2027))
        
        with col3:
            month = st.selectbox("Month", range(1, 13), format_func=lambda x: f"{x:02d}")
        
        # Get attendance
        staff_row = staff_df[staff_df['name'] == staff]
        if not staff_row.empty:
            staff_id = staff_row.iloc[0]['staff_id']
            
            monthly = staff_mgmt.get_monthly_attendance(staff_id, year, month)
            
            if not monthly.empty:
                st.dataframe(monthly, use_container_width=True)
                
                summary = staff_mgmt.get_attendance_summary(
                    staff_id,
                    f"{year}-{month:02d}"
                )
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("✅ Present", summary['present'])
                
                with col2:
                    st.metric("❌ Absent", summary['absent'])
                
                with col3:
                    st.metric("🏥 Leave", summary['leave'])
                
                with col4:
                    st.metric("⏰ Half Day", summary['half_day'])
            else:
                st.info("No attendance records for this month")
    
    with tab4:
        st.markdown("### Salary Calculation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            staff = st.selectbox(
                "Select Staff",
                options=staff_df['name'].tolist() if not staff_df.empty else [],
                key="salary_staff"
            )
        
        with col2:
            year = st.selectbox("Year", range(2024, 2027), key="salary_year")
        
        with col3:
            month = st.selectbox("Month", range(1, 13),
                               format_func=lambda x: f"{x:02d}",
                               key="salary_month")
        
        # Calculate salary
        staff_row = staff_df[staff_df['name'] == staff]
        if not staff_row.empty:
            staff_id = staff_row.iloc[0]['staff_id']
            
            salary = staff_mgmt.calculate_salary(staff_id, year, month)
            
            if 'error' not in salary:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                        **Attendance:**
                        - Present: {salary['present_days']} days
                        - Half Days: {salary['half_days']} days
                        - Total: {salary['total_working_days']:.1f} days
                    """)
                
                with col2:
                    st.markdown(f"""
                        **Salary:**
                        - Daily Rate: ₹{salary['salary_per_day']:.2f}
                        - Base: ₹{salary['base_salary']:,.2f}
                        - Deductions: ₹{salary['deductions']:,.2f}
                        - Bonus: ₹{salary['bonus']:,.2f}
                    """)
                
                st.metric(
                    "💰 Net Salary",
                    f"₹{salary['net_salary']:,.2f}",
                    delta=f"{salary['present_days']} days"
                )
    
    with tab5:
        st.markdown("### Festival Role Suggestions")
        
        suggestions = staff_mgmt.suggest_festival_roles()
        
        if suggestions['festival']:
            st.info(f"🎉 Current Festival: **{suggestions['festival'].upper()}**")
            
            if suggestions['suggestions']:
                st.markdown("#### Suggested Staff")
                
                for sugg in suggestions['suggestions']:
                    col1, col2, col3 = st.columns([2, 2, 2])
                    
                    with col1:
                        st.write(f"**{sugg['name']}**")
                        st.caption(f"Current: {sugg['current_role']}")
                    
                    with col2:
                        st.write(f"**Suggested Roles:**")
                        for role in sugg['suggested_roles']:
                            st.caption(f"✅ {role}")
                    
                    with col3:
                        st.write(f"**Attendance:** {sugg['attendance_score']}")
                        st.caption(f"Floor: {sugg['priority_floor']}")
            else:
                st.info("No staff meet the attendance criteria for festival roles")
        else:
            st.info("No current festival period")


def render_manager_bonus_management():
    """Manager's bonus & sales management"""
    
    st.subheader("💰 Bonus & Sales Management")
    
    try:
        staff_df = pd.read_csv('staff.csv')
        sales_df = pd.read_csv('sales.csv')
    except FileNotFoundError:
        st.warning("Creating new data files...")
        staff_df = pd.DataFrame()
        sales_df = pd.DataFrame()
    
    bonus_mgmt = BonusManagementSystem(sales_df, staff_df)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📊 Record Sales",
        "🤖 Bonus Suggestions",
        "📈 Analytics"
    ])
    
    with tab1:
        render_sales_tracking(bonus_mgmt)
    
    with tab2:
        render_bonus_suggestions(bonus_mgmt)
    
    with tab3:
        render_bonus_analytics(bonus_mgmt)


# ============================================================================
# SECTION 4: YOUR main() FUNCTION SHOULD LOOK LIKE THIS
# ============================================================================

def main():
    """Main application"""
    
    # Initialize session
    init_session_state()
    
    # Check authentication
    if not st.session_state.get('authenticated', False):
        
        # Customer registration/login
        if st.session_state.get('page') == 'Register':
            try:
                users_df = pd.read_csv('users.csv')
                customers_df = pd.read_csv('customers.csv')
            except FileNotFoundError:
                st.warning("Data files not found. Creating...")
                users_df = pd.DataFrame()
                customers_df = pd.DataFrame()
            
            auth = AuthenticationSystem(users_df, customers_df)
            render_registration_page(auth)
        
        else:
            render_login_page()
    
    else:
        # User authenticated
        user_role = st.session_state.get('user_role')
        
        if user_role == 'customer':
            # Customer dashboard
            render_customer_dashboard(st.session_state.user_data)
        
        elif user_role == 'Staff':
            # Staff dashboard
            try:
                staff_df = pd.read_csv('staff.csv')
                attendance_df = pd.read_csv('attendance.csv')
            except FileNotFoundError:
                st.error("Staff data files not found")
                return
            
            staff_mgmt = StaffManagementSystem(staff_df, attendance_df)
            render_staff_dashboard(st.session_state.user_data, staff_mgmt)
        
        elif user_role == 'Manager':
            # Manager dashboard
            render_manager_dashboard()
        
        else:
            st.error(f"Unknown role: {user_role}")


# ============================================================================
# SECTION 5: REPLACE YOUR if __name__ == "__main__": BLOCK WITH THIS
# ============================================================================

if __name__ == "__main__":
    main()


# ============================================================================
# THAT'S IT!
# ============================================================================

# Your app now has:
# ✅ Customer portal (registration, login, dashboard)
# ✅ Staff management (attendance, salary, performance)
# ✅ Manager dashboard (customers, staff, bonuses)
# ✅ AI bonus system (sales-based bonuses)
# ✅ Festival role suggestions
# ✅ All integrated together!

# Test with:
# streamlit run streamlit_app.py
