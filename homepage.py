this is the code
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
    page_icon="💎",  # Changed to diamond for luxury vibe
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize theme
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def get_theme_colors():
    if st.session_state.dark_mode:
        return {
            # === DARK MODE (Bloomberg Terminal Style) ===
            "bg_primary": "#0a0f1a",  # Deep navy
            "bg_secondary": "#1a2236",  # Dark slate blue
            "text_primary": "#e0e6ff",  # Soft blue-white
            "text_secondary": "#8a9bb8",  # Muted slate
            "accent": "#00c896",  # Emerald green
            "accent_secondary": "#ffb74d",  # Gold for highlights
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
            # === LIGHT MODE (Wealth Management Style) ===
            "bg_primary": "#f8fafc",  # Ultra-light gray
            "bg_secondary": "#ffffff",  # Pure white
            "text_primary": "#1e293b",  # Dark slate
            "text_secondary": "#64748b",
            "accent": "#059669",  # Deep emerald
            "accent_secondary": "#d97706",  # Warm gold
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
# 💎 PREMIUM CSS STYLING
# ===========================================
st.markdown(f"""
<style>
    /* === GLOBAL STYLES === */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, .stApp {{
        font-family: 'Inter', sans-serif;
        background-color: {theme["bg_primary"]};
        color: {theme["text_primary"]};
        transition: all 0.3s ease !important;
    }}
    
    /* === HEADER STYLES === */
    h1 {{
        font-weight: 700 !important;
        letter-spacing: -0.03em !important;
        background: linear-gradient(90deg, {theme["accent"]}, {theme["accent_secondary"]});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem !important;
    }}
    
    h2, h3 {{
        font-weight: 600 !important;
        color: {theme["text_primary"]} !important;
    }}
    
    /* === THEME TOGGLE BUTTON (Floating Jewel) === */
    .theme-toggle-container {{
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 999;
    }}
    
    .stButton[data-testid="theme_toggle_btn"] > button {{
        background: {theme["bg_secondary"]} !important;
        color: {theme["accent"]} !important;
        border: 1px solid {theme["accent"]}40 !important;
        border-radius: 12px !important;
        padding: 0.4rem 1rem !important;
        font-weight: 600 !important;
        box-shadow: {theme["shadow"]} !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton[data-testid="theme_toggle_btn"] > button:hover {{
        background: {theme["accent"]}20 !important;
        transform: translateY(-1px);
    }}
    
    /* === BUTTONS (Gemstone Effect) === */
    .stButton > button {{
        background: linear-gradient(135deg, {theme["accent"]}, {theme["button_hover"]}) !important;
        color: {theme["button_text"]} !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: {theme["shadow"]} !important;
        transition: all 0.3s ease !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px {theme["accent"]}30 !important;
    }}
    
    /* === CARDS (Elevated Luxury) === */
    .stMetric, div[data-testid="stMetric"] {{
        background: {theme["card_bg"]} !important;
        border: 1px solid {theme["card_border"]} !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: {theme["shadow"]} !important;
    }}
    
    .custom-card {{
        background: {theme["card_bg"]} !important;
        border: 1px solid {theme["card_border"]} !important;
        border-radius: 16px !important;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: {theme["shadow"]} !important;
        transition: all 0.3s ease !important;
    }}
    
    .custom-card:hover {{
        transform: translateY(-3px);
        box-shadow: 0 12px 24px {theme["accent"]}20 !important;
    }}
    
    /* === INPUTS (Minimalist Chic) === */
    .stSelectbox > div > div, 
    .stNumberInput > div > div,
    .stTextInput > div > div {{
        background: {theme["bg_secondary"]} !important;
        border-radius: 12px !important;
        border: 1px solid {theme["card_border"]} !important;
        transition: all 0.3s ease !important;
    }}
    
    /* === DATAFRAME EDITOR (Premium Spreadsheet) === */
    .stDataEditor {{
        background: {theme["bg_secondary"]} !important;
        border-radius: 16px !important;
        box-shadow: {theme["shadow"]} !important;
        border: 1px solid {theme["card_border"]} !important;
    }}
    
    /* === TABLES (Clean & Airy) === */
    .stDataFrame {{
        border-radius: 12px !important;
    }}
    
    /* === DIVIDERS === */
    hr {{
        border-color: {theme["card_border"]} !important;
        margin: 2rem 0 !important;
    }}
    
    /* === ACCENT ELEMENTS === */
    .accent-gold {{
        color: {theme["accent_secondary"]} !important;
        font-weight: 600;
    }}
    
    .accent-emerald {{
        color: {theme["accent"]} !important;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# ===========================================
# 🎛️ THEME TOGGLE UI
# ===========================================
theme_toggle_container = st.container()
with theme_toggle_container:
    st.markdown('<div class="theme-toggle-container">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns([10, 1, 1])
    with col3:
        theme_icon = "🌙" if not st.session_state.dark_mode else "☀️"
        theme_text = "Dark" if not st.session_state.dark_mode else "Light"
        if st.button(f"{theme_icon} {theme_text}", key="theme_toggle_btn"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# ===========================================
# 📊 DATA & FUNCTIONALITY (With Premium Styling)
# ===========================================
@st.cache_data
def load_data():
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
# 🏆 PREMIUM HEADER
# ===========================================
st.markdown("""
    <h1>💎 StockGennie Pro</h1>
    <p style='text-align:center;font-size:18px;color:%s'>
    Smart Portfolio Analysis & Fundamental Scorecards
    </p>
""" % theme["text_secondary"], unsafe_allow_html=True)

# ===========================================
# 🛒 STOCK SELECTION (Premium Card)
# ===========================================
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

# ===========================================
# 💳 STOCK INFO CARD (Luxury Design)
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
# ➕ ADD TO PORTFOLIO BUTTON (Centered)
# ===========================================
st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
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
# 📈 PORTFOLIO SECTION (Premium Layout)
# ===========================================
if st.session_state.portfolio:
    st.markdown("---")
    st.markdown(f"<h2 style='color:{theme['accent']}'>📈 Portfolio Overview</h2>", unsafe_allow_html=True)

    portfolio_df = pd.DataFrame(list(st.session_state.portfolio.values()))
    total_investment = portfolio_df["Investment"].sum()

    # Premium Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Investment", f"${total_investment:,.2f}")
    col2.metric("Stocks Held", len(portfolio_df))
    avg_score = (portfolio_df["Composite Score"] * portfolio_df["Investment"] / total_investment).sum()
    col3.metric("Weighted Score", f"{avg_score:.1f}/100")

    # Editable Table
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

    # Sync Back to Session
    for idx, row in edited_df.iterrows():
        ticker = row["Ticker"]
        if ticker in st.session_state.portfolio:
            st.session_state.portfolio[ticker]["Quantity"] = int(row["Quantity"])
            st.session_state.portfolio[ticker]["Investment"] = round(
                int(row["Quantity"]) * st.session_state.portfolio[ticker]["Price"], 2
            )

    # ===========================================
    # 🚀 ACTION BUTTONS (Premium Centered Layout)
    # ===========================================
    st.markdown("<div style='margin-top:2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col2:
        generate_clicked = st.button("🚀 Analyze Portfolio", key="generate_btn")
    with col3:
        clear_clicked = st.button("🗑️ Clear All", key="clear_btn")

    if generate_clicked:
        weights = portfolio_df["Investment"] / total_investment
        score = sum(weights * portfolio_df["Composite Score"])

        # Premium Score Display
        st.markdown(f"""
            <div style='background:{theme["success_bg"]}; 
                        padding:2rem; 
                        border-radius:20px; 
                        text-align:center; 
                        margin:2rem 0; 
                        border:1px solid {theme["accent"]}40;
                        box-shadow: {theme["shadow"]}'>
                <h2 style='color:{theme["success_text"]}; margin-bottom:0.5rem;'>Portfolio Quality Score</h2>
                <div style='font-size:3.5rem; font-weight:700; color:{theme["accent"]}'>
                    {score:.1f}<span style='font-size:1.5rem; color:{theme["text_secondary"]}'>/100</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # Luxury Charts
        chart_template = "plotly_dark" if st.session_state.dark_mode else "plotly_white"
        
        # Score Breakdown Chart
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
            font_color=theme["text_primary"],
            hoverlabel=dict(
                bgcolor=theme["accent"],
                font_color=theme["button_text"]
            )
        )
        st.plotly_chart(fig, use_container_width=True)

        # Allocation Pie Chart
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
# 🏁 LUXURY FOOTER
# ===========================================
st.markdown(f"""
    <hr>
    <p style='text-align:center; font-size:0.9rem; color:{theme["text_secondary"]}'>
        © 2024 StockGennie Pro | <span class='accent-gold'>Premium Portfolio Analytics</span>
    </p>
""", unsafe_allow_html=True)
