import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Page Config
st.set_page_config(
    page_title="StockGennie Pro | Portfolio Management",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme in session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

# Theme Toggle Function
def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# Theme Variables
def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            "bg_primary": "#1f2937",
            "bg_secondary": "#374151",
            "text_primary": "#f9fafb",
            "text_secondary": "#d1d5db",
            "accent": "#10b981",
            "card_bg": "#374151",
            "success_bg": "#064e3b",
            "success_text": "#10b981",
            "info_bg": "#1e3a8a",
            "info_text": "#3b82f6"
        }
    else:
        return {
            "bg_primary": "#ffffff",
            "bg_secondary": "#f9fafb",
            "text_primary": "#1f2937",
            "text_secondary": "#64748b",
            "accent": "#059669",
            "card_bg": "#f0fdf4",
            "success_bg": "#ecfdf5",
            "success_text": "#059669",
            "info_bg": "#eff6ff",
            "info_text": "#2563eb"
        }

theme = get_theme_colors()

# Apply Global Theme CSS
st.markdown(f"""
<style>
    .stApp {{
        background-color: {theme["bg_primary"]};
        color: {theme["text_primary"]};
    }}
    .theme-toggle {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
        background-color: {theme["accent"]};
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    .theme-toggle:hover {{
        opacity: 0.8;
    }}
</style>
""", unsafe_allow_html=True)

# Theme Toggle HTML Button
theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
theme_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"

st.markdown(f"""
<form method="POST">
    <button class="theme-toggle" name="theme_toggle" type="submit">{theme_icon} {theme_text}</button>
</form>
""", unsafe_allow_html=True)

if st.session_state.get("_theme_toggle_submitted"):
    toggle_theme()
    st.session_state["_theme_toggle_submitted"] = False
    st.rerun()

if st.experimental_get_query_params().get("theme_toggle") is not None:
    st.session_state["_theme_toggle_submitted"] = True

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

# Theme Toggle Button
col1, col2, col3 = st.columns([1, 1, 1])
with col3:
    theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
    theme_text = "Dark Mode" if not st.session_state.dark_mode else "Light Mode"
    if st.button(f"{theme_icon} {theme_text}", key="theme_toggle"):
        toggle_theme()
        st.rerun()

# Header
st.markdown(f"""
    <h1 style='text-align:center;color:{theme["text_primary"]}'>📊 StockGennie Pro</h1>
    <p style='text-align:center;font-size:18px;color:{theme["text_secondary"]}'>Smart Portfolio Analysis & Fundamental Scorecards</p>
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
<div style='background:{theme["card_bg"]};padding:1.5rem;border-radius:16px;margin-top:1rem;border:1px solid {theme["text_secondary"]}20;'>
    <h3 style='color:{theme["accent"]}'>{selected_row['Name']} ({selected_ticker})</h3>
    <div style='display:flex;justify-content:space-between;color:{theme["text_primary"]};'>
        <div><b>Sector:</b> {selected_row['Sub-Sector']}</div>
        <div><b>Market Cap:</b> ₹{selected_row['Market Cap_y']:,.0f} Cr</div>
        <div><b>PE Ratio:</b> {selected_row['PE Ratio_x']:.2f}</div>
        <div><b>Price:</b> ₹{market_price:.2f}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ➕ Add to Portfolio Button (centered with 20px top margin)
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    add_clicked = st.button("➕ Add to Portfolio", key="add_btn")

if add_clicked:
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
    st.subheader("📈 Portfolio Overview")

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

    # 🚀 Generate + 🗑️ Clear Buttons (centered with same size)
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
    with col2:
        generate_clicked = st.button("🚀 Generate Portfolio", key="generate_btn")
    with col4:
        clear_clicked = st.button("🗑️ Clear Portfolio", key="clear_btn")

    if generate_clicked:
        weights = portfolio_df["Investment"] / total_investment
        score = sum(weights * portfolio_df["Composite Score"])

        st.markdown(f"""
            <div style='background:{theme["success_bg"]};padding:2rem;border-radius:20px;text-align:center;margin:2rem 0;border:1px solid {theme["accent"]}40;'>
                <h2 style='color:{theme["success_text"]}'>Final Portfolio Score: {score:.1f}/100</h2>
            </div>
        """, unsafe_allow_html=True)

        # Theme-aware charts
        chart_template = "plotly_dark" if st.session_state.dark_mode else "plotly_white"
        
        fig = px.bar(
            portfolio_df,
            x="Name",
            y="Composite Score",
            color="Composite Score",
            title="📊 Score Breakdown by Stock",
            color_continuous_scale="Greens",
            template=chart_template
        )
        fig.update_layout(
            paper_bgcolor=theme["bg_primary"],
            plot_bgcolor=theme["bg_secondary"],
            font_color=theme["text_primary"]
        )
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.pie(
            portfolio_df,
            names="Sector",
            values="Investment",
            title="🥧 Sector Allocation",
            template=chart_template
        )
        fig2.update_layout(
            paper_bgcolor=theme["bg_primary"],
            font_color=theme["text_primary"]
        )
        st.plotly_chart(fig2, use_container_width=True)

        avg_pe = (portfolio_df["PE Ratio"] * weights).sum()
        st.markdown(f"### 📊 Portfolio Average PE Ratio: `{avg_pe:.2f}`")

    if clear_clicked:
        st.session_state.portfolio = {}
        st.rerun()

# Footer
st.markdown(f"""
    <hr style='border-color:{theme["text_secondary"]}40;'>
    <p style='text-align:center;font-size:0.9rem;color:{theme["text_secondary"]}'>
        ⚠️ Simulated Prices | Educational Use Only | © StockGennie Pro 2024
    </p>
""", unsafe_allow_html=True)
