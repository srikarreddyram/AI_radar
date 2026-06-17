import yfinance as yf
import pandas as pd
import datetime
import os
import csv

def main():
    print("Fetching AI stocks data...")
    
    tickers = ["MSFT", "GOOGL", "NVDA", "META", "AAPL", "AMD", "TSM", "AMZN"]
    now_dt = datetime.datetime.now(datetime.UTC)
    date_str = now_dt.strftime("%Y-%m-%d")
    time_str = now_dt.strftime("%H:%M:%S")

    # CSV path
    aggregated_dir = os.path.join(os.path.dirname(__file__), '..', 'aggregated')
    os.makedirs(aggregated_dir, exist_ok=True)
    csv_file = os.path.join(aggregated_dir, 'ai_stocks.csv')
    
    file_exists = os.path.isfile(csv_file)
    
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Date', 'Time', 'Ticker', 'Price', 'Change_Pct', 'Volume'])
            
        for ticker_symbol in tickers:
            try:
                ticker = yf.Ticker(ticker_symbol)
                # Fetch recent history (1d to get the latest close)
                hist = ticker.history(period="1d")
                
                if hist.empty:
                    print(f"No data for {ticker_symbol}")
                    continue
                
                price = float(hist['Close'].iloc[-1])
                volume = int(hist['Volume'].iloc[-1])
                
                # To get change pct, we need previous close
                # So we fetch 5d history to ensure we get previous trading day
                hist_5d = ticker.history(period="5d")
                if len(hist_5d) >= 2:
                    prev_close = float(hist_5d['Close'].iloc[-2])
                    change_pct = round(((price - prev_close) / prev_close) * 100, 2)
                else:
                    change_pct = 0.0

                writer.writerow([date_str, time_str, ticker_symbol, round(price, 2), change_pct, volume])
                print(f"Logged {ticker_symbol}: ${price:.2f} ({change_pct}%)")
            except Exception as e:
                print(f"Error fetching {ticker_symbol}: {e}")

    print("Stock tracking complete.")

if __name__ == "__main__":
    main()
