#!/usr/bin/env python
# coding: utf-8

import yfinance as yf
import pandas as pd

def banknifty_golden_strategy(symbol="^NSEBANK"):
    # 1. Fetch historical data (using Yahoo Finance for demonstration)
    # In a live setup, use your broker's API (Zerodha, AngelOne, etc.)
    data = yf.download(symbol, period="5d", interval="15m")
    
    if data.empty:
        return "No data found."

    # 2. Get Previous Day's High, Low, and Close
    # We group by date to isolate the previous session
    data['Date'] = data.index.date
    unique_dates = data['Date'].unique()
    prev_day = data[data['Date'] == unique_dates[-2]]
    
    pd_high = prev_day['High'].max()
    pd_low = prev_day['Low'].min()
    pd_close = prev_day['Close'].iloc[-1]

    # 3. Get Today's Opening Range (First 15 mins)
    today_data = data[data['Date'] == unique_dates[-1]]
    opening_candle = today_data.iloc[0]
    opening_range = opening_candle['High'] - opening_candle['Low']

    # 4. Calculate Golden Number and Levels
    golden_number = (float(pd_high - pd_low) + opening_range) * 0.618
    
    buy_above = round(pd_close + golden_number, 2)
    sell_below = round(pd_close - golden_number, 2)

    print(f"--- Bank Nifty Golden Levels ---")
    print(f"Prev Day Close: {pd_close}")
    print(f"Golden Number:  {golden_number:.2f}")
    print(f"BUY ABOVE:      {buy_above}")
    print(f"SELL BELOW:     {sell_below}")
    
    return buy_above, sell_below

# Execute
banknifty_golden_strategy()
