def download_data_yfinance(credential_path, gsheet_id, ticker_list,start_date=False, new_ticker=False):
    """
    Downloads stock data for a list of tickers from Yahoo Finance and writes it to a Google Sheet.

    Args:
        start_date (datetime): The starting date for downloading data for new tickers (YYYY-MM-DD format).
        credential_path (str): Path to the Google service account credentials file (JSON format).
        gsheet_id (str): The ID of the Google Sheet to write the data to.
        ticker_list (list): A list of stock tickers to download data for.
        new_data (bool, optional): If True, creates a new worksheet for each ticker. Defaults to False (appends data to existing sheets).
    """

    # Load Modules
    import gspread
    from google.oauth2.service_account import Credentials
    import yfinance as yf
    import pandas as pd
    from datetime import timedelta, date, datetime
    
    
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets"
    ]
    creds = Credentials.from_service_account_file(credential_path, scopes=scopes)
    client = gspread.authorize(creds)
    sheet_id = gsheet_id
    workbook = client.open_by_key(sheet_id)

    # Get today's date and set default start date one month earlier
    
    # Create an empty dictionary to store sheet data
    sheet_data = {}

    # Loop through each worksheet in the workbook
    for sheet in workbook.worksheets():
      sheet_name = sheet.title
    
      # Use get_all_records to get data as a list of dictionaries
      sheet_records = pd.DataFrame(sheet.get_all_records())
    
      # Add data for this sheet to the main dictionary
      sheet_data[sheet_name] = sheet_records
      
         
    # Define a list of supported stock tickers
    ticker_list = ticker_list
    count = 0
    format = '%Y-%m-%d'
    for stock_name in ticker_list:
        
        # Handle new data or existing sheet scenario
        if new_ticker:
            end_date = date.today()
            default_start_date = start_date
            # Download data from Yahoo Finance
            try:
              df = yf.download(stock_name, start=default_start_date, end=end_date)
            except Exception as e:
              print(f"Error downloading data for {stock_name}: {e}")
              continue  # Skip to next ticker on download error
            # Add a 'date' column with formatted date strings
            df['date'] = df.index.astype(str)
            df = df.applymap(lambda x: x.strftime(format) if pd.api.types.is_datetime64_dtype(x) else x)
            # Create a new worksheet for the current stock
                        
            workbook.add_worksheet(title=stock_name, rows=365 * 30, cols=20)
            worksheet = workbook.worksheet(stock_name)
            
            # Write the DataFrame headers and data to the worksheet
            try:
              worksheet.update([df.columns.values.tolist()] + df.values.tolist())
              print('Done : ' + stock_name)
            except Exception as e:
              print(f"Error uploading data for {stock_name}: {e}")
            print('Done : ' + stock_name)
            
        else:
            # Access the existing worksheet for the stock
            # worksheet = workbook.worksheet(stock_name)

            # Read existing data from the worksheet
            # ex_df = pd.DataFrame(worksheet.get_all_records())
            #print(str(ex_df[['date']].iloc[-1])[8:])
            ex_df = sheet_data.get(sheet_name)
            ex_df['date'] = pd.to_datetime(ex_df['date'])
            ex_df = ex_df.sort_values(by='date')
            # df['col1'].iloc[-1].astype(str)
            date_string = ex_df['date'].iloc[-1]
            if date_string.date() < date.today()-timedelta(days=1):
                start_date = date_string.date()+ timedelta(days=1)
                end_date=date.today()
                # Download data from Yahoo Finance
                try:
                  df = yf.download(stock_name, start=default_start_date, end=end_date)
                except Exception as e:
                  print(f"Error downloading data for {stock_name}: {e}")
                  continue  # Skip to next ticker on download error
                df['date'] = df.index
                # Concatenate the existing and downloaded dataframes (ignoring duplicate indices)
                ex_df = pd.concat([ex_df, df], ignore_index=True)
                sheet_data[stock_name] = ex_df
                count = 0
                # Update the worksheet with the combined data (headers and values)
                # worksheet.update([ex_df.columns.values.tolist()] + ex_df.values.tolist())
                # print('Done : ' + stock_name)
            else:
                ex_df = sheet_data.get(sheet_name)
                ex_df['date'] = pd.to_datetime(ex_df['date'])
                ex_df = ex_df.sort_values(by='date')
                count = 1
                print("Data Already Updated : "+stock_name)
            
    print(count)        
    if (new_ticker == False and count == 0):
        for stock_name in ticker_list:
            worksheet = workbook.worksheet(stock_name)
            try:
                worksheet.update([sheet_data[stock_name].columns.values.tolist()] + sheet_data[stock_name].values.tolist())    
            except Exception as e:
              print(f"Error uploading data for {stock_name}: {e}")
            print('Done : ' + stock_name)
                
    print('Data Updated')
    
    return sheet_data


def calculate_ema(data, window):
  return data.ewm(span=window, min_periods=window, adjust=False).mean()

def explain_sma_ema():
  import streamlit as st
  """Displays explanation of SMA and EMA"""
  st.write("**Trend direction:**")
  st.markdown("* Both SMA and EMA can be used to identify the overall trend. If the indicator is rising, it suggests an uptrend, and vice versa. You might consider buying during uptrends and selling during downtrends.")
  st.write("**Support and resistance:**")
  st.markdown("* A rising SMA/EMA can act as support, meaning the price might find buyers around that level. Conversely, a falling SMA/EMA can act as resistance, where the price might face selling pressure. You might consider buying near support and selling near resistance.")
  st.write("**Crossovers:**")
  st.markdown("* Traders sometimes look for crossovers between the price and the SMA/EMA. For example, if the price crosses above the EMA, it might signal a potential buying opportunity. The opposite (price crossing below EMA) might indicate a potential sell signal.")


def explain_macd():
  import streamlit as st
  """Displays explanation of MACD"""
  st.write("**The MACD Indicator:**")
  st.markdown("* The MACD (Moving Average Convergence Divergence) is a technical indicator used to identify trend direction, momentum, and potential buying and selling opportunities.")
  st.write("**Components:**")
  st.markdown("* **MACD Line:** Represents the difference between two exponential moving averages (EMAs) of a security's price. A positive MACD suggests bullish momentum, while a negative MACD indicates bearish momentum.")
  st.markdown("* **Signal Line:** A shorter-term EMA of the MACD line, used to smooth out fluctuations and confirm trend signals.")
  st.write("**Interpretations:**")
  st.markdown("* **Crossovers:** When the MACD line crosses above the signal line, it might signal a potential **bullish** opportunity. Conversely, a crossover below the signal line could suggest a **bearish** signal.")
  st.markdown("* **Divergence:** When the price and MACD move in opposite directions (e.g., price continues to rise while MACD falls), it can indicate a potential **divergence** and a possible trend reversal.")

def calculate_psar(data, af=0.02, af_max=0.2):
  """
  This function calculates the Parabolic SAR (PSAR) for a given price series (data)
  using the provided acceleration factor (af) and maximum acceleration factor (af_max).

  Args:
      data (pd.Series): A Pandas Series containing the High prices for the calculation.
      af (float, optional): The initial acceleration factor (default: 0.02).
      af_max (float, optional): The maximum acceleration factor (default: 0.2).

  Returns:
      pd.Series: A Pandas Series containing the PSAR values for each data point.
  """

  # Initialize variables
  import pandas as pd
  psar = [data.iloc[0]]  # Start with the first high price as the initial PSAR
  ep = data.iloc[0]  # Initialize Extreme Price (initial high)
  af_step = af  # Current acceleration factor

  for i in range(1, len(data)):
    # Update Extreme Price if the current High is greater than the existing ep
    if data.iloc[i] > ep:
      ep = data.iloc[i]

    # Calculate new PSAR
    new_psar = psar[-1] + af_step * (ep - psar[-1])

    # Update PSAR and acceleration factor based on trend reversal
    if (data.iloc[i-1] < psar[-1] and data.iloc[i] > psar[-1]) or (data.iloc[i-1] > psar[-1] and data.iloc[i] < psar[-1]):
      af_step = min(af_max, af_step * 2)  # Increase acceleration if trend reverses
      ep = min(ep, data.iloc[i])  # Update Extreme Price to the lower low in case of reversal

    # Enforce minimum distance between PSAR and High price
    new_psar = max(new_psar, psar[-1])

    # Update PSAR and acceleration factor
    psar.append(new_psar)
    if ep == psar[-1]:
      af_step = af  # Reset acceleration if PSAR touches Extreme Price

  return pd.Series(psar, index=data.index, name='PSAR')

