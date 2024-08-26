 
import pandas as pd
from src.technical_analysis.indicators import simple_moving_average, relative_strength_index

def generate_sma_crossover_signals(data: pd.DataFrame, short_window: int, long_window: int) -> pd.Series:
    """
    Generate buy/sell signals based on SMA crossover strategy.

    Args:
        data (pd.DataFrame): Input data containing 'close' prices
        short_window (int): Short-term SMA window
        long_window (int): Long-term SMA window

    Returns:
        pd.Series: Series of buy (1), sell (-1), and hold (0) signals
    """
    short_sma = simple_moving_average(data['close'], short_window)
    long_sma = simple_moving_average(data['close'], long_window)
    
    signals = pd.Series(0, index=data.index)
    signals[short_sma > long_sma] = 1  # Buy signal
    signals[short_sma < long_sma] = -1  # Sell signal
    
    return signals

def generate_rsi_signals(data: pd.DataFrame, window: int, overbought: float, oversold: float) -> pd.Series:
    """
    Generate buy/sell signals based on RSI strategy.

    Args:
        data (pd.DataFrame): Input data containing 'close' prices
        window (int): RSI calculation window
        overbought (float): RSI level considered overbought
        oversold (float): RSI level considered oversold

    Returns:
        pd.Series: Series of buy (1), sell (-1), and hold (0) signals
    """
    rsi = relative_strength_index(data['close'], window)
    
    signals = pd.Series(0, index=data.index)
    signals[rsi < oversold] = 1  # Buy signal
    signals[rsi > overbought] = -1  # Sell signal
    
    return signals