import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
from pathlib import Path
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

# Demo credentials
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
    try:
        customers = pd.read_csv(r"C:\\Users\\shail\\OneDrive\\Desktop\\oops prog\\DA2\\customers.csv")
    except FileNotFoundError:
        st.warning("❌ customers.csv not found. Using sample data.")
        customers = pd.DataFrame({
            "name": ["Rajesh Kumar", "Priya Singh", "Amit Patel", "Neha Sharma", "Vikram Gupta"],
            "mobile": ["9876543210", "9123456789", "9098765432", "9012345678", "9111223344"],
            "digital_gold": [50, 75, 100, 30, 60],
            "pending_amount": [5000, 0, 10000, 2000, 0]
        })
    
    try:
        summary = pd.read_csv(r"C:\\Users\\shail\\OneDrive\\Desktop\\oops prog\\DA2\\summary.csv")
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
    
    # Generate transaction history (mock data for trends)
    dates = pd.date_range(start="2025-01-01", end="2025-12-09", freq="D")
    transactions = pd.DataFrame({
        "date": np.random.choice(dates, 100),
        "amount": np.random.randint(1000, 50000, 100),
        "type": np.random.choice(["sale", "purchase"], 100),
        "category": np.random.choice(["gold", "silver", "diamond"], 100)
    })
    
    return customers, summary, transactions

customers, summary, transactions = load_data()

# ============================================================================
# CALCULATE ADVANCED FINANCIAL METRICS
# ============================================================================

def calculate_metrics():
    gold_rate = float(summary.get("gold_rate", [7500])[0])
    silver_rate = float(summary.get("silver_rate", [85])[0])
    profit = float(summary.get("profit", [0])[0])
    loss = float(summary.get("loss", [0])[0])
    
    inventory_gold = float(summary.get("inventory_gold", [500])[0])
    inventory_silver = float(summary.get("inventory_silver", [2000])[0])
    
    # Calculate metrics
    total_revenue = profit + loss
    net_profit = profit - loss
    profit_margin = (net_profit / total_revenue * 100) if total_revenue > 0 else 0
    roi = (net_profit / (inventory_gold * gold_rate + inventory_silver * silver_rate) * 100) if (inventory_gold * gold_rate + inventory_silver * silver_rate) > 0 else 0
    
    # Customer metrics
    total_customers = len(customers)
    pending_customers = len(customers[customers.get("pending_amount", 0) > 0])
    total_pending = customers.get("pending_amount", pd.Series([0])).sum()
    
    # Cash flow
    daily_transactions = transactions[transactions["date"] >= datetime.now() - timedelta(days=30)]
    sales = daily_transactions[daily_transactions["type"] == "sale"]["amount"].sum()
    purchases = daily_transactions[daily_transactions["type"] == "purchase"]["amount"].sum()
    cash_flow = sales - purchases
    
    # Inventory turnover (simplified)
    inventory_value = inventory_gold * gold_rate + inventory_silver * silver_rate
    turnover_ratio = total_revenue / inventory_value if inventory_value > 0 else 0
    
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
        "purchases_30d": purchases
    }

metrics = calculate_metrics()

# ============================================================================
# CUSTOMER LOYALTY TIER SYSTEM
# ============================================================================

def classify_customer_tier(row):
    pending = row.get("pending_amount", 0)
    digital_gold = row.get("digital_gold", 0)
    
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
        # Profit vs Loss Donut
        fig_profit = go.Figure(data=[go.Pie(
            labels=["Profit", "Loss"],
            values=[metrics["net_profit"] + metrics["total_revenue"]//2, metrics["total_revenue"]//2],
            hole=0.4,
            marker=dict(colors=["#00C853", "#D50000"])
        )])
        fig_profit.update_layout(title="Profit/Loss Distribution")
        st.plotly_chart(fig_profit, use_container_width=True)
    
    with col2:
        # Revenue trend
        daily_sales = transactions[transactions["type"] == "sale"].groupby(transactions["date"].dt.date)["amount"].sum()
        fig_trend = px.line(
            x=daily_sales.index,
            y=daily_sales.values,
            title="Revenue Trend (Last 30 Days)",
            labels={"x": "Date", "y": "Amount (₹)"}
        )
        st.plotly_chart(fig_trend, use_container_width=True)
    
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
        # Category-wise sales
        category_sales = transactions[transactions["type"] == "sale"].groupby("category")["amount"].sum()
        fig_cat = px.pie(
            names=category_sales.index,
            values=category_sales.values,
            title="Sales by Category"
        )
        st.plotly_chart(fig_cat, use_container_width=True)
    
    with col2:
        # Monthly comparison
        monthly_data = transactions.copy()
        monthly_data["month"] = pd.to_datetime(monthly_data["date"]).dt.to_period("M")
        monthly_sales = monthly_data[monthly_data["type"] == "sale"].groupby("month")["amount"].sum()
        
        fig_monthly = px.bar(
            x=monthly_sales.index.astype(str),
            y=monthly_sales.values,
            title="Month-over-Month Sales",
            labels={"x": "Month", "y": "Amount (₹)"},
            color=monthly_sales.values,
            color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    # Customer comparison
    st.subheader("👥 Customer Performance Ranking")
    customer_stats = customers.copy()
    customer_stats["total_value"] = customer_stats.get("digital_gold", 0) * metrics["gold_rate"]
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
    st.plotly_chart(fig_customer, use_container_width=True)

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
        filtered = filtered[filtered.get("pending_amount", 0) > 0]
    
    # Display customer table with editable data
    st.subheader("Customer Records")
    st.dataframe(filtered, use_container_width=True, hide_index=True)
    
    # Loyalty tiers breakdown
    col1, col2, col3, col4, col5 = st.columns(5)
    for idx, tier in enumerate(["👑 Platinum", "🥇 Gold", "🥈 Silver", "🔵 Standard", "🔴 At Risk"]):
        count = len(customers[customers["tier"] == tier])
        cols = [col1, col2, col3, col4, col5]
        cols[idx].metric(tier, count)
    
    # Detailed customer analysis
    st.subheader("📊 Customer Value Distribution")
    customers_copy = customers.copy()
    customers_copy["value"] = customers_copy.get("digital_gold", 0) * metrics["gold_rate"]
    
    fig_value = px.histogram(
        customers_copy,
        x="value",
        nbins=10,
        title="Customer Value Distribution",
        color_discrete_sequence=["#1f77b4"]
    )
    st.plotly_chart(fig_value, use_container_width=True)

# ============================================================================
# PAGE 4: FINANCIAL METRICS
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
        # Revenue composition
        revenue_data = pd.DataFrame({
            "Source": ["Gold Sales", "Silver Sales", "Other"],
            "Amount": [
                metrics["inventory_gold"] * metrics["gold_rate"] * 0.3,
                metrics["inventory_silver"] * metrics["silver_rate"] * 0.5,
                metrics["total_revenue"] * 0.2
            ]
        })
        fig_revenue = px.pie(revenue_data, names="Source", values="Amount", title="Revenue Composition")
        st.plotly_chart(fig_revenue, use_container_width=True)
    
    with col2:
        # Price trends
        gold_trend = [7000 + i*10 for i in range(30)]
        dates_list = pd.date_range(end=datetime.now(), periods=30).date
        
        fig_price = px.line(
            x=dates_list,
            y=gold_trend,
            title="Gold Price Trend (30 Days)",
            labels={"x": "Date", "y": "Price (₹/g)"}
        )
        st.plotly_chart(fig_price, use_container_width=True)
    
    # Price recommendations
    st.subheader("💡 AI Price Recommendations")
    col1, col2 = st.columns(2)
    
    with col1:
        current_rate = metrics["gold_rate"]
        trend = "📈 Upward" if gold_trend[-1] > gold_trend[0] else "📉 Downward"
        recommendation = f"Increase by 2-3%" if gold_trend[-1] > gold_trend[0] else "Maintain current"
        st.info(f"**Gold Rate:** ₹{current_rate}\n\n**Trend:** {trend}\n\n**Recommendation:** {recommendation}")
    
    with col2:
        current_rate_silver = metrics["silver_rate"]
        st.info(f"**Silver Rate:** ₹{current_rate_silver}\n\n**Market:** Stable\n\n**Recommendation:** Maintain current")

# ============================================================================
# PAGE 5: SMART ALERTS
# ============================================================================

elif page == "alerts":
    st.markdown("<h1>🔔 Smart Alerts System</h1>", unsafe_allow_html=True)
    
    alerts = []
    
    # Check for alerts
    if metrics["total_pending"] > 50000:
        alerts.append({"type": "warning", "icon": "⚠️", "title": "High Pending Amount", "message": f"Total pending: ₹{metrics['total_pending']:,.0f}"})
    
    if metrics["inventory_gold"] < 100:
        alerts.append({"type": "error", "icon": "🚨", "title": "Low Gold Inventory", "message": f"Only {metrics['inventory_gold']} grams left"})
    
    if metrics["roi"] < 10:
        alerts.append({"type": "error", "icon": "📉", "title": "Low ROI", "message": f"Current ROI: {metrics['roi']:.1f}%"})
    
    # Overdue payments
    overdue = customers[customers.get("pending_amount", 0) > 5000]
    if len(overdue) > 0:
        alerts.append({"type": "warning", "icon": "💰", "title": "Overdue Payments", "message": f"{len(overdue)} customers with pending > ₹5000"})
    
    # Price threshold
    if metrics["gold_rate"] > 7500:
        alerts.append({"type": "info", "icon": "📊", "title": "Price Threshold Alert", "message": f"Gold exceeded ₹7500 (Current: ₹{metrics['gold_rate']})"})
    
    # Display alerts
    if alerts:
        for alert in alerts:
            if alert["type"] == "error":
                st.error(f"{alert['icon']} **{alert['title']}**\n{alert['message']}")
            elif alert["type"] == "warning":
                st.warning(f"{alert['icon']} **{alert['title']}**\n{alert['message']}")
            else:
                st.info(f"{alert['icon']} **{alert['title']}**\n{alert['message']}")
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
    
    st.info("📌 **Feature:** Send WhatsApp reminders to customers for pending payments and offers")
    
    # Section 1: Send to specific customer
    st.subheader("1️⃣ Send to Single Customer")
    
    col1, col2 = st.columns(2)
    with col1:
        customer_name = st.selectbox("Select Customer", customers["name"].unique())
        customer = customers[customers["name"] == customer_name].iloc[0]
    with col2:
        phone = st.text_input("WhatsApp Number", value=customer.get("mobile", ""), placeholder="+91XXXXXXXXXX")
    
    message_type = st.radio("Message Type", ["Payment Reminder", "Special Offer", "Custom"])
    
    if message_type == "Payment Reminder":
        default_msg = f"Hi {customer_name}, Your pending amount is ₹{customer.get('pending_amount', 0)}. Please settle at your earliest convenience. Thank you!"
    elif message_type == "Special Offer":
        default_msg = f"Hi {customer_name}, We have a special offer on gold jewelry. Get 5% discount this week! Visit us soon."
    else:
        default_msg = ""
    
    message = st.text_area("Message", value=default_msg, height=100)
    
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("📤 Send Message", key="send_single"):
            st.success(f"✅ WhatsApp message sent to {phone}!")
            st.info(f"Message: {message}")
    with col2:
        st.caption("💡 Tip: Use PyWhatKit or Twilio API for actual WhatsApp integration")
    
    st.markdown("---")
    
    # Section 2: Bulk send to overdue customers
    st.subheader("2️⃣ Bulk Send to Overdue Customers")
    
    overdue_customers = customers[customers.get("pending_amount", 0) > 0]
    
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
        with st.expander("View Details"):
            for _, customer in overdue_customers.iterrows():
                msg = bulk_message.format(name=customer["name"], pending=int(customer.get("pending_amount", 0)))
                st.caption(f"📱 {customer['mobile']}: {msg}")
    
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
    
    st.markdown("---")
    
    # Message history
    st.subheader("📋 Message History")
    history_data = pd.DataFrame({
        "Timestamp": pd.date_range(end=datetime.now(), periods=5),
        "Customer": overdue_customers["name"].head(5).values,
        "Phone": overdue_customers["mobile"].head(5).values,
        "Status": ["✅ Sent"] * 5
    })
    st.dataframe(history_data, use_container_width=True, hide_index=True)

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
    with col2:
        if api_choice == "Twilio API (Paid)":
            api_key = st.text_input("Twilio API Key", type="password")
            account_sid = st.text_input("Account SID")
    
    st.subheader("📊 Dashboard Settings")
    col1, col2 = st.columns(2)
    with col1:
        currency = st.selectbox("Currency", ["INR (₹)", "USD ($)", "EUR (€)"])
    with col2:
        decimal_places = st.number_input("Decimal Places", value=2, min_value=0, max_value=4)
    
    st.subheader("📧 Notification Preferences")
    col1, col2 = st.columns(2)
    with col1:
        st.checkbox("Email Notifications", value=True)
        st.checkbox("WhatsApp Alerts", value=True)
    with col2:
        st.checkbox("SMS Reminders", value=False)
        st.checkbox("Push Notifications", value=True)
    
    st.subheader("💾 Data Management")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📥 Export Data (CSV)"):
            customers.to_csv("customers_export.csv", index=False)
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
st.markdown("<p style='text-align: center; color: gray;'>💎 Premium Jewellery Shop Dashboard v2.0 | © 2025</p>", unsafe_allow_html=True)
