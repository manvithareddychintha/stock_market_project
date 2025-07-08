import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Page Config
st.set_page_config(
    page_title="StockGennie Pro | Portfolio Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load Scored Data
@st.cache_data
def load_data():
    df = pd.read_csv(r"filtered_df.csv")
    df["Name_lower"] = df["Name"].str.lower()
    df["Display"] = df["Ticker"] + " - " + df["Name"]
    return df

stock_df = load_data()

# Session State
if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# Header
st.markdown("""
    <h1 style='text-align:center;color:#1f2937'>📊 StockGennie Pro</h1>
    <p style='text-align:center;font-size:18px;color:#64748b'>Smart Portfolio Analysis & Fundamental Scorecards</p>
""", unsafe_allow_html=True)

# Stock Selection
col1, col2 = st.columns([2, 1])
with col1:
    selected_display = st.selectbox("Select Stock", stock_df["Display"])
with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

selected_ticker = selected_display.split(" - ")[0]
selected_row = stock_df[stock_df["Ticker"] == selected_ticker].iloc[0]

# Simulated Price
np.random.seed(hash(selected_ticker) % 2**32)
market_price = np.random.uniform(100, 800)

# Info Card
st.markdown(f"""
<div style='background:#f0fdf4;padding:1.5rem;border-radius:16px;margin-top:1rem;'>
    <h3 style='color:#16a34a'>{selected_row['Name']} ({selected_ticker})</h3>
    <div style='display:flex;justify-content:space-between;'>
        <div><b>Sector:</b> {selected_row['Sub-Sector']}</div>
        <div><b>Market Cap:</b> ₹{selected_row['Market Cap_y']:,.0f} Cr</div>
        <div><b>PE Ratio:</b> {selected_row['PE Ratio_x']:.2f}</div>
        <div><b>Price:</b> ₹{market_price:.2f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Add or Update Portfolio
if st.button("➕ Add to Portfolio"):
    investment_value = quantity * market_price
    if selected_ticker in st.session_state.portfolio:
        existing = st.session_state.portfolio[selected_ticker]
        existing["Quantity"] += quantity
        existing["Investment"] += investment_value
        st.success(f"Updated {selected_row['Name']} with +{quantity} shares.")
    else:
        st.session_state.portfolio[selected_ticker] = {
            "Ticker": selected_ticker,
            "Name": selected_row['Name'],
            "Sub-Sector": selected_row['Sub-Sector'],
            "Quantity": quantity,
            "Price": round(market_price, 2),
            "Investment": round(investment_value, 2),
            "Market Cap": selected_row['Market Cap_y'],
            "PE Ratio": selected_row['PE Ratio_x'],
            "Sector": selected_row['Sub-Sector'],
            "Composite Score": selected_row.get("Composite Score", 0)
        }
        st.success(f"Added {quantity} shares of {selected_row['Name']} to portfolio")

# Portfolio View
if st.session_state.portfolio:
    st.markdown("---")
    st.subheader("📦 Portfolio Overview")

    portfolio_df = pd.DataFrame(list(st.session_state.portfolio.values()))
    total_investment = portfolio_df["Investment"].sum()

    col1, col2 = st.columns(2)
    col1.metric("Total Investment", f"₹{total_investment:,.0f}")
    col2.metric("Stocks Held", len(portfolio_df))

    # Editable Table
    edited_df = st.data_editor(
        portfolio_df[["Ticker", "Name", "Quantity", "Price", "Investment", "PE Ratio", "Market Cap"]],
        use_container_width=True,
        hide_index=True,
        key="portfolio_editor"
    )

    # Sync Back to Session
    for idx, row in edited_df.iterrows():
        ticker = row["Ticker"]
        if ticker in st.session_state.portfolio:
            st.session_state.portfolio[ticker]["Quantity"] = int(row["Quantity"])
            st.session_state.portfolio[ticker]["Investment"] = round(
                int(row["Quantity"]) * st.session_state.portfolio[ticker]["Price"], 2
            )

    portfolio_df = pd.DataFrame(list(st.session_state.portfolio.values()))
    total_investment = portfolio_df["Investment"].sum()

    if st.button("📈 Generate Portfolio Score & Visuals"):
        weights = portfolio_df["Investment"] / total_investment
        score = sum(weights * portfolio_df["Composite Score"])

        st.markdown(f"""
            <div style='background:#ecfdf5;padding:2rem;border-radius:20px;text-align:center;margin:2rem 0;'>
                <h2 style='color:#059669'>Final Portfolio Score: {score:.1f}/100</h2>
            </div>
        """, unsafe_allow_html=True)

        fig = px.bar(
            portfolio_df,
            x="Name",
            y="Composite Score",
            color="Composite Score",
            title="📊 Score Breakdown by Stock",
            color_continuous_scale="Greens"
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.pie(
            portfolio_df,
            names="Sector",
            values="Investment",
            title="💼 Sector Allocation"
        )
        st.plotly_chart(fig2, use_container_width=True)

        avg_pe = (portfolio_df["PE Ratio"] * weights).sum()
        st.markdown(f"### 🧠 Portfolio Average PE Ratio: `{avg_pe:.2f}`")

    if st.button("🗑️ Clear Portfolio"):
        st.session_state.portfolio = {}
        st.rerun()

# Footer
st.markdown("""
    <hr>
    <p style='text-align:center;font-size:0.9rem;color:#94a3b8'>
        ⚠️ Simulated Prices | Educational Use Only | © StockGennie Pro 2024
    </p>
""", unsafe_allow_html=True)
