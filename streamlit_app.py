import pandas as pd
import streamlit as st
import plotly.express as px

# Page setup
st.set_page_config(page_title="Jewellery Shop Dashboard", layout="wide", page_icon="💎")

# --- Load Data Function ---
@st.cache_data
def load_data():
    try:
        customers = pd.read_csv("customers.csv")
    except FileNotFoundError:
        st.warning("❌ customers.csv not found. Using empty data.")
        customers = pd.DataFrame(columns=["name", "mobile", "digital_gold", "pending_amount"])

    try:
        summary = pd.read_csv("summary.csv")
    except FileNotFoundError:
        st.warning("❌ summary.csv not found. Using default values.")
        summary = pd.DataFrame([{
            "gold_rate": 5000,
            "silver_rate": 60,
            "profit": 0,
            "loss": 0
        }])

    # 🧩 Normalise headers
    customers.columns = customers.columns.str.strip().str.lower().str.replace(" ", "_")
    summary.columns = summary.columns.str.strip().str.lower().str.replace(" ", "_")

    return customers, summary

# --- Load data ---
customers, summary = load_data()

# --- Sidebar Filters ---
st.sidebar.title("🔍 Dashboard Filters")
customer_search = st.sidebar.text_input("Search Customer Name")
pending_filter = st.sidebar.checkbox("Show Only Pending Payments", value=False)

# --- Header ---
st.title("💎 Jewellery Shop Dashboard")
st.markdown("### Real-time Overview of Daily Jewellery Sales and Performance")

# --- Display Summary Metrics ---
gold_rate = float(summary.get("gold_rate", [0])[0])
silver_rate = float(summary.get("silver_rate", [0])[0])
profit = float(summary.get("profit", [0])[0])
loss = float(summary.get("loss", [0])[0])
net = profit - loss

col1, col2, col3 = st.columns(3)
col1.metric("Gold Rate (₹/g)", f"{gold_rate:.2f}")
col2.metric("Silver Rate (₹/g)", f"{silver_rate:.2f}")
col3.metric("Net Profit / Loss", f"₹{net:.2f}", delta_color="off")

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📊 Summary", "👥 Customers", "📈 Charts"])

# === Tab 1: Daily Summary ===
with tab1:
    st.subheader("🪙 Day Summary Details")
    st.dataframe(summary, use_container_width=True)

# === Tab 2: Customer Information ===
with tab2:
    st.subheader("👥 Customer Records")

    filtered_customers = customers.copy()
    if customer_search:
        filtered_customers = filtered_customers[
            filtered_customers["name"].str.contains(customer_search, case=False, na=False)
        ]
    if pending_filter and "pending_amount" in filtered_customers.columns:
        filtered_customers = filtered_customers[filtered_customers["pending_amount"] > 0]

    st.data_editor(filtered_customers, use_container_width=True, num_rows="dynamic", key="customer_edit")

    if "pending_amount" in filtered_customers.columns:
        pending = filtered_customers[filtered_customers["pending_amount"] > 0]
        st.metric("Customers with Pending", len(pending))
        if not pending.empty:
            st.subheader("Pending Payments")
            st.dataframe(pending, use_container_width=True)
    else:
        st.info("⚠️ No 'pending_amount' column found in customer data.")

# === Tab 3: Charts & Visuals ===
with tab3:
    st.subheader("📈 Gold and Silver Analysis")

    # 1️⃣ Digital Gold Chart
    if "digital_gold" in customers.columns and not customers.empty:
        fig1 = px.bar(
            customers,
            x="name",
            y="digital_gold",
            color="digital_gold",
            title="Digital Gold Holdings (grams)",
            color_continuous_scale=[[0, "#b8860b"], [1, "#ffd700"]]  # gold gradient
        )
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No digital gold data available.")

    # 2️⃣ Profit vs Loss Pie Chart
    st.subheader("Profit vs Loss Overview")
    fig2 = px.pie(
        names=["Profit", "Loss"],
        values=[profit, loss],
        title="Profit/Loss Ratio",
        hole=0.4,
        color_discrete_sequence=["#00C853", "#D50000"]
    )
    st.plotly_chart(fig2, use_container_width=True)

    # 3️⃣ Pending Amount Distribution
    if "pending_amount" in customers.columns and customers["pending_amount"].sum() > 0:
        st.subheader("Pending Payments Distribution")
        fig3 = px.histogram(
            customers,
            x="pending_amount",
            nbins=10,
            title="Distribution of Pending Payments Among Customers",
            color_discrete_sequence=["#fbc02d"]
        )
        st.plotly_chart(fig3, use_container_width=True)

st.caption("📘 Data auto-generated from your C Jewellery Shop program.")

