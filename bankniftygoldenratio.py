#!/usr/bin/env python
# coding: utf-8

import yfinance as yf
import pandas as pd

def banknifty_golden_strategy(symbol="^NSEBANK"):
    print(f"Fetching data for {symbol}...")
    
    # 1. Fetch data (5 days to ensure we have enough for 'Yesterday' and 'Today')
    # Using 15m interval for the Opening Range
    df = yf.download(symbol, period="5d", interval="15m")
    
    if df.empty:
        print("Error: Could not fetch data. Check your internet or symbol.")
        return

    # FIX: Flatten MultiIndex columns if they exist (common in newer yfinance versions)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    # 2. Organize data by date
    df['Date'] = df.index.date
    unique_dates = sorted(df['Date'].unique())
    
    if len(unique_dates) < 2:
        print("Error: Not enough historical data to calculate strategy.")
        return

    today_date = unique_dates[-1]
    prev_date = unique_dates[-2]

    # 3. Get Previous Day's High, Low, and Close
    prev_day_data = df[df['Date'] == prev_date]
    pd_high = float(prev_day_data['High'].max())
    pd_low = float(prev_day_data['Low'].min())
    pd_close = float(prev_day_data['Close'].iloc[-1])

    # 4. Get Today's Opening Range (First 15-min candle)
    today_data = df[df['Date'] == today_date]
    if today_data.empty:
        print("Market hasn't opened yet for today.")
        return
        
    opening_candle = today_data.iloc[0]
    # .item() ensures we get a float, not a Series
    open_high = float(opening_candle['High'])
    open_low = float(opening_candle['Low'])
    opening_range = open_high - open_low

    # 5. Golden Strategy Calculation
    # Formula: ((Prev Day Range) + Opening Range) * 0.618
    golden_number = ((pd_high - pd_low) + opening_range) * 0.618
    
    buy_above = round(pd_close + golden_number, 2)
    sell_below = round(pd_close - golden_number, 2)

    # 6. Output Results
    print("\n" + "="*30)
    print(f"STRATEGY FOR: {today_date}")
    print(f"PREV CLOSE:   {pd_close:.2f}")
    print(f"GOLDEN VALUE: {golden_number:.2f}")
    print("-" * 30)
    print(f"🚀 BUY ABOVE:  {buy_above}")
    print(f"🔻 SELL BELOW: {sell_below}")
    print("="*30)

if __name__ == "__main__":
    try:
        banknifty_golden_strategy()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
