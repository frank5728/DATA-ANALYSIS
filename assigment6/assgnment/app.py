import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="Supermarket Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("SuperMarket Analysis.csv")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    return df

df = load_data()

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.title("🛒 Supermarket Sales Dashboard")
st.write(
    "An interactive dashboard for exploring supermarket "
    "sales performance."
)

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.header("🔎 Filters")

branch_options = ["All"] + sorted(df["Branch"].dropna().unique().tolist())

selected_branch = st.sidebar.selectbox(
    "Select Branch",
    branch_options
)

product_options = ["All"] + sorted(
    df["Product line"].dropna().unique().tolist()
)

selected_product = st.sidebar.selectbox(
    "Select Product Line",
    product_options
)

customer_options = ["All"] + sorted(
    df["Customer type"].dropna().unique().tolist()
)

selected_customer = st.sidebar.selectbox(
    "Select Customer Type",
    customer_options
)

# ---------------------------------------------------------
# FILTER DATA
# ---------------------------------------------------------
filtered_df = df.copy()

if selected_branch != "All":
    filtered_df = filtered_df[
        filtered_df["Branch"] == selected_branch
    ]

if selected_product != "All":
    filtered_df = filtered_df[
        filtered_df["Product line"] == selected_product
    ]

if selected_customer != "All":
    filtered_df = filtered_df[
        filtered_df["Customer type"] == selected_customer
    ]

# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------
total_sales = filtered_df["Sales"].sum()
total_quantity = filtered_df["Quantity"].sum()
transactions = len(filtered_df)

average_sale = (
    filtered_df["Sales"].mean()
    if transactions > 0 else 0
)

average_rating = (
    filtered_df["Rating"].mean()
    if transactions > 0 else 0
)

total_gross_income = filtered_df["gross income"].sum()

st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Sales",
        f"{total_sales:,.2f}"
    )

with col2:
    st.metric(
        "Quantity Sold",
        f"{total_quantity:,}"
    )

with col3:
    st.metric(
        "Transactions",
        f"{transactions:,}"
    )

with col4:
    st.metric(
        "Average Sale",
        f"{average_sale:,.2f}"
    )

col5, col6 = st.columns(2)

with col5:
    st.metric(
        "Average Rating",
        f"{average_rating:.2f}"
    )

with col6:
    st.metric(
        "Gross Income",
        f"{total_gross_income:,.2f}"
    )

# ---------------------------------------------------------
# SALES BY PRODUCT LINE
# ---------------------------------------------------------
st.subheader("🛍️ Sales by Product Line")

sales_product = (
    filtered_df.groupby("Product line")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_product = px.bar(
    sales_product,
    x="Product line",
    y="Sales",
    title="Total Sales by Product Line",
    text_auto=".2s"
)

st.plotly_chart(
    fig_product,
    width='stretch'
)

# ---------------------------------------------------------
# BRANCH ANALYSIS
# ---------------------------------------------------------
st.subheader("🏢 Sales by Branch")

sales_branch = (
    filtered_df.groupby("Branch")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig_branch = px.bar(
    sales_branch,
    x="Branch",
    y="Sales",
    title="Total Sales by Branch",
    text_auto=".2s"
)

st.plotly_chart(
    fig_branch,
    width='stretch'
)

# ---------------------------------------------------------
# MONTHLY SALES TREND
# ---------------------------------------------------------
st.subheader("📈 Sales Trend")

filtered_df = filtered_df.copy()
filtered_df["Month"] = (
    filtered_df["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
    .reset_index()
)

fig_trend = px.line(
    monthly_sales,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

st.plotly_chart(
    fig_trend,
    width='stretch'
)

# ---------------------------------------------------------
# PAYMENT METHOD
# ---------------------------------------------------------
st.subheader("💳 Payment Methods")

payment_data = (
    filtered_df["Payment"]
    .value_counts()
    .reset_index()
)

payment_data.columns = [
    "Payment",
    "Transactions"
]

fig_payment = px.pie(
    payment_data,
    names="Payment",
    values="Transactions",
    title="Transactions by Payment Method"
)

st.plotly_chart(
    fig_payment,
    width='stretch'
)

# ---------------------------------------------------------
# QUANTITY VS SALES
# ---------------------------------------------------------
st.subheader("🔵 Quantity vs Sales")

fig_scatter = px.scatter(
    filtered_df,
    x="Quantity",
    y="Sales",
    color="Product line",
    hover_data=[
        "Branch",
        "City",
        "Customer type",
        "Payment",
        "Rating"
    ],
    title="Relationship Between Quantity and Sales"
)

st.plotly_chart(
    fig_scatter,
    width='stretch'
)

# ---------------------------------------------------------
# CUSTOMER TYPE
# ---------------------------------------------------------
st.subheader("👥 Sales by Customer Type")

customer_sales = (
    filtered_df.groupby("Customer type")["Sales"]
    .sum()
    .reset_index()
)

fig_customer = px.bar(
    customer_sales,
    x="Customer type",
    y="Sales",
    title="Sales by Customer Type",
    text_auto=".2s"
)

st.plotly_chart(
    fig_customer,
    width='stretch'
)

# ---------------------------------------------------------
# DATA TABLE
# ---------------------------------------------------------
st.subheader("📋 Transaction Data")

st.dataframe(
    filtered_df,
    width='stretch',
    hide_index=True
)

st.caption(
    "Supermarket Sales Analysis — Jupyter Notebook → Streamlit Dashboard"
)
