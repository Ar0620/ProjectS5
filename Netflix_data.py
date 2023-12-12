import matplotlib.pyplot as plt
import mplcursors 
import pandas as pd
import yfinance as yf
from scipy import stats
import numpy as np
from matplotlib.widgets import CheckButtons


# Function to calculate linear trend
def calculate_linear_trend(x, y):
    slope, intercept, _, _, _ = stats.linregress(x, y)
    predicted_y = slope * np.array(x) + intercept
    return slope, intercept, predicted_y

# Function to detect outliers using Z-score method
def detect_outliers_zscore(data):
    threshold = 3  # Threshold value for Z-score method
    z_scores = np.abs(stats.zscore(data))
    return np.where(z_scores > threshold)

# Function to plot returns with linear trend and highlighted outliers
def plot_with_trend_and_outliers(df, returns_col, title):
    x = range(len(df))
    y = df[returns_col].values

    slope, intercept, predicted_y = calculate_linear_trend(x, y)

    fig, ax = plt.subplots(figsize=(10, 5))
    lines = []
    lines.append(ax.plot(df.index, df[returns_col], label=f'{returns_col}', color='blue')[0])
    lines.append(ax.plot(df.index, predicted_y, label='Linear Trend', color='green')[0])

    # Detect outliers using Z-score method
    outliers = detect_outliers_zscore(df[returns_col].values)
    outliers_indices = outliers[0]
    outliers_values = df[returns_col].iloc[outliers_indices]

    # Calculate the count of outliers and data points
    count_outliers = len(outliers_indices)
    count_data_points = len(df)

    # Add the count of outliers and data points to the title
    title += f'\nOutliers: {count_outliers}, Data Points: {count_data_points}'
    plt.title(title)

    # Show counts of outliers and data points in the plot
    plt.text(0.5, 0.5, f"Outliers: {count_outliers}\nData Points: {count_data_points}", ha='center', va='center')

    # Calculate the count of outliers and data points
    count_outliers = len(outliers_indices)
    count_data_points = len(df)

    scatter = ax.scatter(df.index[outliers_indices], outliers_values, color='red', label='Outliers')

    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel('Returns')
    plt.legend()
    plt.grid(True)

      # Convert y-axis ticks to percentages
    vals = ax.get_yticks()
    ax.set_yticklabels(['{:,.2%}'.format(x) for x in vals])

    # Checkbox functionality
    labels = [str(line.get_label()) for line in lines]
    visibility = [line.get_visible() for line in lines]

    def toggle_lines(label):
        index = labels.index(label)
        lines[index].set_visible(not lines[index].get_visible())
        plt.draw()

    axbox = plt.axes([0.02, 0.85, 0.15, 0.1])
    check = CheckButtons(axbox, labels, visibility)
    check.on_clicked(toggle_lines)

    plt.show()

    print(f"Slope: {slope}")
    print(f"Intercept: {intercept}")

# Function to plot histogram
def plot_histogram(data, returns_col):
    plt.figure(figsize=(8, 5))
    plt.hist(data[returns_col], bins=30, color='skyblue', edgecolor='black')
    plt.title('Histogram of Returns')
    plt.xlabel('Returns')
    plt.ylabel('Frequency')
    plt.grid(True)

    # Detect and mark extreme outliers on the histogram
    outliers = detect_outliers_zscore(data[returns_col].values)
    outliers_indices = outliers[0]
    outliers_values = data[returns_col].iloc[outliers_indices]
    plt.scatter(outliers_values, np.zeros_like(outliers_values), color='red', label='Extreme Outliers')

    plt.legend()
    plt.show()

# Function to calculate cumulative returns
def calculate_cumulative_returns(data, returns_col):
    data['Cumulative_Returns'] = (1 + data[returns_col]).cumprod() - 1
    return data

# Function to simulate investment growth since start date with $1 investment
def simulate_investment_growth(data, returns_col):
    cumulative_returns = calculate_cumulative_returns(data, returns_col)['Cumulative_Returns']
    initial_investment = 100
    investment_growth = initial_investment+(cumulative_returns * initial_investment)
    return investment_growth

# Define the stock symbol and retrieve data using yfinance
symbol = 'NFLX'
netflix = yf.download(symbol, start='2012-01-01', end='2023-01-01')

# Calculate Daily Returns and drop missing values
netflix['Daily_Returns'] = netflix['Close'].pct_change()
netflix.dropna(subset=['Daily_Returns'], inplace=True)

# Plot Daily Returns with Linear Trend and Outliers
plot_with_trend_and_outliers(netflix, 'Daily_Returns', 'Netflix Daily Returns with Linear Trend and Outliers')

# Plot Histogram with Extreme Outliers Marked
plot_histogram(netflix, 'Daily_Returns')

# Calculate and Plot Cumulative Returns (same as previous code)
calculate_cumulative_returns(netflix, 'Daily_Returns')
plt.figure(figsize=(10, 5))
plt.plot(netflix.index, netflix['Cumulative_Returns'], label='Cumulative Returns', color='purple')
plt.title('Netflix Cumulative Returns')
plt.xlabel('Date')
plt.ylabel('Cumulative Returns %')
plt.legend()
plt.grid(True)
plt.show()

# Simulate Investment Growth Since Start Date with $1 Investment (same as previous code)
investment_growth = simulate_investment_growth(netflix, 'Daily_Returns')
fig, ax = plt.subplots(figsize=(10, 5))
plt.plot(netflix.index, investment_growth, label='Investment Growth ($100 initial investment)', color='orange')
plt.title('Investment Growth Since Start Date')
plt.xlabel('Date')
plt.ylabel('Investment Value $')
plt.legend()

plt.grid(True)

# Create annotations for investment growth chart
mpl_cursors = mplcursors.cursor(ax, hover=True)
mpl_cursors.connect("add", lambda sel: sel.annotation.set_text(f"Investment Value: ${sel.target[1]:.2f}"))

plt.show()
