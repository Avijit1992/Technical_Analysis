import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import date, timedelta
import plotly.express as px

# Define a list of supported stock tickers
ticker_list = ["AAPL", "GOOG", "AMZN", "TSLA", "MSFT"]

# Get today's date and set default start date one month earlier
today = date.today()
default_start_date = today - timedelta(days=30)

# Create Streamlit app
st.title("Stock Price Dashboard with Bollinger Bands and SMA")

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

# Download stock data
try:
    df = yf.download(selected_ticker, start=start_date, end=end_date)
except Exception as e:
    st.error(f"Error downloading data for {selected_ticker}: {e}")
    st.stop()

# Calculate Bollinger Bands
df["Upper Band"] = df["Close"] + 2 * df["Close"].rolling(window=20).std()
df["Lower Band"] = df["Close"] - 2 * df["Close"].rolling(window=20).std()

# Calculate SMA
df["SMA"] = df["Close"].rolling(window=sma_period).mean()

# Create Bollinger Band chart
fig1 = px.line(
    df,
    x=df.index,
    y=["Close", "Upper Band", "Lower Band"],
    title=f"{selected_ticker} Stock Price with Bollinger Bands (Start: {start_date:%Y-%m-%d}, End: {end_date:%Y-%m-%d})",
    labels={"Close": "Close Price", "Upper Band": "Upper Band", "Lower Band": "Lower Band"},
)

# Create SMA chart
fig2 = px.line(
    df,
    x=df.index,
    y=["Close", "SMA"],
    title=f"{selected_ticker} Stock Price with SMA ({sma_period}-day) (Start: {start_date:%Y-%m-%d}, End: {end_date:%Y-%m-%d})",
    labels={"Close": "Close Price", "SMA": f"SMA ({sma_period})"},
)

# Add chart descriptions
st.write("Bollinger Bands are a technical analysis indicator that uses volatility to create 'bands' around a moving average. The bands are typically 2 standard deviations above and below the moving average. When the bands widen, it may indicate increased volatility, while narrowing bands may suggest decreased volatility.")


# Display charts
st.plotly_chart(fig1)


st.write("The Simple Moving Average (SMA) is a technical indicator that calculates the average price of a security over a specified period of time.")
st.plotly_chart(fig2)
