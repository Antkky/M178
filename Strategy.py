import pandas as pd

def strategy(spot: pd.DataFrame):
    """
        Implement Strategy Here
    """
    trade = {
        "type": "buy",
        "size": 1,
        "price": spot.iloc[0]["open"],
        "direction": True,
        "takeprofit": 100,
        "stoploss": 100,
    }
    return trade
