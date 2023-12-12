import yfinance as yf
import matplotlib.pyplot as plt

# Function to analyze stock performance and advise investors
def analyze_stock_and_advise(symbol, start_date, end_date, short_term_lookback, long_term_lookback):
    try:
        # Retrieve historical stock data from Yahoo Finance
        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Calculate short-term percentage change
        short_term_start = stock_data.index[-short_term_lookback]
        short_term_initial = stock_data.loc[short_term_start]['Close']
        short_term_final = stock_data['Close'][-1]
        short_term_change = ((short_term_final - short_term_initial) / short_term_initial) * 100

        # Calculate long-term percentage change
        long_term_start = stock_data.index[-long_term_lookback]
        long_term_initial = stock_data.loc[long_term_start]['Close']
        long_term_final = stock_data['Close'][-1]
        long_term_change = ((long_term_final - long_term_initial) / long_term_initial) * 100

        # Advise investors based on short-term and long-term percentage changes
        advise_short_term = ""
        if short_term_change > 5:
            advise_short_term = "Positive short-term momentum - Consider buying"
        elif short_term_change < -5:
            advise_short_term = "Negative short-term momentum - Consider selling"
        else:
            advise_short_term = "Stable short-term movement - Hold position"

        advise_long_term = ""
        if long_term_change > 20:
            advise_long_term = "Positive long-term growth potential - Consider holding or buying"
        elif long_term_change < -20:
            advise_long_term = "Negative long-term growth potential - Consider selling"
        else:
            advise_long_term = "Stable long-term performance - Hold position"

        # Plotting the percentage change on a chart with advice
        plt.figure(figsize=(10, 6))

        # Plotting short-term performance with advice
        plt.subplot(211)
        plt.plot(stock_data.index, stock_data['Close'])
        plt.title(f"Stock: {symbol}\nShort-Term Change ({short_term_lookback} days): {short_term_change:.2f}%\nAdvice: {advise_short_term}")
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)

        # Plotting long-term performance with advice
        plt.subplot(212)
        plt.plot(stock_data.index, stock_data['Close'])
        plt.title(f"Long-Term Change ({long_term_lookback} days): {long_term_change:.2f}%\nAdvice: {advise_long_term}")
        plt.xlabel('Date')
        plt.ylabel('Closing Price')
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")

# Example usage:
stock_symbol = 'NFLX'  # Replace with the desired stock symbol
start_date = '2019-01-01'  # Replace with the desired start date
end_date = '2022-01-01'  # Replace with the desired end date
short_term_lookback = 90  # Short-term lookback period in days
long_term_lookback = 365  # Long-term lookback period in days

analyze_stock_and_advise(stock_symbol, start_date, end_date, short_term_lookback, long_term_lookback)
