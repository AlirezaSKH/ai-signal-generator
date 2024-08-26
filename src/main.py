 
import pandas as pd
import yfinance as yf
from src.technical_analysis.indicators import simple_moving_average, relative_strength_index
from src.signal_generation.basic_signals import generate_sma_crossover_signals, generate_rsi_signals

def main():
    # Download sample data (e.g., AAPL stock)
    data = yf.download("AAPL", start="2022-01-01", end="2023-01-01")

    # Calculate indicators
    data['SMA_20'] = simple_moving_average(data['Close'], 20)
    data['SMA_50'] = simple_moving_average(data['Close'], 50)
    data['RSI'] = relative_strength_index(data['Close'], 14)

    # Generate signals
    data['SMA_Signal'] = generate_sma_crossover_signals(data, 20, 50)
    data['RSI_Signal'] = generate_rsi_signals(data, 14, 70, 30)

    # Print the last 10 rows of the data
    print(data.tail(10))

    # TODO: Add more analysis, visualization, or performance metrics

if __name__ == "__main__":
    main()