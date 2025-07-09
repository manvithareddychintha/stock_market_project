import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ===========================================
# 🎨 ULTRA-PREMIUM THEME SETUP
# ===========================================
st.set_page_config(
    page_title="StockGennie Pro | Portfolio Management",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            "bg_primary": "#0a0f1a",
            "bg_secondary": "#1a2236",
            "text_primary": "#e0e6ff",
            "text_secondary": "#8a9bb8",
            "accent": "#00c896",
            "accent_secondary": "#ffb74d",
            "card_bg": "#1a2236",
            "card_border": "#2a3a5a",
            "success_bg": "#0d2b26",
            "success_text": "#00c896",
            "info_bg": "#1a2a4a",
            "info_text": "#4dabf7",
            "button_bg": "#00c896",
            "button_text": "#0a0f1a",
            "button_hover": "#00a57a",
            "button_border": "#00c896",
            "shadow": "0 8px 32px rgba(0, 200, 150, 0.1)",
            "chart_bg": "#1a2236",
            "plot_bg": "#141b2d"
        }
    else:
        return {
            "bg_primary": "#f8fafc",
            "bg_secondary": "#ffffff",
            "text_primary": "#1e293b",
            "text_secondary": "#64748b",
            "accent": "#059669",
            "accent_secondary": "#d97706",
            "card_bg": "#ffffff",
            "card_border": "#e2e8f0",
            "success_bg": "#ecfdf5",
            "success_text": "#059669",
            "info_bg": "#eff6ff",
            "info_text": "#2563eb",
            "button_bg": "#059669",
            "button_text": "#ffffff",
            "button_hover": "#047857",
            "button_border": "#059669",
            "shadow": "0 8px 24px rgba(5, 150, 105, 0.12)",
            "chart_bg": "#ffffff",
            "plot_bg": "#f1f5f9"
        }

theme = get_theme_colors()

# ===========================================
# 📈 DATA LOADING
# ===========================================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("filtered_df.csv")
        df["Display"] = df["Ticker"] + " - " + df["Name"]
    except FileNotFoundError:
        st.warning("⚠️ Could not find `filtered_df.csv`. Using demo data.")
        df = pd.DataFrame({
            "Ticker": ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"],
            "Name": ["Apple", "Microsoft", "Tesla", "Amazon", "Google"],
            "Sub-Sector": ["Technology", "Technology", "Automotive", "E-Commerce", "Technology"],
            "Market Cap_y": [2800000, 2500000, 800000, 1800000, 1700000],
            "PE Ratio_x": [28.5, 32.1, 110.2, 58.7, 24.3],
            "Composite Score": [88, 92, 76, 85, 90]
        })
        df["Display"] = df["Ticker"] + " - " + df["Name"]
    return df

stock_df = load_data()

if "portfolio" not in st.session_state:
    st.session_state.portfolio = {}

# ===========================================
# 🌟 HEADER
# ===========================================
st.markdown(f"""
    <h1>💎 StockGennie Pro</h1>
    <p style='text-align:center;font-size:18px;color:{theme["text_secondary"]}'>
        Smart Portfolio Analysis & Fundamental Scorecards
    </p>
""", unsafe_allow_html=True)

# ===========================================
# 🛒 STOCK SELECTION
# ===========================================
col1, col2 = st.columns([2, 1])
with col1:
    selected_display = st.selectbox("Select Stock", stock_df["Display"])
with col2:
    quantity = st.number_input("Quantity", min_value=1, value=1, step=1)

selected_ticker = selected_display.split(" - ")[0]
selected_row = stock_df[stock_df["Ticker"] == selected_ticker].iloc[0]

# Simulate Price
np.random.seed(hash(selected_ticker) % 2**32)
market_price = np.random.uniform(100, 800)

# ===========================================
# 💳 STOCK CARD
# ===========================================
st.markdown(f"""
<div class='custom-card'>
    <h3 style='color:{theme["accent"]}'>{selected_row['Name']} <span class='accent-gold'>({selected_ticker})</span></h3>
    <div style='display:flex; justify-content:space-between; flex-wrap:wrap; gap:1rem; margin-top:1rem;'>
        <div><b>Sector:</b> {selected_row['Sub-Sector']}</div>
        <div><b>Market Cap:</b> <span class='accent-emerald'>${selected_row['Market Cap_y']/1000:,.1f}B</span></div>
        <div><b>PE Ratio:</b> {selected_row['PE Ratio_x']:.1f}</div>
        <div><b>Current Price:</b> <span class='accent-emerald'>${market_price:,.2f}</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ===========================================
# ➕ ADD TO PORTFOLIO
# ===========================================
col1, col2, col3 = st.columns([1, 2, 1])
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
            "Composite Score": selected_row.get("Composite Score", 0)
        }
        st.success(f"Added {quantity} shares of {selected_row['Name']} to portfolio")

# ===========================================
# 📊 PORTFOLIO OVERVIEW
# ===========================================
if st.session_state.portfolio:
    st.markdown("---")
    st.markdown(f"<h2 style='color:{theme['accent']}'>📈 Portfolio Overview</h2>", unsafe_allow_html=True)

    portfolio_df = pd.DataFrame(list(st.session_state.portfolio.values()))
    total_investment = portfolio_df["Investment"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Investment", f"${total_investment:,.2f}")
    col2.metric("Stocks Held", len(portfolio_df))
    avg_score = (portfolio_df["Composite Score"] * portfolio_df["Investment"] / total_investment).sum()
    col3.metric("Weighted Score", f"{avg_score:.1f}/100")

    edited_df = st.data_editor(
        portfolio_df[["Ticker", "Name", "Quantity", "Price", "Investment", "PE Ratio"]],
        column_config={
            "Price": st.column_config.NumberColumn(format="$%.2f"),
            "Investment": st.column_config.NumberColumn(format="$%.2f")
        },
        use_container_width=True,
        hide_index=True,
        key="portfolio_editor"
    )

    for idx, row in edited_df.iterrows():
        ticker = row["Ticker"]
        if ticker in st.session_state.portfolio:
            st.session_state.portfolio[ticker]["Quantity"] = int(row["Quantity"])
            st.session_state.portfolio[ticker]["Investment"] = round(
                int(row["Quantity"]) * st.session_state.portfolio[ticker]["Price"], 2
            )

    # Buttons
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        generate_clicked = st.button("🚀 Analyze Portfolio", key="generate_btn")
    with col3:
        clear_clicked = st.button("🗑️ Clear All", key="clear_btn")

    if generate_clicked:
        weights = portfolio_df["Investment"] / total_investment
        score = sum(weights * portfolio_df["Composite Score"])

        st.markdown(f"""
            <div style='background:{theme["success_bg"]}; padding:2rem; border-radius:20px; 
                        text-align:center; margin:2rem 0; border:1px solid {theme["accent"]}40;
                        box-shadow: {theme["shadow"]}'>
                <h2 style='color:{theme["success_text"]}; margin-bottom:0.5rem;'>Portfolio Quality Score</h2>
                <div style='font-size:3.5rem; font-weight:700; color:{theme["accent"]}'>
                    {score:.1f}<span style='font-size:1.5rem; color:{theme["text_secondary"]}'>/100</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        chart_template = "plotly_dark" if st.session_state.dark_mode else "plotly_white"

        fig = px.bar(
            portfolio_df.sort_values("Composite Score", ascending=False),
            x="Name",
            y="Composite Score",
            color="Composite Score",
            color_continuous_scale="Emrld",
            title="<b>📊 Fundamental Score by Holding</b>",
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
            names="Sub-Sector",
            values="Investment",
            title="<b>🥧 Sector Allocation</b>",
            color_discrete_sequence=px.colors.sequential.Emrld,
            template=chart_template
        )
        fig2.update_layout(
            paper_bgcolor=theme["bg_primary"],
            font_color=theme["text_primary"]
        )
        st.plotly_chart(fig2, use_container_width=True)

    if clear_clicked:
        st.session_state.portfolio = {}
        st.rerun()

# ===========================================
# 🌟 FOOTER
# ===========================================
st.markdown(f"""
    <hr>
    <p style='text-align:center; font-size:0.9rem; color:{theme["text_secondary"]}'>
        © 2024 StockGennie Pro | <span class='accent-gold'>Premium Portfolio Analytics</span>
    </p>
""", unsafe_allow_html=True)

