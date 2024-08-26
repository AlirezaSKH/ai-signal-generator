import sys
import pandas as pd
from data_fetcher import get_data
from technical_analysis.indicators import simple_moving_average, relative_strength_index
from signal_generation.basic_signals import generate_sma_crossover_signals, generate_rsi_signals

def main(symbol):
    # Fetch data
    data = get_data(symbol)
    
    if data is None or data.empty:
        print(f"Failed to fetch data for {symbol}")
        return

    # Calculate indicators
    data['SMA_20'] = simple_moving_average(data['Close'], 20)
    data['SMA_50'] = simple_moving_average(data['Close'], 50)
    data['RSI'] = relative_strength_index(data['Close'], 14)

    # Generate signals
    data['SMA_Signal'] = generate_sma_crossover_signals(data, 20, 50)
    data['RSI_Signal'] = generate_rsi_signals(data, 14, 70, 30)

    # Print the last 10 rows of the data (or all rows if less than 10)
    print(data.tail(min(10, len(data))))

    # TODO: Add more analysis, visualization, or performance metrics

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <symbol>")
        sys.exit(1)
    
    symbol = sys.argv[1]
    main(symbol)