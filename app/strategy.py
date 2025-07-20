import pandas as pd
from typing import List, Dict, Any
from decimal import Decimal

def moving_average_crossover_strategy(
    data: List[Dict[str, Any]],
    short_window: int = 10,
    long_window: int = 30
) -> Dict[str, Any]:
    # ... (the top part of the function is the same) ...
    if not data or len(data) < long_window:
        return {"signals": [], "performance": "Insufficient data to calculate strategy."}

    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df = df.sort_values(by='datetime').set_index('datetime')
    df['close'] = pd.to_numeric(df['close'])

    df['short_ma'] = df['close'].rolling(window=short_window, min_periods=1).mean()
    df['long_ma'] = df['close'].rolling(window=long_window, min_periods=1).mean()

    df['signal'] = 0
    df.loc[df['short_ma'] > df['long_ma'], 'signal'] = 1
    df.loc[df['short_ma'] < df['long_ma'], 'signal'] = -1
    
    df['position'] = df['signal'].diff()
    
    # --- THIS IS THE CORRECTED LINE ---
    # We explicitly filter out the NaN on the first row and only look for actual changes.
    crossover_points = df[df['position'].notna() & (df['position'] != 0)]

    signals = []
    for idx, row in crossover_points.iterrows():
        if row['position'] > 0:
            signal_type = "BUY"
        else:
            signal_type = "SELL"
        
        signals.append({
            "datetime": idx.isoformat(),
            "signal": signal_type,
            "price": row['close']
        })
    
    return {
        "parameters": {
            "short_window": short_window,
            "long_window": long_window,
            "total_data_points": len(df),
        },
        "total_trades": len(signals),
        "signals": signals
    }