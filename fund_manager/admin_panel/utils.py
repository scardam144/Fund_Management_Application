import yfinance as yf

def get_stock_price(symbol):
    try:
        # Download stock data for the given symbol
        stock_data = yf.download(symbol, period="1d", interval="5m")  # Interval of 5 minutes for intraday data
        
        if stock_data.empty:
            stock_data = yf.download(symbol)
            if stock_data.empty:
                return "No data available for this symbol"
        
        # Get the last price from the most recent data point
        last_row = stock_data.iloc[-1]
        last_price = round(last_row['Close'].iloc[-1], 3)
        print(f"printing the thinfs like {last_price}", type(last_price))
        return last_price
    except Exception as e:
        return f"Error: {str(e)}"

# # Example usage
# symbol = 'BA'  # Use the full ticker symbol for international stocks (e.g., BA.LON for Boeing on the London Stock Exchange)
# current_price = get_stock_price(symbol)
# print(type(current_price))
# print(f"The current price of {symbol} is: {current_price}")
