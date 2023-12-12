import matplotlib.pyplot as plt
import pandas as pd
import yfinance as yf

# Define the stock symbol and retrieve data using yfinance
symbol = 'NFLX'
netflix = yf.download(symbol, start='2012-01-01', end='2023-01-01')

# Calculate Daily Returns and drop missing values
netflix['Daily_Returns'] = netflix['Close'].pct_change()
netflix.dropna(subset=['Daily_Returns'], inplace=True)

# Function to calculate summary statistics
def calculate_summary_statistics(data):
    summary_stats = {
        'Maximum Price': data['Close'].max(),
        'Minimum Price': data['Close'].min(),
        'Mean': data['Close'].mean(),
        'Mode': data['Close'].mode()[0],
        'Median': data['Close'].median(),
        'Standard Deviation': data['Close'].std()
    }
    return summary_stats

# Calculate summary statistics for Netflix data
summary_stats_netflix = calculate_summary_statistics(netflix)

# Create a bar graph for summary statistics with annotations
plt.figure(figsize=(10, 6))

keys = list(summary_stats_netflix.keys())
values = list(summary_stats_netflix.values())

bars = plt.bar(keys, values, color='skyblue')
plt.title('Summary Statistics of Netflix Stock Prices')
plt.xlabel('Metrics')
plt.ylabel('Values')

# Annotate each bar with its corresponding value 
for bar, value in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'${value:.2f}', 
             ha='center', va='bottom', color='black', fontsize=10)

plt.get_current_fig_manager().window.title('Summary Statistics of Netflix Stock Prices')
plt.show()
