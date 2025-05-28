# File: stock_news_sentiment_example.py

import yfinance as yf
from bs4 import BeautifulSoup
import requests
from transformers import pipeline
import warnings

# Suppress specific warnings if needed (e.g., from yfinance or https)
warnings.filterwarnings("ignore", category=FutureWarning)

# --- Component 1: Fetching Stock Prices ---
def get_stock_data(ticker):
    """Fetches historical stock data for the last year."""
    try:
        stock = yf.Ticker(ticker)
        # Fetch data for the last year
        data = stock.history(period='1y')
        print(f"Successfully fetched stock data for {ticker}.")
        return data
    except Exception as e:
        print(f"Error fetching stock data for {ticker}: {e}")
        return None

# --- Component 2: Scraping News Headlines ---
def get_stock_news(ticker):
    """Scrapes news headlines for a ticker from Yahoo Finance."""
    # IMPORTANT: Yahoo Finance structure changes often. This selector might break.
    # The class 'Mb(5px)' from the article might be outdated. Inspect the
    # current Yahoo Finance page for the correct headline elements if this fails.
    # A possible updated selector might involve 'h3' tags within specific divs.
    # Let's try a slightly more robust search (might still need adjustment)
    url = f'https://finance.yahoo.com/quote/{ticker}?p={ticker}'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'} # Mimic browser

    print(f"Attempting to fetch news for {ticker} from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)

        soup = BeautifulSoup(response.text, 'html.parser')

        # --- !!! Selector Alert !!! ---
        # This is the critical part that might break.
        # Original article used: soup.find_all('h3', class_='Mb(5px)')
        # Let's try finding 'h3' tags that likely contain news links
        # This is a guess based on potential structure - INSPECT THE PAGE if it fails
        headlines = []
        # Look for list items that might contain news
        news_items = soup.find_all('li', class_=lambda x: x and 'StreamItem' in x) # Heuristic guess
        for item in news_items:
             # Find h3 tag within the item
             h3_tag = item.find('h3')
             if h3_tag and h3_tag.text:
                 headlines.append(h3_tag.text.strip())

        if not headlines:
             print(f"Warning: Could not find headlines using common selectors for {ticker}. Scraping structure might have changed.")
             # Fallback attempt: Find all h3 tags (might get unrelated titles)
             # print("Trying fallback: searching all h3 tags...")
             # all_h3 = soup.find_all('h3')
             # headlines = [h.text.strip() for h in all_h3 if h.text.strip()]


        print(f"Found {len(headlines)} potential headlines for {ticker}.")
        return headlines[:10] # Limit number of headlines processed

    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL {url}: {e}")
        return []
    except Exception as e:
        print(f"Error parsing news for {ticker}: {e}")
        return []

# --- Component 3: Sentiment Analysis ---
# Initialize the sentiment analysis pipeline once
print("Loading sentiment analysis model...")
try:
    sentiment_analyzer = pipeline('sentiment-analysis')
    print("Sentiment analysis model loaded.")
except Exception as e:
    print(f"Fatal Error: Could not load sentiment analysis model: {e}")
    sentiment_analyzer = None # Ensure it's defined even on failure

def analyze_sentiment(text):
    """Analyzes the sentiment of a given text using the pre-loaded pipeline."""
    if not sentiment_analyzer or not text:
        return "N/A" # Cannot analyze if model failed or text is empty
    try:
        result = sentiment_analyzer(text)
        # Return only the label (e.g., 'POSITIVE', 'NEGATIVE')
        return result[0]['label']
    except Exception as e:
        print(f"Error analyzing sentiment for text '{text[:50]}...': {e}")
        return "Error"

# --- Bringing It All Together ---
if __name__ == "__main__":
    stock_ticker = 'AAPL' # Example: Apple Inc.

    print(f"\n--- Analysis for Stock Ticker: {stock_ticker} ---")

    # 1. Get stock data
    stock_data = get_stock_data(stock_ticker)
    if stock_data is not None and not stock_data.empty:
        # Print only the last 5 days for brevity
        print(f"\nRecent Stock Data for {stock_ticker}:")
        print(stock_data.tail())
    else:
        print(f"\nCould not retrieve stock data for {stock_ticker}.")

    # 2. Get stock news headlines
    news_headlines = get_stock_news(stock_ticker)

    # 3. Analyze sentiment for each news headline (if model loaded)
    if news_headlines and sentiment_analyzer:
        print("\nNews Headlines and Sentiments:")
        sentiments = []
        for i, headline in enumerate(news_headlines):
            print(f"Analyzing headline {i+1}/{len(news_headlines)}...")
            sentiment = analyze_sentiment(headline)
            sentiments.append(sentiment)
            print(f"- Headline: {headline}")
            print(f"  Sentiment: {sentiment}")
            print("-" * 10) # Separator
    elif not news_headlines:
        print("\nNo news headlines found or fetched.")
    else:
        print("\nSentiment analysis model not available. Skipping sentiment analysis.")

    print(f"\n--- End of Analysis for {stock_ticker} ---")
