 
import numpy as np
import pandas as pd

def simple_moving_average(data: pd.Series, window: int) -> pd.Series:
    """
    Calculate the Simple Moving Average (SMA) for a given data series.

    Args:
        data (pd.Series): Input data series
        window (int): The rolling window size

    Returns:
        pd.Series: The calculated SMA series
    """
    return data.rolling(window=window).mean()

def exponential_moving_average(data: pd.Series, span: int) -> pd.Series:
    """
    Calculate the Exponential Moving Average (EMA) for a given data series.

    Args:
        data (pd.Series): Input data series
        span (int): The span for the EMA calculation

    Returns:
        pd.Series: The calculated EMA series
    """
    return data.ewm(span=span, adjust=False).mean()

def relative_strength_index(data: pd.Series, window: int) -> pd.Series:
    """
    Calculate the Relative Strength Index (RSI) for a given data series.

    Args:
        data (pd.Series): Input data series
        window (int): The rolling window size

    Returns:
        pd.Series: The calculated RSI series
    """
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    return rsi