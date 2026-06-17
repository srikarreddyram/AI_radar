import requests
from bs4 import BeautifulSoup
import datetime
import os
import csv
import time
import random

def scrape_google_finance(ticker, exchange="NASDAQ"):
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None, None
        
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract Price
    price_div = soup.find('div', class_='YMlKec fxKbKc')
    if not price_div:
        return None, None
    price_str = price_div.text.replace('$', '').replace(',', '')
    
    # Extract Change Percentage
    # Usually in a div with class "JwB6zf"
    pct_divs = soup.find_all('div', class_='JwB6zf')
    change_pct_str = "0.0%"
    for div in pct_divs:
        if '%' in div.text:
            change_pct_str = div.text
            break
            
    try:
        price = float(price_str)
        # Clean change pct string (e.g., "+1.23%" or "-0.45%")
        change_pct_clean = change_pct_str.replace('%', '').replace('+', '')
        change_pct = float(change_pct_clean)
    except Exception:
        price = 0.0
        change_pct = 0.0
        
    return price, change_pct

def main():
    print("Fetching AI stocks data...")
    
    # Ticker mapped to its exchange on Google Finance
    tickers = {
        "MSFT": "NASDAQ",
        "GOOGL": "NASDAQ",
        "NVDA": "NASDAQ",
        "META": "NASDAQ",
        "AAPL": "NASDAQ",
        "AMD": "NASDAQ",
        "TSM": "NYSE",
        "AMZN": "NASDAQ"
    }
    
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
            
        for ticker, exchange in tickers.items():
            try:
                price, change_pct = scrape_google_finance(ticker, exchange)
                if price is not None:
                    # We don't scrape volume to keep it simple and robust, just put 0
                    volume = 0
                    writer.writerow([date_str, time_str, ticker, round(price, 2), change_pct, volume])
                    print(f"Logged {ticker}: ${price:.2f} ({change_pct}%)")
                else:
                    print(f"Failed to fetch {ticker}")
            except Exception as e:
                print(f"Error fetching {ticker}: {e}")
            
            # Sleep slightly to avoid rate limits
            time.sleep(random.uniform(1.0, 2.0))

    print("Stock tracking complete.")

if __name__ == "__main__":
    main()
