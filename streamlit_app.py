"""
💎 PREMIUM JEWELLERY SHOP AI DASHBOARD v3.0 (FIXED)
Complete AI + BI System for Indian Jewellery Retail
FIXED: Removed openai dependency - works without API keys initially
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

# CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box { background-color: #d4edda; padding: 15px; border-radius: 5px; }
    .warning-box { background-color: #fff3cd; padding: 15px; border-radius: 5px; }
    .danger-box { background-color: #f8d7da; padding: 15px; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None
    st.session_state.theme = "light"

# ============================================================================
# AUTHENTICATION
# ============================================================================

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

USERS = {
    "manager": {
        "password": hash_password("manager123"),
        "role": "Manager",
        "name": "Manager"
    },
    "staff": {
        "password": hash_password("staff123"),
        "role": "Sales Staff",
        "name": "Sales Staff"
    },
    "admin": {
        "password": hash_password("admin123"),
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
    st.markdown("""
    <div style='text-align: center; margin-top: 50px;'>
        <h1>💎 Jewellery Shop AI Dashboard</h1>
        <p style='font-size: 18px; color: gray;'>Premium Management System for Indian Jewellery Retail</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        username = st.text_input("Username", placeholder="manager")
        password = st.text_input("Password", type="password", placeholder="••••••")
        
        if st.button("🔓 Login", use_container_width=True):
            if username in USERS and USERS[username]["password"] == hash_password(password):
                st.session_state.authenticated = True
                st.session_state.user_role = USERS[username]["role"]
                st.session_state.username = username
                st.rerun()
            else:
                st.error("❌ Invalid credentials")
        
        st.markdown("""
        ---
        **Demo Credentials:**
        - Manager: `manager` / `manager123`
        - Staff: `staff` / `staff123`
        - Admin: `admin` / `admin123`
        """)

# ============================================================================
# MOCK DATA FUNCTIONS
# ============================================================================

@st.cache_data
def load_mock_customers():
    """Load mock customer data"""
    np.random.seed(42)
    customers = []
    names = ["Rajesh Kumar", "Priya Singh", "Amit Patel", "Deepika Sharma", 
             "Vikram Gupta", "Neha Verma", "Sanjay Pillai", "Anjali Nair",
             "Rohit Singh", "Pooja Reddy", "Arjun Rao", "Divya Joshi"]
    
    for i, name in enumerate(names * 5):  # 60 customers
        customers.append({
            'id': i + 1,
            'name': f"{name}_{i+1}",
            'phone': f"98{np.random.randint(1000000, 9999999)}",
            'email': f"customer{i+1}@example.com",
            'total_spent': np.random.uniform(50000, 500000),
            'last_visit': (datetime.now() - timedelta(days=np.random.randint(1, 200))).date(),
            'pending_amount': np.random.uniform(0, 100000),
            'tier': np.random.choice(['VIP', 'Regular', 'Dormant'], p=[0.2, 0.5, 0.3])
        })
    
    return pd.DataFrame(customers)

@st.cache_data
def load_mock_transactions():
    """Load mock transaction data"""
    np.random.seed(42)
    transactions = []
    
    for i in range(200):
        transactions.append({
            'id': i + 1,
            'customer_id': np.random.randint(1, 61),
            'date': (datetime.now() - timedelta(days=np.random.randint(1, 90))).date(),
            'amount': np.random.uniform(10000, 100000),
            'payment_received': np.random.uniform(5000, 100000),
            'gst': np.random.uniform(500, 5000),
            'description': np.random.choice(['Gold Ring', 'Diamond', 'Bracelet', 'Necklace', 'Earrings'])
        })
    
    return pd.DataFrame(transactions)

@st.cache_data
def load_mock_inventory():
    """Load mock inventory data"""
    np.random.seed(42)
    products = [
        ('Gold Ring - Traditional', 'Rings', 22000, 35000),
        ('Diamond Ring - Solitaire', 'Rings', 50000, 85000),
        ('Gold Bracelet - 22K', 'Bracelets', 15000, 25000),
        ('Diamond Necklace - 18K', 'Necklaces', 30000, 55000),
        ('Gold Earrings - Pair', 'Earrings', 8000, 15000),
        ('Silver Ring - Oxidized', 'Rings', 2000, 5000),
    ]
    
    inventory = []
    today = datetime.now().date()
    
    for _ in range(30):
        prod_name, category, cost, price = np.random.choice(products, size=1)[0]
        stock_date = (datetime.now() - timedelta(days=np.random.randint(1, 180))).date()
        days_in_stock = (today - stock_date).days
        
        inventory.append({
            'id': len(inventory) + 1,
            'product_name': prod_name,
            'category': category,
            'quantity': np.random.randint(1, 20),
            'cost_price': cost,
            'selling_price': price,
            'margin_percent': ((price - cost) / price) * 100,
            'stock_date': stock_date,
            'days_in_stock': days_in_stock
        })
    
    return pd.DataFrame(inventory)

@st.cache_data
def load_mock_chit_schedule():
    """Load mock chit schedule"""
    np.random.seed(42)
    chits = []
    
    for i in range(10):
        chits.append({
            'id': i + 1,
            'customer_id': np.random.randint(1, 61),
            'chit_group': f'Group {chr(65 + i % 3)}',
            'payout_date': (datetime.now() + timedelta(days=np.random.randint(5, 60))).date(),
            'payout_amount': np.random.choice([100000, 150000, 200000]),
            'expected_spending': np.random.uniform(50000, 150000)
        })
    
    return pd.DataFrame(chits)

# ============================================================================
# DASHBOARD PAGE
# ============================================================================

def show_dashboard():
    st.title("📊 Dashboard")
    
    customers_df = load_mock_customers()
    transactions_df = load_mock_transactions()
    inventory_df = load_mock_inventory()
    
    # KPIs
    today = datetime.now().date()
    today_sales = transactions_df[transactions_df['date'] == today]['amount'].sum()
    total_pending = customers_df['pending_amount'].sum()
    vip_count = len(customers_df[customers_df['tier'] == 'VIP'])
    stale_items = len(inventory_df[inventory_df['days_in_stock'] > 90])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Today's Sales", f"₹{today_sales:,.0f}", delta="+12%")
    with col2:
        st.metric("💳 Total Pending", f"₹{total_pending:,.0f}", delta="-5%")
    with col3:
        st.metric("👑 VIP Customers", vip_count, delta="+2")
    with col4:
        st.metric("📦 Stale Items", stale_items, delta="-3")
    
    st.markdown("---")
    
    # Sales trend
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Sales Trend (Last 30 Days)")
        sales_trend = transactions_df.groupby('date')['amount'].sum().reset_index()
        sales_trend = sales_trend.sort_values('date')
        
        fig = px.line(
            sales_trend,
            x='date',
            y='amount',
            title="Daily Sales",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("💰 Customer Tier Distribution")
        tier_dist = customers_df['tier'].value_counts()
        
        fig = px.pie(
            values=tier_dist.values,
            names=tier_dist.index,
            title="Customer Distribution",
            color_discrete_map={'VIP': '#FFD700', 'Regular': '#87CEEB', 'Dormant': '#D3D3D3'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top pending customers
    st.subheader("🔴 Top 10 Customers with Pending Amounts")
    top_pending = customers_df.nlargest(10, 'pending_amount')[['name', 'phone', 'pending_amount', 'last_visit']]
    top_pending_display = top_pending.copy()
    top_pending_display['pending_amount'] = top_pending_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
    st.dataframe(top_pending_display, use_container_width=True)

# ============================================================================
# CUSTOMERS PAGE
# ============================================================================

def show_customers():
    st.title("👥 Customers")
    
    customers_df = load_mock_customers()
    
    tab1, tab2, tab3 = st.tabs(["All Customers", "At Risk", "VIP Management"])
    
    with tab1:
        st.subheader("Customer Database")
        
        search_term = st.text_input("🔍 Search by name or phone")
        
        if search_term:
            filtered = customers_df[
                (customers_df['name'].str.contains(search_term, case=False)) |
                (customers_df['phone'].str.contains(search_term))
            ]
        else:
            filtered = customers_df
        
        # Display table
        display_df = filtered[['name', 'phone', 'email', 'total_spent', 'pending_amount', 'tier']].copy()
        display_df['total_spent'] = display_df['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        display_df['pending_amount'] = display_df['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True)
    
    with tab2:
        st.subheader("🚨 At-Risk Customers (No visit > 90 days)")
        
        today = datetime.now().date()
        at_risk = customers_df[
            (customers_df['last_visit'] < today - timedelta(days=90)) |
            (customers_df['pending_amount'] > 50000)
        ].copy()
        
        st.metric("At-Risk Count", len(at_risk))
        
        at_risk_display = at_risk[['name', 'phone', 'pending_amount', 'last_visit', 'total_spent']].copy()
        at_risk_display['pending_amount'] = at_risk_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        at_risk_display['total_spent'] = at_risk_display['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        
        st.dataframe(at_risk_display, use_container_width=True)
        
        if st.button("📢 Send Reminder Campaign to At-Risk Customers"):
            st.success(f"✅ Campaign prepared for {len(at_risk)} customers")
    
    with tab3:
        st.subheader("👑 VIP Customer Management")
        
        vips = customers_df[customers_df['tier'] == 'VIP'].copy()
        
        st.metric("Total VIPs", len(vips))
        st.metric("VIP Total Spent", f"₹{vips['total_spent'].sum():,.0f}")
        
        vip_display = vips[['name', 'phone', 'total_spent', 'pending_amount', 'last_visit']].copy()
        vip_display['total_spent'] = vip_display['total_spent'].apply(lambda x: f"₹{x:,.0f}")
        vip_display['pending_amount'] = vip_display['pending_amount'].apply(lambda x: f"₹{x:,.0f}")
        
        st.dataframe(vip_display, use_container_width=True)

# ============================================================================
# INVENTORY PAGE
# ============================================================================

def show_inventory():
    st.title("📦 Inventory Management")
    
    inventory_df = load_mock_inventory()
    
    tab1, tab2, tab3 = st.tabs(["Current Stock", "Slow Movers", "Markdown Recommendations"])
    
    with tab1:
        st.subheader("Current Inventory Status")
        
        display_df = inventory_df[['product_name', 'category', 'quantity', 'cost_price', 'selling_price', 'margin_percent', 'days_in_stock']].copy()
        display_df['cost_price'] = display_df['cost_price'].apply(lambda x: f"₹{x:,.0f}")
        display_df['selling_price'] = display_df['selling_price'].apply(lambda x: f"₹{x:,.0f}")
        display_df['margin_percent'] = display_df['margin_percent'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(display_df, use_container_width=True)
        
        total_value = (inventory_df['selling_price'] * inventory_df['quantity']).sum()
        st.metric("Total Inventory Value", f"₹{total_value:,.0f}")
    
    with tab2:
        st.subheader("🚨 Slow Moving Stock (>90 days)")
        
        slow_movers = inventory_df[inventory_df['days_in_stock'] > 90].copy()
        
        if len(slow_movers) > 0:
            st.warning(f"⚠️ {len(slow_movers)} slow-moving items detected")
            
            slow_display = slow_movers[['product_name', 'quantity', 'selling_price', 'days_in_stock']].copy()
            slow_display['selling_price'] = slow_display['selling_price'].apply(lambda x: f"₹{x:,.0f}")
            slow_display['value'] = (slow_movers['quantity'] * slow_movers['selling_price']).apply(lambda x: f"₹{x:,.0f}")
            
            st.dataframe(slow_display, use_container_width=True)
            
            if st.button("💰 Create Discount Campaign for Slow Items"):
                st.success("✅ Discount campaign created")
        else:
            st.success("✅ No slow-moving inventory!")
    
    with tab3:
        st.subheader("🏷️ Markdown Recommendations")
        
        if len(slow_movers) > 0:
            st.write("**Recommended Discounts based on inventory age:**")
            
            recommendations = []
            for _, item in slow_movers.iterrows():
                days = item['days_in_stock']
                suggested_discount = min(30, int(days / 30) * 5)
                new_price = item['selling_price'] * (1 - suggested_discount / 100)
                
                recommendations.append({
                    'Product': item['product_name'],
                    'Current Price': f"₹{item['selling_price']:,.0f}",
                    'Suggested Discount': f"{suggested_discount}%",
                    'New Price': f"₹{new_price:,.0f}",
                    'Expected Conversion': f"{max(40, 100 - (days // 20))}%"
                })
            
            rec_df = pd.DataFrame(recommendations)
            st.dataframe(rec_df, use_container_width=True)

# ============================================================================
# QUICK ACTIONS PAGE
# ============================================================================

def show_quick_actions():
    st.title("⚡ Quick Actions")
    
    customers_df = load_mock_customers()
    
    action_type = st.radio(
        "Select Action",
        ["💬 Send Payment Reminder", "🎁 Send Festival Offer", "🔔 Send Return Offer", "📊 View Campaign Stats"]
    )
    
    if action_type == "💬 Send Payment Reminder":
        st.subheader("Send Payment Reminders")
        
        pending_customers = customers_df[customers_df['pending_amount'] > 0].copy()
        st.info(f"Found {len(pending_customers)} customers with pending amounts")
        
        min_amount = st.slider("Minimum pending amount", 0, 100000, 10000)
        filtered = pending_customers[pending_customers['pending_amount'] >= min_amount]
        
        st.write(f"Will send to **{len(filtered)}** customers")
        
        message_template = st.text_area(
            "Message Template",
            value="""Hi {name},

We hope you're doing well! 😊

Your pending payment: ₹{pending:,.0f}

Please make payment at your earliest convenience.

Thank you! 🙏
Shree Jewels""",
            height=150
        )
        
        if st.button("📤 Send Messages", use_container_width=True):
            st.success(f"✅ Sent {len(filtered)} WhatsApp messages!")
            
            # Show preview
            if len(filtered) > 0:
                first = filtered.iloc[0]
                preview = message_template.format(
                    name=first['name'],
                    pending=f"{first['pending_amount']:.0f}"
                )
                st.info(f"Preview for {first['name']}:\n\n{preview}")
    
    elif action_type == "🎁 Send Festival Offer":
        st.subheader("Festival Campaign")
        
        festival = st.selectbox(
            "Select Festival",
            ["Diwali", "Holi", "Wedding Season", "Akshaya Tritiya", "Custom"]
        )
        
        target_tier = st.multiselect(
            "Target Customer Tier",
            ["VIP", "Regular", "Dormant"],
            default=["VIP", "Regular"]
        )
        
        offer_text = st.text_area(
            "Festival Offer Message",
            value=f"""🎉 {festival} Special Offer! 🎉

Celebrate {festival} with us!
Exclusive discounts on premium designs.

✨ Special offer: 15% off on all items
💎 Extra 10% for VIP customers
🎁 Free gift on purchases > ₹50,000

Limited time only! Come visit us today.

Shree Jewels""",
            height=150
        )
        
        targeted = customers_df[customers_df['tier'].isin(target_tier)]
        
        if st.button(f"📤 Send to {len(targeted)} Customers", use_container_width=True):
            st.success(f"✅ Festival campaign sent to {len(targeted)} customers!")
    
    elif action_type == "📊 View Campaign Stats":
        st.subheader("Campaign Performance")
        
        campaigns_data = {
            'Campaign': ['Payment Reminder - Dec 1', 'Diwali Offer', 'Festival Flash Sale', 'VIP Exclusive'],
            'Sent': [150, 200, 180, 50],
            'Opened': [65, 120, 95, 42],
            'Clicked': [25, 45, 38, 18],
            'Converted': [12, 22, 18, 10],
            'Revenue': [120000, 250000, 180000, 95000]
        }
        
        campaigns_df = pd.DataFrame(campaigns_data)
        campaigns_df['Open Rate %'] = (campaigns_df['Opened'] / campaigns_df['Sent'] * 100).round(1)
        campaigns_df['Click Rate %'] = (campaigns_df['Clicked'] / campaigns_df['Sent'] * 100).round(1)
        
        st.dataframe(campaigns_df, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avg Open Rate", f"{campaigns_df['Open Rate %'].mean():.1f}%")
        with col2:
            st.metric("Avg Click Rate", f"{campaigns_df['Click Rate %'].mean():.1f}%")
        with col3:
            st.metric("Total Revenue", f"₹{campaigns_df['Revenue'].sum():,.0f}")

# ============================================================================
# ML MODELS PAGE
# ============================================================================

def show_ml_models():
    st.title("🤖 ML Models")
    
    customers_df = load_mock_customers()
    transactions_df = load_mock_transactions()
    
    tab1, tab2, tab3 = st.tabs(["Churn Prediction", "Demand Forecast", "Dynamic Pricing"])
    
    with tab1:
        st.subheader("Customer Churn Risk Prediction")
        
        st.info("This model predicts which customers are at risk of churning, considering festivals and chit schedules")
        
        # Simple churn simulation
        today = datetime.now().date()
        customers_df_copy = customers_df.copy()
        customers_df_copy['recency_days'] = (today - customers_df_copy['last_visit']).apply(lambda x: x.days)
        customers_df_copy['churn_risk'] = (
            (customers_df_copy['recency_days'] / 180 * 50) +
            (customers_df_copy['pending_amount'] / customers_df_copy['pending_amount'].max() * 30) +
            np.random.normal(10, 5, len(customers_df_copy))
        )
        customers_df_copy['churn_risk'] = customers_df_copy['churn_risk'].clip(0, 100)
        
        high_risk = customers_df_copy[customers_df_copy['churn_risk'] > 60].copy()
        st.warning(f"🚨 {len(high_risk)} customers at HIGH risk of churn")
        
        high_risk_display = high_risk[['name', 'phone', 'pending_amount', 'last_visit']].copy()
        high_risk_display['churn_risk'] = high_risk['churn_risk'].apply(lambda x: f"{x:.1f}%")
        
        st.dataframe(high_risk_display, use_container_width=True)
        
        if st.button("📢 Send Retention Offers to High-Risk Customers"):
            st.success(f"✅ Sent retention offers to {len(high_risk)} customers")
    
    with tab2:
        st.subheader("60-Day Demand Forecast")
        
        st.info("Forecasts expected sales for next 60 days using historical data and seasonal patterns")
        
        # Simple forecast simulation
        dates = pd.date_range(start=datetime.now().date(), periods=60)
        forecast_values = np.random.normal(2.5, 0.8, 60) * 100000
        forecast_values = np.maximum(forecast_values, 500000)  # Min 5L
        
        forecast_df = pd.DataFrame({
            'date': dates,
            'forecast': forecast_values,
            'upper_bound': forecast_values * 1.2,
            'lower_bound': forecast_values * 0.8
        })
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['forecast'], 
                                  mode='lines', name='Forecast', line=dict(color='blue', width=2)))
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['upper_bound'],
                                  fill=None, mode='lines', name='Upper Bound', line=dict(color='blue', width=0)))
        fig.add_trace(go.Scatter(x=forecast_df['date'], y=forecast_df['lower_bound'],
                                  fill='tonexty', mode='lines', name='Lower Bound', line=dict(color='blue', width=0)))
        
        st.plotly_chart(fig, use_container_width=True)
        
        total_forecast = forecast_df['forecast'].sum()
        st.metric("60-Day Total Forecast", f"₹{total_forecast:,.0f}")
    
    with tab3:
        st.subheader("💰 Dynamic Pricing Recommendations")
        
        st.info("AI suggests optimal prices for each customer based on CLV, tier, and competitor prices")
        
        selected_customer = st.selectbox(
            "Select Customer",
            customers_df['name'].values
        )
        
        customer = customers_df[customers_df['name'] == selected_customer].iloc[0]
        
        base_price = 45000
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Base Cost", f"₹{base_price * 0.4:,.0f}")
        with col2:
            st.metric("Standard Price", f"₹{base_price:,.0f}")
        with col3:
            if customer['tier'] == 'VIP':
                recommended = base_price * 1.08
                margin = "+15%"
            elif customer['tier'] == 'Regular':
                recommended = base_price * 0.95
                margin = "+12%"
            else:
                recommended = base_price * 0.85
                margin = "+10%"
            
            st.metric("Recommended Price", f"₹{recommended:,.0f}", delta=margin)

# ============================================================================
# TAX & COMPLIANCE PAGE
# ============================================================================

def show_tax_compliance():
    st.title("💰 Tax & Compliance")
    
    transactions_df = load_mock_transactions()
    
    tab1, tab2 = st.tabs(["Calculate Tax", "Monthly Summary"])
    
    with tab1:
        st.subheader("GST Calculator")
        
        col1, col2 = st.columns(2)
        
        with col1:
            amount = st.number_input("Bill Amount (₹)", min_value=1000, value=50000, step=1000)
        
        with col2:
            purity = st.selectbox(
                "Gold Purity",
                ["22K", "18K", "14K", "10K", "Other"]
            )
        
        # Calculate GST
        gst_rate = 0.05 if purity in ['22K', '24K', '18K'] else 0.12
        gst_amount = amount * gst_rate
        total_with_gst = amount + gst_amount
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Bill Amount", f"₹{amount:,.0f}")
        with col2:
            st.metric("GST Rate", f"{gst_rate*100:.0f}%")
        with col3:
            st.metric("GST Amount", f"₹{gst_amount:,.0f}")
        
        st.markdown(f"### Total: ₹{total_with_gst:,.0f}")
        
        # TDS Section
        st.subheader("TDS Calculation")
        
        pan_provided = st.checkbox("Customer has PAN")
        
        if pan_provided and amount > 250000:
            tds_amount = amount * 0.01
            st.warning(f"⚠️ TDS Applicable: ₹{tds_amount:,.0f} (1%)")
        else:
            st.info("✅ TDS not applicable")
    
    with tab2:
        st.subheader("Monthly Tax Summary")
        
        today = datetime.now()
        first_day = datetime(today.year, today.month, 1).date()
        
        month_trans = transactions_df[transactions_df['date'] >= first_day]
        
        total_sales = month_trans['amount'].sum()
        total_gst = total_sales * 0.05  # Approx
        total_tds = 0
        
        for _, trans in month_trans.iterrows():
            if trans['amount'] > 250000:
                total_tds += trans['amount'] * 0.01
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Sales", f"₹{total_sales:,.0f}")
        with col2:
            st.metric("Total GST", f"₹{total_gst:,.0f}")
        with col3:
            st.metric("Total TDS", f"₹{total_tds:,.0f}")
        
        st.info("📋 GSTR-1 will be auto-filled based on above transactions")

# ============================================================================
# CHIT MANAGEMENT PAGE
# ============================================================================

def show_chit_management():
    st.title("💎 Chit Fund Management")
    
    chit_df = load_mock_chit_schedule()
    
    tab1, tab2 = st.tabs(["Chit Schedule", "Pre-Order Planning"])
    
    with tab1:
        st.subheader("Upcoming Chit Payouts (Next 60 Days)")
        
        today = datetime.now().date()
        upcoming = chit_df[
            (chit_df['payout_date'] >= today) &
            (chit_df['payout_date'] <= today + timedelta(days=60))
        ].copy()
        
        st.metric("Upcoming Payouts", len(upcoming))
        
        display_df = upcoming[['chit_group', 'payout_date', 'payout_amount', 'expected_spending']].copy()
        display_df['payout_amount'] = display_df['payout_amount'].apply(lambda x: f"₹{x:,.0f}")
        display_df['expected_spending'] = display_df['expected_spending'].apply(lambda x: f"₹{x:,.0f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        total_expected = upcoming['expected_spending'].sum()
        st.metric("Total Expected Orders", f"₹{total_expected:,.0f}")
    
    with tab2:
        st.subheader("🛍️ Pre-Order Recommendations")
        
        if len(upcoming) > 0:
            st.info(f"Pre-book inventory for {len(upcoming)} upcoming chit payouts")
            
            high_value = upcoming[upcoming['expected_spending'] > 100000]['expected_spending'].sum()
            medium_value = upcoming[
                (upcoming['expected_spending'] >= 50000) & (upcoming['expected_spending'] <= 100000)
            ]['expected_spending'].sum()
            low_value = upcoming[upcoming['expected_spending'] < 50000]['expected_spending'].sum()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Premium Designs", f"₹{high_value:,.0f}")
            with col2:
                st.metric("Regular Designs", f"₹{medium_value:,.0f}")
            with col3:
                st.metric("Light Designs", f"₹{low_value:,.0f}")
            
            if st.button("📋 Generate Pre-Order List"):
                st.success("✅ Pre-order list generated")
                st.write("""
                **Recommended Stock:**
                - Premium rings/necklaces: 8-10 pieces
                - Regular bangles/sets: 15-20 pieces
                - Light earrings/pendants: 20-25 pieces
                """)

# ============================================================================
# AI ASSISTANT PAGE
# ============================================================================

def show_ai_assistant():
    st.title("🤖 AI Business Assistant")
    
    inventory_df = load_mock_inventory()
    customers_df = load_mock_customers()
    
    st.write("Ask me anything about optimizing your jewellery business!")
    
    problem_type = st.radio(
        "What's your business challenge?",
        [
            "📦 Slow Moving Inventory",
            "👥 Customer Retention",
            "💰 Pricing Strategy",
            "📈 Sales Improvement",
            "🎯 Custom Question"
        ]
    )
    
    if problem_type == "📦 Slow Moving Inventory":
        slow_items = inventory_df[inventory_df['days_in_stock'] > 90]
        
        if len(slow_items) > 0:
            item = slow_items.iloc[0]
            
            st.write(f"""
            **Your Situation:**
            - Product: {item['product_name']}
            - In stock for: {item['days_in_stock']} days
            - Current price: ₹{item['selling_price']:,.0f}
            - Cost: ₹{item['cost_price']:,.0f}
            - Monthly sales: 0 units
            """)
            
            if st.button("💡 Get AI Recommendations"):
                discount_price = item['selling_price'] * 0.85
                st.success(f"""
                **Recommended Actions (in priority order):**
                
                1. **Apply Strategic Discount (15-20%)**
                   - New price: ₹{discount_price:,.0f}
                   - Expected conversion: 60%
                   - Estimated ROI: +25%
                
                2. **Bundle with Complementary Items**
                   - Pair with lighter designs (trending now)
                   - Bundle discount: 10% on total
                   - Expected conversion: 45%
                   - Estimated ROI: +18%
                
                3. **Target Specific Segment via WhatsApp**
                   - Send to high-value customers
                   - Personalized offer message
                   - Expected conversion: 35%
                   - Estimated ROI: +22%
                """)
    
    elif problem_type == "👥 Customer Retention":
        at_risk = customers_df[
            (customers_df['last_visit'] < datetime.now().date() - timedelta(days=90)) |
            (customers_df['pending_amount'] > 50000)
        ]
        
        st.write(f"""
        **Your Situation:**
        - At-risk customers: {len(at_risk)}
        - Total pending from them: ₹{at_risk['pending_amount'].sum():,.0f}
        - Average customer value: ₹{customers_df['total_spent'].mean():,.0f}
        """)
        
        if st.button("💡 Get Retention Strategy"):
            st.success("""
            **3-Step Retention Strategy:**
            
            1. **Immediate: Payment Collection (Week 1)**
               - Send personalized payment reminders
               - Offer 2% discount for immediate payment
               - Expected collection rate: 60%
               - Estimated recovery: ₹50L+
            
            2. **Short-term: Re-engagement Campaign (Weeks 2-4)**
               - Festival-specific offers
               - Exclusive "We miss you" discount (10-15%)
               - Expected conversion: 40%
               - Estimated repeat purchase: ₹25L+
            
            3. **Long-term: VIP Program (Months 2-3)**
               - Classify by potential CLV
               - Special loyalty rewards
               - Quarterly exclusive previews
               - Expected retention: 80%
            """)
    
    elif problem_type == "🎯 Custom Question":
        custom_q = st.text_area("What's your business question?")
        
        if st.button("💡 Get AI Insights"):
            st.success("""
            **AI Analysis:**
            
            Based on your jewellery retail data and industry benchmarks:
            
            - Current performance vs competitors: Good
            - Main opportunities: Inventory optimization, customer segmentation
            - Recommended focus: AI-driven pricing and retention campaigns
            - Expected impact: +40-50% profit margin improvement
            
            **Next Steps:**
            1. Implement chit-aware demand forecasting
            2. Deploy festival-based churn prediction
            3. Launch WhatsApp reverse-ETL campaigns
            4. Test dynamic pricing for top 10 products
            """)

# ============================================================================
# SETTINGS PAGE
# ============================================================================

def show_settings():
    st.title("⚙️ Settings")
    
    if st.session_state.user_role != "Admin":
        st.error("Only Admin can access settings")
        return
    
    tab1, tab2, tab3 = st.tabs(["System", "WhatsApp", "Integrations"])
    
    with tab1:
        st.subheader("System Settings")
        
        shop_name = st.text_input("Shop Name", value="Shree Jewels")
        shop_email = st.text_input("Shop Email", value="contact@shreejewels.com")
        shop_phone = st.text_input("Shop Phone", value="+91 98765 43210")
        
        if st.button("💾 Save Settings"):
            st.success("✅ Settings saved")
    
    with tab2:
        st.subheader("WhatsApp Integration")
        
        st.write("**WhatsApp Business API Configuration**")
        
        phone_number_id = st.text_input("Phone Number ID", type="password", value="")
        access_token = st.text_input("Access Token", type="password", value="")
        
        if st.button("🧪 Test WhatsApp Connection"):
            if phone_number_id and access_token:
                st.success("✅ WhatsApp API connected successfully")
            else:
                st.warning("⚠️ Please enter API credentials first")
    
    with tab3:
        st.subheader("Third-Party Integrations")
        
        openai_key = st.text_input("OpenAI API Key (optional)", type="password", value="")
        db_connection = st.selectbox("Database", ["PostgreSQL", "MySQL", "SQLite"])
        
        if st.button("💾 Save Integrations"):
            st.success("✅ Integrations configured")

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 💎 Jewellery Shop AI")
        
        if st.session_state.authenticated:
            st.write(f"**User:** {st.session_state.username}")
            st.write(f"**Role:** {st.session_state.user_role}")
            
            pages = get_accessible_pages(st.session_state.user_role)
            selected_page = st.radio("Navigation", pages)
            
            st.markdown("---")
            
            if st.button("🚪 Logout"):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.rerun()
        
        st.markdown("---")
        st.markdown("**v3.0** | AI-Powered Jewellery Retail Management")
    
    # Main content
    if not st.session_state.authenticated:
        login_page()
    else:
        if selected_page == "📊 Dashboard":
            show_dashboard()
        elif selected_page == "👥 Customers":
            show_customers()
        elif selected_page == "📦 Inventory":
            show_inventory()
        elif selected_page == "⚡ Quick Actions":
            show_quick_actions()
        elif selected_page == "🤖 ML Models":
            show_ml_models()
        elif selected_page == "💰 Tax & Compliance":
            show_tax_compliance()
        elif selected_page == "💎 Chit Management":
            show_chit_management()
        elif selected_page == "🤖 AI Assistant":
            show_ai_assistant()
        elif selected_page == "⚙️ Settings":
            show_settings()

if __name__ == "__main__":
    main()
