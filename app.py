import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
plt.style.use('ggplot')

# Title
st.title("📊 Sales Analysis Dashboard")
st.markdown("### Insights on Sales, Profit & Customer Trends")

# Load data
df = pd.read_csv("sales_analysis_dataset.csv")

# Clean column names
df.columns = df.columns.str.strip()

# Sidebar filters
st.markdown("---")
st.sidebar.title("🔍 Filters")
region = st.sidebar.selectbox("Select Region", df['Region'].unique())
category = st.sidebar.selectbox("Select Category", df['Category'].unique())

# Filter data
filtered_df = df[(df['Region'] == region) & (df['Category'] == category)]

# KPIs
st.markdown("## 📌 Key Metrics")
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"{filtered_df['Sales'].sum():,.0f}")
col2.metric("Total Profit", f"{filtered_df['Profit'].sum():,.0f}")
col3.metric("Total Quantity", f"{filtered_df['Quantity'].sum():,.0f}")


st.markdown("---")
st.markdown("## 📊 Visual Insights")

# Chart (using Product instead of Sub-Category)
col1, col2 = st.columns(2)

# 📊 Sales by Product (Top 5 only)
with col1:
    st.subheader("Top 5 Products by Sales")
    
    top_products = (
        filtered_df.groupby('Product')['Sales']
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    
    fig1, ax1 = plt.subplots()
    top_products.plot(kind='bar', ax=ax1, color=['#2196F3', '#4CAF50', '#FFC107', '#FF5722', '#9C27B0'])
    plt.xticks(rotation=30)
    
    st.pyplot(fig1)

# 🥧 Category Share
with col2:
    st.subheader("Category Contribution (Overall)")
    
    cat_data = df.groupby('Category')['Sales'].sum()
    colors = ['#4CAF50', '#2196F3', '#FFC107']
    fig2, ax2 = plt.subplots()
    cat_data.plot(kind='pie', autopct='%1.1f%%', ax=ax2,colors=colors)
    
    st.pyplot(fig2)

st.markdown("---")
#sales trends
st.subheader("Monthly Sales Trend")

df['Order Date'] = pd.to_datetime(df['Order Date'])

monthly_sales = (
    df.groupby(df['Order Date'].dt.to_period('M'))['Sales']
    .sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

fig3, ax3 = plt.subplots()
monthly_sales.plot(ax=ax3)

st.pyplot(fig3)

st.markdown("---")
#top customers
col3, col4 = st.columns(2)

# 📉 Top Customers
with col3:
    st.subheader("Top 5 Customers")
    
    top_customers = (
        df.groupby('Customer')['Sales']
        .sum()
        .sort_values()
        .tail(5)
    )
    
    fig4, ax4 = plt.subplots()
    top_customers.plot(kind='barh', ax=ax4, color='green')
    
    st.pyplot(fig4)

# 📊 Profit by Category
with col4:
    st.subheader("Profit by Category")
    
    profit_data = df.groupby('Category')['Profit'].sum()
    
    fig5, ax5 = plt.subplots()
    profit_data.plot(kind='bar', ax=ax5, color='orange')
    
    st.pyplot(fig5)

#dynamic insights
st.markdown("---")
st.markdown("## 📌 Key Insights")

st.write("• Technology category generates highest sales.")
st.write("• South region contributes most profit.")
st.write("• Central region needs improvement.")
st.write("• Top customers drive majority revenue.")
