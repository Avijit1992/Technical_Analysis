import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import plotly.express as px
import plotly.graph_objects as go
import requests

url = 'https://raw.githubusercontent.com/Avijit1992/Technical_Analysis/main/functions.py'
response = requests.get(url)

with open('functions.py', 'wb') as f:
    f.write(response.content)

import functions as fn



st.set_page_config(layout='wide')

# Define a list of supported stock tickers
ticker_list = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'ICICIBANK.NS', 'INFY.NS', 'HINDUNILVR.NS', 'BHARTIARTL.NS', 'ITC.NS', 
               'SBIN.NS', 'LICI.NS', 'LT.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'KOTAKBANK.NS', 'AXISBANK.NS', 'ASIANPAINT.NS', 
               'TITAN.NS', 'ADANIENT.NS', 'MARUTI.NS', 'ULTRACEMCO.NS', 'SUNPHARMA.NS', 'NTPC.NS', 'BAJAJFINSV.NS', 'DMART.NS', 'TATAMOTORS.NS', 'ONGC.NS', 'NESTLEIND.NS', 'ADANIGREEN.NS', 'WIPRO.NS', 'COALINDIA.NS']

# Get today's date and set default start date one month earlier
today = date.today()
default_start_date = today - timedelta(days=100)

# Create sidebar for user input
with st.sidebar:
    selected_ticker = st.selectbox("Select Stock:", ticker_list)
    start_date = st.date_input("Start Date:", default_start_date)
    end_date = st.date_input("End Date:", today)
    sma_period = st.number_input("SMA Period:", min_value=1, value=20)  

    # Add the multiselection dropdown
    selected_charts = st.multiselect(
        "Select Charts to Display:",
        ("SMA/EMA Chart", "MACD Chart","PSAR")
    
    )

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

# Calculate SMA and EMA
df["SMA"] = df["Close"].rolling(window=sma_period).mean()
df['EMA'] = df["Close"].ewm(span=sma_period, min_periods=sma_period, adjust=False).mean()

custom_colors = {'Close': 'blue', 'SMA': 'red', 'EMA':'black'}


# Plot SMA
fig_SMA = px.line(
    df,
    x=df.index,
    y=["Close", "SMA", "EMA"],
    title=f"{selected_ticker} Stock Price with SMA ({sma_period}-day) (Start: {start_date:%Y-%m-%d}, End: {end_date:%Y-%m-%d})",
    labels={"Close": "Close Price", "SMA": f"SMA ({sma_period})","EMA": f"EMA ({sma_period})"},
    color_discrete_map=custom_colors
)

 

# # Define EMA (Exponential Moving Average) function
# def calculate_ema(data, window):
#   return data.ewm(span=window, min_periods=window, adjust=False).mean()
# Calculate MACD (fast EMA minus slow EMA)
sma_fast = fn.calculate_ema(df['Close'], 12)  # Fast Window - 12
sma_slow = fn.calculate_ema(df['Close'], 26)  # Slow Window - 26
macd = sma_fast - sma_slow

# Calculate Signal Line (EMA of MACD)
signal_line = fn.calculate_ema(macd, 9)  # Signal window - 9

# Add MACD and Signal Line to DataFrame
df['MACD'] = macd
df['Signal Line'] = signal_line

df2 = df.dropna()

custom_colors = {'MACD': 'green', 'Signal Line': 'black'}
# Plot MACD
fig_MACD = px.line(
    df2,
    x=df2.index,
    y=[ "MACD", "Signal Line"],  # Include Close price for reference
    title=f"{selected_ticker} Stock Price with MACD (Fast: 12 Days, Slow: 26 Days, Signal: 9 Days)",
    labels={ "MACD": "MACD", "Signal Line": "Signal Line"},
    color_discrete_map=custom_colors
)

# Add chart descriptions
# Calculate the MACD Histogram (MACD minus Signal Line)
df2['MACD Histogram'] = df2['MACD'] - df2['Signal Line']

fig_MACD_hist = px.bar(
    df2,  
    x=df2.index,  
    y='MACD Histogram',  # Y-axis (histogram values)
    title=f"{selected_ticker} Stock Price with MACD Histogram (Fast: 12 Days, Slow: 26 Days, Signal: 9 Days)",
    labels={"MACD Histogram": "MACD Histogram"},  
    barmode='stack'
)

# # Add PSAR to DataFrame
# df['PSAR'] = calculate_psar(df['High'])  # Assuming PSAR based on High prices

# Calculate PSAR
df['PSAR'] = fn.calculate_psar(df['High'])  # Assuming PSAR based on High prices

# Customize colors (optional)
custom_colors = {'Close': 'blue', 'SMA': 'red', 'EMA': 'black', 'PSAR': 'purple'}  # Add PSAR color

# Plot SMA/EMA with PSAR (modify fig_SMA_EMA)
fig_SMA_EMA_PSA = px.line(
    df,
    x=df.index,
    y=["Close", "SMA", "EMA", "PSAR"],  # Include PSAR
    title=f"{selected_ticker} Stock Price with SMA ({sma_period}-day), EMA ({sma_period}-day), and PSAR",
    labels={
        "Close": "Close Price",
        "SMA": f"SMA ({sma_period})",
        "EMA": f"EMA ({sma_period})",
        "PSAR": "PSAR"
    },
    color_discrete_map=custom_colors,
    range_y=[df['Low'].min() - (df['High'].max() - df['Low'].min()) * 0.1,  # Adjust y-axis range for PSAR visibility
              df['High'].max() + (df['High'].max() - df['Low'].min()) * 0.1]  # Adjust y-axis range for PSAR visibility
)


# Create Streamlit app
st.title("Technical Analysis of stock price")

# Only display selected charts based on user choice
if "SMA/EMA Chart" in selected_charts:
    st.subheader("SMA (Simple Moving Average) and EMA (Exponential Moving Average)")
    # Call the function to display the explanation
    fn.explain_sma_ema()
    # Display charts
    st.plotly_chart(fig_SMA)
    # ... (original SMA/EMA chart code)

if "MACD Chart" in selected_charts:
    st.subheader("Moving Average Convergence/Divergence")
    # Call the function to display the explanation
    fn.explain_macd()
    # Display charts
    st.plotly_chart(fig_MACD)
    st.markdown("""* The MACD histogram, which represents the difference between the MACD line and the signal line, can help traders visualize the momentum of a trend. 
             Positive histogram values indicate bullish momentum, while negative values suggest bearish momentum.""")
    # Display charts
    st.plotly_chart(fig_MACD_hist)
if "PSAR" in selected_charts:
    st.subheader("SMA (Simple Moving Average) and EMA (Exponential Moving Average)")
    st.plotly_chart(fig_SMA_EMA_PSA )
