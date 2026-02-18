#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import time
from datetime import datetime
from nsepython import *

# 1. Formatting settings
pd.set_option('display.max_columns', None)

def get_data():
    print("Fetching BankNIFTY Data...")
    try:
        # BankNifty Future meta data
        bn_meta = nse_quote_meta("BANKNIFTY", "latest", "Fut")
        
        # Check if data is actually received
        if not bn_meta or 'expiryDate' not in bn_meta:
            print("Error: NSE se data nahi mil raha. 5 min baad try karein.")
            return None

        # Fetching LTP and previous day values
        prev_close = float(bn_meta['prevClose'])
        r_high = float(bn_meta['highPrice'])
        r_low = float(bn_meta['lowPrice'])
        
        # Note: Historical data manual URL often fails. 
        # For simplicity, we use current session range as per your logic.
        opening_range = r_high - r_low
        
        # Golden Number Calculation
        # Formula: ((Prev High - Prev Low) + Today's Range) * 0.618
        # Yahan hum simplified logic use kar rahe hain jo NSE blocks se bachega
        golden_number = (opening_range) * 0.618 
        
        buy_above = int(prev_close + golden_number)
        sell_below = int(prev_close - golden_number)
        
        return buy_above, sell_below, prev_close

    except Exception as e:
        print(f"Connection Error: {e}")
        return None

# Initial Setup
data = get_data()
if data:
    buy_above, sell_below, prev_close = data
    print(f"\n--- Strategy Levels ---")
    print(f"Prev Close: {prev_close}")
    print(f"BUY ABOVE: {buy_above}")
    print(f"SELL BELOW: {sell_below}")
    print(f"-----------------------\n")

    # Entry Loop
    who_triggered = "NONE"
    while True:
        try:
            bn_ltp = nse_quote_ltp("BANKNIFTY", "latest", "Fut")
            curr_time = datetime.now().strftime("%H:%M:%S")
            print(f"[{curr_time}] BankNIFTY LTP: {bn_ltp}")

            if bn_ltp > buy_above:
                print(f"!!! BUY TRIGGERED at {bn_ltp} !!!")
                who_triggered = "BUY"
                stop_loss = bn_ltp * 0.995
                target = bn_ltp * 1.02
                break
            
            elif bn_ltp < sell_below:
                print(f"!!! SELL TRIGGERED at {bn_ltp} !!!")
                who_triggered = "SELL"
                stop_loss = bn_ltp * 1.005
                target = bn_ltp * 0.98
                break

            time.sleep(10) # 10 seconds wait
        except:
            print("Retrying connection...")
            time.sleep(5)

    # Trade Management Loop
    if who_triggered != "NONE":
        print(f"Target: {target:.2f} | StopLoss: {stop_loss:.2f}")
        while True:
            bn_ltp = nse_quote_ltp("BANKNIFTY", "latest", "Fut")
            print(f"Monitoring Trade... Current: {bn_ltp}")
            
            if who_triggered == "BUY":
                if bn_ltp >= target:
                    print("TARGET HIT! Happy Profits.")
                    break
                if bn_ltp <= stop_loss:
                    print("STOP LOSS HIT!")
                    break
            
            if who_triggered == "SELL":
                if bn_ltp <= target:
                    print("TARGET HIT! Happy Profits.")
                    break
                if bn_ltp >= stop_loss:
                    print("STOP LOSS HIT!")
                    break
            
            time.sleep(10)
