import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# 1. App ka Title
st.title("🚀 Smart Stock Analyzer")
st.write("Apna stock symbol likhein aur trend check karein!")

# 2. User Input
user_input = st.text_input("Enter Ticker (e.g. AAPL, TSLA, BTC-USD):", "AAPL")

if user_input:
    # Data fetch karna
    # 'multi_level_index=False' error se bachne ke liye add kiya hai
    df = yf.download(user_input, period="1y", multi_level_index=False)
    
    if not df.empty:
        # 20-day Moving Average calculation
        df['SMA20'] = df['Close'].rolling(window=20).mean()

        # Graph dikhana
        fig, ax = plt.subplots()
        ax.plot(df.index, df['Close'], label='Price', color='blue')
        ax.plot(df.index, df['SMA20'], label='20-Day Trend', color='red')
        ax.legend()
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Simple Advice Logic
        # .item() use kiya hai taake sirf ek value mile, Series nahi
        last_price = df['Close'].iloc[-1].item()
        last_sma = df['SMA20'].iloc[-1].item()
        
        st.subheader("Market Analysis:")
        if last_price > last_sma:
            st.success(f"✅ Mashwara: {user_input} is looking Strong (Bullish)!")
        else:
            st.error(f"⚠️ Mashwara: {user_input} is looking Weak (Bearish)!")
    else:
        st.warning("Symbol sahi nahi hai ya data nahi mil raha.")
        # 1. Data ko CSV format (Excel readable) mein badlein
csv_data = df.to_csv().encode('utf-8')

# 2. Sidebar ya neechay aik Download Button banayein
st.download_button(
    label="📥 Download Data as CSV",
    data=csv_data,
    file_name=f"{user_input}_market_data.csv",
    mime='text/csv',
)
st.header("📊 Portfolio Check")

import streamlit as st
import yfinance as yf

st.title("📊 Pro Portfolio Tracker")

# Symbol input
ticker = st.text_input("Enter Ticker (e.g. AAPL, BTC-USD, ENGRO.KA):", "AAPL")

# 1. Data Fetching with Fix
try:
    # multi_level_index=False bohat zaroori hai error khatam karne ke liye
    df = yf.download(ticker, period="1d", multi_level_index=False)

    if not df.empty:
        # Latest price nikalna (item() use kiya taake sirf number mile)
        latest_price = df['Close'].iloc[-1].item()
        st.info(f"Current Market Price of {ticker}: **Rs. {latest_price:.2f}**")

        # Portfolio Inputs
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            buy_price = st.number_input("Your Buy Price", min_value=0.1, value=latest_price)
        with col_in2:
            quantity = st.number_input("Quantity", min_value=1, value=10)

        # 2. Calculation Logic (The Math)
        invested_value = buy_price * quantity
        current_value = latest_price * quantity
        profit_loss = current_value - invested_value
        
        # Percentage Calculation (Zero Division error se bachne ke liye)
        p_l_percent = (profit_loss / invested_value) * 100 if invested_value > 0 else 0

        # 3. Display Metrics
        st.divider()
        m1, m2, m3 = st.columns(3)
        m1.metric("Invested", f"{invested_value:,.2f}")
        m2.metric("Current Value", f"{current_value:,.2f}")
        # Profit green hoga, loss red (delta parameter se)
        m3.metric("Profit / Loss", f"{profit_loss:,.2f}", f"{p_l_percent:.2f}%")

    else:
        st.warning("Symbol sahi likhein (e.g. AAPL or TSLA)")

except Exception as e:
    st.error(f"Kuch masla hai: {e}")