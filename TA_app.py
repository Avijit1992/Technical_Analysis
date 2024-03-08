import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import plotly.express as px

# Define a list of supported stock tickers
ticker_list = ["HDFCBANK.NS", "DLF.NS", "TCS.NS", "INFY.NS", "ITC.NS"]

# Get today's date and set default start date one month earlier
today = date.today()
default_start_date = today - timedelta(days=100)

# Create Streamlit app
st.title("Technical Analysis of stock price")

# Create sidebar for user input
with st.sidebar:
    selected_ticker = st.selectbox("Select Stock:", ticker_list)
    start_date = st.date_input("Start Date:", default_start_date)
    end_date = st.date_input("End Date:", today)
    sma_period = st.number_input("SMA Period:", min_value=1, value=20)

# Ensure start date is before or equal to end date
if start_date > end_date:
    st.error("Start date must be before or equal to end date.")
    st.stop()

# ignore
#df = yf.download("DLF.NS", start=default_start_date, end=today)
#sma_period = 20

# Download stock data
try:
    df = yf.download(selected_ticker, start=start_date, end=end_date)
except Exception as e:
    st.error(f"Error downloading data for {selected_ticker}: {e}")
    st.stop()

# Calculate SMA
df["SMA"] = df["Close"].rolling(window=sma_period).mean()

custom_colors = {'Close': 'blue', 'SMA': 'red'}

# Plot SMA
fig_SMA = px.line(
    df,
    x=df.index,
    y=["Close", "SMA"],
    title=f"{selected_ticker} Stock Price with SMA ({sma_period}-day) (Start: {start_date:%Y-%m-%d}, End: {end_date:%Y-%m-%d})",
    labels={"Close": "Close Price", "SMA": f"SMA ({sma_period})"},
    color_discrete_map=custom_colors
)

# Add chart descriptions
st.write("The Simple Moving Average (SMA) is a technical indicator that calculates the average price of a security over a specified period of time.")
# Display charts
st.plotly_chart(fig_SMA)

# 

# Define EMA (Exponential Moving Average) function
def calculate_ema(data, window):
  return data.ewm(span=window, min_periods=window, adjust=False).mean()

# Calculate MACD (fast EMA minus slow EMA)
sma_fast = calculate_ema(df['Close'], 12)  # Fast Window - 12
sma_slow = calculate_ema(df['Close'], 26)  # Slow Window - 26
macd = sma_fast - sma_slow

# Calculate Signal Line (EMA of MACD)
signal_line = calculate_ema(macd, 9)  # Signal window - 9

# Add MACD and Signal Line to DataFrame
df['MACD'] = macd
df['Signal Line'] = signal_line

custom_colors = {'MACD': 'green', 'Signal Line': 'black'}
# Plot MACD
fig_MACD = px.line(
    df,
    x=df.index,
    y=[ "MACD", "Signal Line"],  # Include Close price for reference
    title=f"{selected_ticker} Stock Price with MACD (Fast: 12 Days, Slow: 26 Days, Signal: 9 Days)",
    labels={ "MACD": "MACD", "Signal Line": "Signal Line"},
    color_discrete_map=custom_colors
)

# Add chart descriptions

st.write("""The MACD indicator was developed by Gerald Appel and is designed to show the relationship between two moving averages of an asset's price. Typically, the MACD is calculated using the 26-day exponential moving average (EMA) and the 12-day EMA. The MACD line is derived by subtracting the 26-day EMA from the 12-day EMA.
The MACD indicator also includes a signal line, which is a 9-day EMA of the MACD line. The signal line helps traders identify potential buy or sell signals based on crossovers with the MACD line.
When the MACD line crosses above the signal line, it is considered a bullish signal, indicating a potential buying opportunity. Conversely, when the MACD line crosses below the signal line, it is seen as a bearish signal, suggesting a possible selling opportunity.""")
# Display charts
st.plotly_chart(fig_MACD)

# Calculate the MACD Histogram (MACD minus Signal Line)
df['MACD Histogram'] = df['MACD'] - df['Signal Line']

fig_MACD_hist = px.bar(
    df,  
    x=df.index,  
    y='MACD Histogram',  # Y-axis (histogram values)
    title=f"{selected_ticker} Stock Price with MACD Histogram (Fast: 12 Days, Slow: 26 Days, Signal: 9 Days)",
    labels={"MACD Histogram": "MACD Histogram"},  
    barmode='stack'
)

st.write("""The MACD histogram, which represents the difference between the MACD line and the signal line, can help traders visualize the momentum of a trend. 
         Positive histogram values indicate bullish momentum, while negative values suggest bearish momentum.""")
# Display charts
st.plotly_chart(fig_MACD_hist)
