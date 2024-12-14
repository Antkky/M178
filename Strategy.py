import pandas as pd

def strategy(spot: pd.DataFrame):
    """
        Implement Strategy Here
    """
    if spot is not None:
        trade = {
            "type": "buy",
            "size": 1,
            "price": spot.iloc[0],
            "direction": True,
            "takeprofit": 100,
            "stoploss": 100,
        }
        return trade
