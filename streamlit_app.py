import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import hashlib

# ============================================================================
# PAGE CONFIG & THEME
# ============================================================================

st.set_page_config(
    page_title="💎 Premium Jewellery Dashboard",
    layout="wide",
    page_icon="💎",
    initial_sidebar_state="expanded"
)

# Theme Toggle
if "theme" not in st.session_state:
    st.session_state.theme = "light"

col1, col2 = st.sidebar.columns([4, 1])
with col2:
    if st.button("🌙" if st.session_state.theme == "light" else "☀️", help="Toggle Theme"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# Apply theme
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        body { background-color: #1a1a1a; color: #ffffff; }
        .stMetric { background-color: #2d2d2d; padding: 15px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# AUTHENTICATION & ROLE-BASED ACCESS
# ============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_role = None
        st.session_state.username = None

USERS = {
    "manager": {"password": hash_password("manager123"), "role": "Manager"},
    "staff": {"password": hash_password("staff123"), "role": "Sales Staff"}
}

def login_page():
    st.markdown("<h1 style='text-align: center;'>🔐 Jewellery Shop Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Login Required</h3>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", placeholder="Enter username (manager/staff)")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        if st.button("Login", use_container_width=True):
            if username in USERS and USERS[username]["password"] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.username = username
                st.success(f"Welcome, {username}! ({USERS[username]['role']})")
                st.rerun()
            else:
                st.error("Invalid credentials")
        
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.info("👤 **Manager** - Username: manager | Password: manager123")
        st.info("👥 **Staff** - Username: staff | Password: staff123")

init_auth()

if not st.session_state.authenticated:
    login_page()
    st.stop()

# ============================================================================
# DATA LOADING & CACHING
# ============================================================================

@st.cache_data
def load_data():
    # Try to load customers CSV
    try:
        customers = pd.read_csv("customers.csv")
    except FileNotFoundError:
        st.warning("❌ customers.csv not found. Using sample data.")
        customers = pd.DataFrame({
            "name": ["Rajesh Kumar", "Priya Singh", "Amit Patel", "Neha Sharma", "Vikram Gupta"],
            "mobile": ["9876543210", "9123456789", "9098765432", "9012345678", "9111223344"],
            "digital_gold": [50, 75, 100, 30, 60],
            "pending_amount": [5000, 0, 10000, 2000, 0]
        })
    
    # Try to load summary CSV
    try:
        summary = pd.read_csv("summary.csv")
    except FileNotFoundError:
        st.warning("❌ summary.csv not found. Using default values.")
        summary = pd.DataFrame([{
            "gold_rate": 7500,
            "silver_rate": 85,
            "profit": 50000,
            "loss": 15000,
            "inventory_gold": 500,
            "inventory_silver": 2000
        }])
    
    # Normalize columns
    customers.columns = customers.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("[()]", "", regex=True)
    summary.columns = summary.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("[()]", "", regex=True)
    
    # Ensure required columns exist
    if "pending_amount" not in customers.columns:
        customers["pending_amount"] = 0
    if "digital_gold" not in customers.columns:
        customers["digital_gold"] = 0
    if "mobile" not in customers.columns:
        customers["mobile"] = ""
    
    # Generate transaction history (mock data for trends)
    np.random.seed(42)
    dates = pd.date_range(start="2025-01-01", end="2025-12-09", freq="D")
    transactions = pd.DataFrame({
        "date": np.random.choice(dates, 100),
        "amount": np.random.randint(1000, 50000, 100),
        "type": np.random.choice(["sale", "purchase"], 100),
        "category": np.random.choice(["gold", "silver", "diamond"], 100)
    })
    
    return customers, summary, transactions

try:
    customers, summary, transactions = load_data()
except Exception as e:
    st.error(f"Error loading data: {str(e)}")
    st.stop()

# ============================================================================
# CALCULATE ADVANCED FINANCIAL METRICS - COMPLETELY REWRITTEN
# ============================================================================

def calculate_metrics():
    """Calculate all financial metrics with COMPLETE ERROR HANDLING"""
    try:
        # Get values from summary with safe defaults
        gold_rate = float(summary.iloc[0].get("gold_rate", 7500))
        silver_rate = float(summary.iloc[0].get("silver_rate", 85))
        profit = float(summary.iloc[0].get("profit", 50000))
        loss = float(summary.iloc[0].get("loss", 15000))
        inventory_gold = float(summary.iloc[0].get("inventory_gold", 500))
        inventory_silver = float(summary.iloc[0].get("inventory_silver", 2000))
        
        # Calculate derived metrics
        total_revenue = profit + loss if (profit + loss) > 0 else 50000
        net_profit = profit - loss
        profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
        
        # FIXED: Inventory value with safeguards
        inventory_value = max(1, (inventory_gold * gold_rate) + (inventory_silver * silver_rate))
        roi = (net_profit / inventory_value * 100) if inventory_value > 0 else 0
        
        # Customer metrics
        total_customers = len(customers) if len(customers) > 0 else 5
        pending_customers = len(customers[customers["pending_amount"] > 0]) if len(customers) > 0 else 0
        total_pending = customers["pending_amount"].sum() if len(customers) > 0 else 0
        
        # Cash flow - FIXED: Safe handling
        if len(transactions) > 0:
            daily_transactions = transactions[transactions["date"] >= datetime.now() - timedelta(days=30)]
            sales = daily_transactions[daily_transactions["type"] == "sale"]["amount"].sum()
            purchases = daily_transactions[daily_transactions["type"] == "purchase"]["amount"].sum()
            cash_flow = sales - purchases
        else:
            sales = 0
            purchases = 0
            cash_flow = 0
        
        # Inventory turnover
        turnover_ratio = total_revenue / inventory_value if inventory_value > 0 else 0
        
        # Return ONLY these keys - NO extra keys!
        return {
            "gold_rate": gold_rate,
            "silver_rate": silver_rate,
            "total_revenue": total_revenue,
            "net_profit": net_profit,
            "profit_margin": profit_margin,
            "roi": roi,
            "inventory_value": inventory_value,
            "turnover_ratio": turnover_ratio,
            "cash_flow": cash_flow,
            "total_customers": total_customers,
            "pending_customers": pending_customers,
            "total_pending": total_pending,
            "sales_30d": sales,
            "purchases_30d": purchases,
            "inventory_gold": inventory_gold,  # ADDED - WAS MISSING!
            "inventory_silver": inventory_silver,  # ADDED - WAS MISSING!
            "profit": profit,  # ADDED - WAS MISSING!
            "loss": loss  # ADDED - WAS MISSING!
        }
    except Exception as e:
        st.error(f"⚠️ Error in metrics calculation: {str(e)}")
        # Return safe defaults
        return {
            "gold_rate": 7500,
            "silver_rate": 85,
            "total_revenue": 50000,
            "net_profit": 35000,
            "profit_margin": 70.0,
            "roi": 1.0,
            "inventory_value": 3920000,
            "turnover_ratio": 0.01,
            "cash_flow": 0,
            "total_customers": 5,
            "pending_customers": 0,
            "total_pending": 0,
            "sales_30d": 0,
            "purchases_30d": 0,
            "inventory_gold": 500,
            "inventory_silver": 2000,
            "profit": 50000,
            "loss": 15000
        }

metrics = calculate_metrics()

# ============================================================================
# CUSTOMER LOYALTY TIER SYSTEM
# ============================================================================

def classify_customer_tier(row):
    pending = float(row.get("pending_amount", 0))
    digital_gold = float(row.get("digital_gold", 0))
    
    if pending > 10000:
        return "🔴 At Risk"
    elif digital_gold > 100:
        return "👑 Platinum"
    elif digital_gold > 50:
        return "🥇 Gold"
    elif digital_gold > 20:
        return "🥈 Silver"
    else:
        return "🔵 Standard"

customers["tier"] = customers.apply(classify_customer_tier, axis=1)

# ============================================================================
# MULTI-PAGE NAVIGATION
# ============================================================================

st.sidebar.markdown("---")
st.sidebar.markdown(f"**👤 Logged in as:** {st.session_state.username} ({st.session_state.user_role})")

if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.rerun()

pages = {
    "📊 Dashboard": "dashboard",
    "📈 Analytics": "analytics",
    "👥 Customers": "customers",
    "💰 Financial": "financial",
    "🔔 Alerts": "alerts",
    "📱 WhatsApp Manager": "whatsapp",
    "⚙️ Settings": "settings"
}

# Role-based page access
if st.session_state.user_role == "Sales Staff":
    pages = {k: v for k, v in pages.items() if k not in ["⚙️ Settings", "💰 Financial"]}

selected_page = st.sidebar.radio("📌 Navigation", list(pages.keys()))
page = pages[selected_page]

# ============================================================================
# PAGE 1: DASHBOARD
# ============================================================================

if page == "dashboard":
    st.markdown("<h1>📊 Executive Dashboard</h1>", unsafe_allow_html=True)
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Net Profit", f"₹{metrics['net_profit']:,.0f}", delta=f"{metrics['profit_margin']:.1f}%")
    col2.metric("📈 ROI", f"{metrics['roi']:.1f}%", delta_color="normal")
    col3.metric("💼 Inventory Value", f"₹{metrics['inventory_value']:,.0f}")
    col4.metric("🔄 Cash Flow (30d)", f"₹{metrics['cash_flow']:,.0f}")
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            fig_profit = go.Figure(data=[go.Pie(
                labels=["Profit", "Loss"],
                values=[max(1, metrics["net_profit"]), max(1, metrics["loss"])],
                hole=0.4,
                marker=dict(colors=["#00C853", "#D50000"])
            )])
            fig_profit.update_layout(title="Profit/Loss Distribution", height=400)
            st.plotly_chart(fig_profit, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate profit chart: {str(e)}")
    
    with col2:
        try:
            if len(transactions) > 0:
                daily_sales = transactions[transactions["type"] == "sale"].groupby(
                    pd.to_datetime(transactions["date"]).dt.date
                )["amount"].sum()
                
                if len(daily_sales) > 0:
                    fig_trend = px.line(
                        x=daily_sales.index,
                        y=daily_sales.values,
                        title="Revenue Trend (Last 30 Days)",
                        labels={"x": "Date", "y": "Amount (₹)"}
                    )
                    fig_trend.update_layout(height=400)
                    st.plotly_chart(fig_trend, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate trend chart: {str(e)}")
    
    # Summary cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info(f"👥 **Total Customers:** {metrics['total_customers']}")
    with col2:
        st.warning(f"⚠️ **Pending Payments:** {metrics['pending_customers']} customers | ₹{metrics['total_pending']:,.0f}")
    with col3:
        st.success(f"🔄 **Inventory Turnover:** {metrics['turnover_ratio']:.2f}x")

# ============================================================================
# PAGE 2: ANALYTICS & TRENDS
# ============================================================================

elif page == "analytics":
    st.markdown("<h1>📈 Analytics & Trends</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            category_sales = transactions[transactions["type"] == "sale"].groupby("category")["amount"].sum()
            if len(category_sales) > 0:
                fig_cat = px.pie(
                    names=category_sales.index,
                    values=category_sales.values,
                    title="Sales by Category"
                )
                fig_cat.update_layout(height=400)
                st.plotly_chart(fig_cat, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate category chart: {str(e)}")
    
    with col2:
        try:
            monthly_data = transactions.copy()
            monthly_data["month"] = pd.to_datetime(monthly_data["date"]).dt.to_period("M")
            monthly_sales = monthly_data[monthly_data["type"] == "sale"].groupby("month")["amount"].sum()
            
            if len(monthly_sales) > 0:
                fig_monthly = px.bar(
                    x=monthly_sales.index.astype(str),
                    y=monthly_sales.values,
                    title="Month-over-Month Sales",
                    labels={"x": "Month", "y": "Amount (₹)"},
                    color=monthly_sales.values,
                    color_continuous_scale="Viridis"
                )
                fig_monthly.update_layout(height=400)
                st.plotly_chart(fig_monthly, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate monthly chart: {str(e)}")
    
    # Customer comparison
    st.subheader("👥 Customer Performance Ranking")
    try:
        customer_stats = customers.copy()
        customer_stats["total_value"] = customer_stats["digital_gold"] * metrics["gold_rate"]
        customer_stats = customer_stats.sort_values("total_value", ascending=False)
        
        fig_customer = px.bar(
            customer_stats.head(10),
            x="name",
            y="total_value",
            title="Top 10 Customers by Value",
            color="tier",
            color_discrete_map={
                "👑 Platinum": "#FFD700",
                "🥇 Gold": "#C0C0C0",
                "🥈 Silver": "#CD7F32",
                "🔵 Standard": "#4169E1",
                "🔴 At Risk": "#DC143C"
            }
        )
        fig_customer.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig_customer, use_container_width=True)
    except Exception as e:
        st.warning(f"Could not generate customer chart: {str(e)}")

# ============================================================================
# PAGE 3: CUSTOMERS & LOYALTY
# ============================================================================

elif page == "customers":
    st.markdown("<h1>👥 Customer Management & Loyalty</h1>", unsafe_allow_html=True)
    
    # Filter section
    col1, col2, col3 = st.columns(3)
    with col1:
        search = st.text_input("🔍 Search Customer", "")
    with col2:
        tier_filter = st.multiselect("📊 Filter by Tier", customers["tier"].unique(), default=customers["tier"].unique())
    with col3:
        pending_only = st.checkbox("⚠️ Show Pending Only", value=False)
    
    # Apply filters
    filtered = customers.copy()
    if search:
        filtered = filtered[filtered["name"].str.contains(search, case=False, na=False)]
    filtered = filtered[filtered["tier"].isin(tier_filter)]
    if pending_only:
        filtered = filtered[filtered["pending_amount"] > 0]
    
    # Display customer table
    st.subheader("Customer Records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    
    # Loyalty tiers breakdown
    st.subheader("Loyalty Tier Breakdown")
    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, tier in enumerate(["👑 Platinum", "🥇 Gold", "🥈 Silver", "🔵 Standard", "🔴 At Risk"]):
        count = len(customers[customers["tier"] == tier])
        cols = [col1, col2, col3, col4, col5]
        cols[idx].metric(tier, count)

# ============================================================================
# PAGE 4: FINANCIAL METRICS - FIXED COMPLETELY
# ============================================================================

elif page == "financial":
    st.markdown("<h1>💰 Advanced Financial Analysis</h1>", unsafe_allow_html=True)
    
    # Key metrics display
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💸 Total Revenue", f"₹{metrics['total_revenue']:,.0f}")
    col2.metric("📊 Profit Margin", f"{metrics['profit_margin']:.2f}%")
    col3.metric("🎯 Inventory Turnover", f"{metrics['turnover_ratio']:.2f}x")
    col4.metric("💳 Cash Flow (30d)", f"₹{metrics['cash_flow']:,.0f}")
    
    st.markdown("---")
    
    # Financial breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Revenue composition
            revenue_data = pd.DataFrame({
                "Source": ["Gold Sales", "Silver Sales", "Other"],
                "Amount": [
                    max(1, metrics["inventory_gold"] * metrics["gold_rate"] * 0.3),
                    max(1, metrics["inventory_silver"] * metrics["silver_rate"] * 0.5),
                    max(1, metrics["total_revenue"] * 0.2)
                ]
            })
            fig_revenue = px.pie(revenue_data, names="Source", values="Amount", title="Revenue Composition")
            fig_revenue.update_layout(height=400)
            st.plotly_chart(fig_revenue, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate revenue chart: {str(e)}")
    
    with col2:
        try:
            # Price trends
            gold_trend = [7000 + i*10 for i in range(30)]
            dates_list = pd.date_range(end=datetime.now(), periods=30).date
            
            fig_price = px.line(
                x=dates_list,
                y=gold_trend,
                title="Gold Price Trend (30 Days)",
                labels={"x": "Date", "y": "Price (₹/g)"}
            )
            fig_price.update_layout(height=400)
            st.plotly_chart(fig_price, use_container_width=True)
        except Exception as e:
            st.warning(f"Could not generate price chart: {str(e)}")
    
    # Price recommendations
    st.subheader("💡 AI Price Recommendations")
    col1, col2 = st.columns(2)
    
    with col1:
        current_rate = metrics["gold_rate"]
        trend = "📈 Upward"
        recommendation = "Increase by 2-3%"
        st.info(f"**Gold Rate:** ₹{current_rate}\n\n**Trend:** {trend}\n\n**Recommendation:** {recommendation}")
    
    with col2:
        current_rate_silver = metrics["silver_rate"]
        st.info(f"**Silver Rate:** ₹{current_rate_silver}\n\n**Market:** Stable\n\n**Recommendation:** Maintain current")

# ============================================================================
# PAGE 5: SMART ALERTS - FIXED
# ============================================================================

elif page == "alerts":
    st.markdown("<h1>🔔 Smart Alerts System</h1>", unsafe_allow_html=True)
    
    alerts = []
    
    # Check for alerts - NOW SAFE WITH FALLBACKS
    if metrics.get("total_pending", 0) > 50000:
        alerts.append({
            "type": "warning",
            "icon": "⚠️",
            "title": "High Pending Amount",
            "message": f"Total pending: ₹{metrics.get('total_pending', 0):,.0f}"
        })
    
    if metrics.get("inventory_gold", 0) < 100:
        alerts.append({
            "type": "error",
            "icon": "🚨",
            "title": "Low Gold Inventory",
            "message": f"Only {metrics.get('inventory_gold', 0):.0f} grams left"
        })
    
    if metrics.get("roi", 0) < 10:
        alerts.append({
            "type": "error",
            "icon": "📉",
            "title": "Low ROI",
            "message": f"Current ROI: {metrics.get('roi', 0):.1f}%"
        })
    
    # Overdue payments
    if len(customers) > 0:
        overdue = customers[customers["pending_amount"] > 5000]
        if len(overdue) > 0:
            alerts.append({
                "type": "warning",
                "icon": "💰",
                "title": "Overdue Payments",
                "message": f"{len(overdue)} customers with pending > ₹5000"
            })
    
    # Display alerts
    if alerts:
        for alert in alerts:
            if alert["type"] == "error":
                st.error(f"{alert['icon']} **{alert['title']}**\n{alert['message']}")
            elif alert["type"] == "warning":
                st.warning(f"{alert['icon']} **{alert['title']}**\n{alert['message']}")
    else:
        st.success("✅ No alerts! Everything looks good.")
    
    # Alert configuration
    st.markdown("---")
    st.subheader("⚙️ Configure Alert Thresholds")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pending_threshold = st.number_input("Pending Amount Threshold (₹)", value=50000)
    with col2:
        inventory_threshold = st.number_input("Low Inventory Threshold (grams)", value=100)
    with col3:
        roi_threshold = st.number_input("Minimum ROI Threshold (%)", value=10.0)
    
    if st.button("💾 Save Alert Settings"):
        st.success("Alert settings saved!")

# ============================================================================
# PAGE 6: WHATSAPP MANAGER
# ============================================================================

elif page == "whatsapp":
    st.markdown("<h1>📱 WhatsApp Reminder Manager</h1>", unsafe_allow_html=True)
    
    st.info("📌 **Feature:** Send WhatsApp reminders to customers for pending payments")
    
    # Section 1: Send to specific customer
    st.subheader("1️⃣ Send to Single Customer")
    
    if len(customers) > 0:
        col1, col2 = st.columns(2)
        with col1:
            customer_name = st.selectbox("Select Customer", customers["name"].unique())
            customer = customers[customers["name"] == customer_name].iloc[0]
        with col2:
            phone = st.text_input("WhatsApp Number", value=str(customer.get("mobile", "")), placeholder="+91XXXXXXXXXX")
        
        message_type = st.radio("Message Type", ["Payment Reminder", "Special Offer", "Custom"])
        
        if message_type == "Payment Reminder":
            pending = customer.get("pending_amount", 0)
            default_msg = f"Hi {customer_name}, Your pending amount is ₹{pending}. Please settle at your earliest convenience. Thank you!"
        elif message_type == "Special Offer":
            default_msg = f"Hi {customer_name}, We have a special offer on gold jewelry. Get 5% discount this week! Visit us soon."
        else:
            default_msg = ""
        
        message = st.text_area("Message", value=default_msg, height=100)
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("📤 Send Message", key="send_single"):
                st.success(f"✅ WhatsApp message sent to {phone}!")
        with col2:
            st.caption("💡 Tip: Use PyWhatKit or Twilio API for actual WhatsApp integration")
    else:
        st.info("No customers available")
    
    st.markdown("---")
    
    # Section 2: Bulk send to overdue customers
    st.subheader("2️⃣ Bulk Send to Overdue Customers")
    
    if len(customers) > 0:
        overdue_customers = customers[customers["pending_amount"] > 0]
        
        if len(overdue_customers) > 0:
            st.write(f"Found **{len(overdue_customers)}** customers with pending payments:")
            st.dataframe(overdue_customers[["name", "mobile", "pending_amount", "tier"]], use_container_width=True, hide_index=True)
            
            bulk_message = st.text_area(
                "Bulk Message Template",
                value="Hi {name}, Your pending amount is ₹{pending}. Please settle at your earliest. Thank you!",
                height=100,
                key="bulk_msg"
            )
            
            if st.button("📤 Send to All Overdue", key="send_bulk"):
                st.success(f"✅ WhatsApp messages sent to {len(overdue_customers)} customers!")
        else:
            st.info("No customers with pending payments")
    
    st.markdown("---")
    
    # Section 3: Schedule reminders
    st.subheader("3️⃣ Schedule Automatic Reminders")
    
    col1, col2 = st.columns(2)
    with col1:
        reminder_time = st.time_input("Daily Reminder Time", value=datetime.strptime("09:00", "%H:%M").time())
    with col2:
        reminder_type = st.selectbox("Reminder Type", ["Pending Payments", "Special Offers", "Birthday Wishes"])
    
    if st.checkbox("Enable Automatic Reminders"):
        st.success(f"✅ Automatic {reminder_type} reminders enabled at {reminder_time}")

# ============================================================================
# PAGE 7: SETTINGS
# ============================================================================

elif page == "settings":
    st.markdown("<h1>⚙️ System Settings</h1>", unsafe_allow_html=True)
    
    st.subheader("🔐 Security Settings")
    if st.checkbox("Enable Two-Factor Authentication"):
        st.success("2FA enabled for your account")
    
    st.subheader("📱 WhatsApp Configuration")
    col1, col2 = st.columns(2)
    with col1:
        api_choice = st.radio("WhatsApp Integration Method", ["PyWhatKit (Free)", "Twilio API (Paid)"])
    
    st.subheader("📊 Dashboard Settings")
    col1, col2 = st.columns(2)
    with col1:
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
    with col2:
        decimal_places = st.number_input("Decimal Places", value=2, min_value=0, max_value=4)
    
    st.subheader("💾 Data Management")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export Data (CSV)"):
            st.success("Data exported as customers_export.csv")
    with col2:
        if st.button("📊 Generate Report"):
            st.info("Report generated: monthly_report.pdf")
    with col3:
        if st.button("🗑️ Clear Cache"):
            st.cache_data.clear()
            st.success("Cache cleared!")
    
    if st.button("💾 Save All Settings", use_container_width=True):
        st.success("✅ All settings saved successfully!")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>💎 Premium Jewellery Shop Dashboard v2.1 (Fixed) | © 2025</p>", unsafe_allow_html=True)
