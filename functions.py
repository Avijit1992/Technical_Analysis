def calculate_ema(data, window):
  return data.ewm(span=window, min_periods=window, adjust=False).mean()

def explain_sma_ema():
  """Displays explanation of SMA and EMA"""
  st.write("**Trend direction:**")
  st.markdown("* Both SMA and EMA can be used to identify the overall trend. If the indicator is rising, it suggests an uptrend, and vice versa. You might consider buying during uptrends and selling during downtrends.")
  st.write("**Support and resistance:**")
  st.markdown("* A rising SMA/EMA can act as support, meaning the price might find buyers around that level. Conversely, a falling SMA/EMA can act as resistance, where the price might face selling pressure. You might consider buying near support and selling near resistance.")
  st.write("**Crossovers:**")
  st.markdown("* Traders sometimes look for crossovers between the price and the SMA/EMA. For example, if the price crosses above the EMA, it might signal a potential buying opportunity. The opposite (price crossing below EMA) might indicate a potential sell signal.")


def explain_macd():
  """Displays explanation of MACD"""
  st.write("**The MACD Indicator:**")
  st.markdown("* The MACD (Moving Average Convergence Divergence) is a technical indicator used to identify trend direction, momentum, and potential buying and selling opportunities.")
  st.write("**Components:**")
  st.markdown("* **MACD Line:** Represents the difference between two exponential moving averages (EMAs) of a security's price. A positive MACD suggests bullish momentum, while a negative MACD indicates bearish momentum.")
  st.markdown("* **Signal Line:** A shorter-term EMA of the MACD line, used to smooth out fluctuations and confirm trend signals.")
  st.write("**Interpretations:**")
  st.markdown("* **Crossovers:** When the MACD line crosses above the signal line, it might signal a potential **bullish** opportunity. Conversely, a crossover below the signal line could suggest a **bearish** signal.")
  st.markdown("* **Divergence:** When the price and MACD move in opposite directions (e.g., price continues to rise while MACD falls), it can indicate a potential **divergence** and a possible trend reversal.")
