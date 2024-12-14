from Account import Account
import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# only 1d intervals
class M178:
    """
    Implement
    """
    def __init__(self, ticker: str, start=None, end=None, initial_deposit=None):
        self.account = Account(initial_deposit)
        self.first_rendering = True

        self.start = start
        self.end = end

        self.step = 0
        self.done = False

        self.ticker = ticker

        self.spot = None # full price dataset
        self.spottd = None # price dataset up to current step

    def backtest(self, strategy):
        """
        Implement
        """
        print("Backtesting...")

        while self.done is False: # main loop
            action = strategy(self.spottd)
            trade = {
                "size": int(1),
                "price": float(1000),
                "entry": bool(True),
                "direction": bool(True),
                "takeprofit": float(100),
                "stoploss": float(100),
            }
            self.forward(trade)

        print("Retreiving BTdata...")
        if self.done is True: # once done
            trades = self.account.get_trades()
            BTdata = pd.DataFrame(trades)
            return BTdata

    def forward(self, trade: dict):
        """
        Advance the simulation by one step and update the environment state.
        """
        # Increment step
        self.step += 1

        # Check if the simulation is done
        if self.step >= len(self.spot):
            self.done = True
            return

        # Execute the action
        self.account.execute(
            trade["entry"],
            trade["size"],
            trade["price"],
            trade["direction"],
            trade["takeprofit"],
            trade["stoploss"]
        )

        self.update()

    def montecarlo(self, data: pd.DataFrame, iterations: int=250):
        """
        Generate a dataset of randomized equity curves using Monte Carlo simulation.

        Args:
            data (pd.DataFrame): DataFrame containing the trade data.
            iterations (int): Number of randomized equity curves to generate.

        Returns:
            pd.DataFrame: A DataFrame where each column represents an equity curve.
        """
        print("Running Monte Carlo Simulation...")
        equity_curves = []

        for i in range(0, iterations):
            # Sample data randomly with replacement
            smData = data.sample(n=len(data), replace=True)  # Random sampling with replacement
            returns = smData['close'] - smData['open']  # Calculate returns

            # Reset index to ensure unique index for each iteration
            returns = returns.reset_index(drop=True)  # Reset index to avoid conflicts

            # Compute cumulative returns (equity curve)
            equity_curve = returns.cumsum()  # Cumulative sum of returns

            # Append the equity curve as a new column
            equity_curves.append(equity_curve)

        # Create DataFrame where each column is a different equity curve
        return pd.DataFrame(equity_curves).transpose()  # Transpose to align columns properly

    def plot(self, df: pd.DataFrame):
        """
        Plots stock price and volume data from a pandas DataFrame.

        Parameters:
            df (pandas.DataFrame): DataFrame containing 'time', 'open', 'high', 'low', 'close', 'volume' columns.
        """
        # Convert time to datetime if it's not already
        if df is None:
            raise ValueError("Dataframe 'df' is None.")

        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

        # Set up the figure and axes
        fig, ax1 = plt.subplots(figsize=(12, 8))

        # Plot price data on the first y-axis
        ax1.plot(df['date'], df['open'], label='Open', color='blue', alpha=0.7)
        ax1.plot(df['date'], df['high'], label='High', color='green', alpha=0.7)
        ax1.plot(df['date'], df['low'], label='Low', color='red', alpha=0.7)
        ax1.plot(df['date'], df['close'], label='Close', color='purple', alpha=0.7)
        ax1.set_ylabel('Price')
        ax1.set_xlabel('Date')
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle='--', alpha=0.5)

        # Set the title
        plt.title('Stock Price')

        # Automatically adjust the x-axis date format
        fig.autofmt_xdate()

        # Show the plot
        plt.show()

    def plotPD(self):
        self.plot(self.spot)

    def plotMC(self, mcData: pd.DataFrame):
        """
        Plot the equity curves from the Monte Carlo simulation.

        Args:
            equity_curves (pd.DataFrame): DataFrame where each column represents an equity curve.
            show_mean (bool): Whether to overlay the mean equity curve.

        Returns:
            None
        """
        plt.figure(figsize=(10, 6))  # Set the figure size for better readability

        # Plot each equity curve
        for column in mcData.columns:
            plt.plot(mcData.index, mcData[column], label=f'Curve {str(column + 1)}')  # Convert column to str


        # Add labels and title
        plt.xlabel('Time')  # X-axis label (adjust based on your data)
        plt.ylabel('Equity Value')  # Y-axis label
        plt.title('Monte Carlo Simulation: Equity Curves')  # Title of the plot

        # Display the plot
        plt.grid(True)
        plt.show()

    def reset(self):
        self.step = 0
        self.first_rendering = True
        self.done = False

        self.spot = None
        self.options = None

    def update(self):
        """
        update the current price data set and other nessasary components
        """
        current_data = []

        for i in range(self.step):
            row = self.spot.iloc[i]
            current_data.append({
                "date": row["date"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"],
            })

        current_data = pd.DataFrame(current_data)
        self.spottd = current_data

    def get_pricing_data(self):
        """
        Implement
        """
        pdata = yf.download(self.ticker, start=self.start, end=self.end)
        data = []
        for _, row in pdata.iterrows():
            temp = {
                "date": row.name,
                "open": row["Open"],
                "high": row["High"],
                "low": row["Low"],
                "close": row["Close"],
                "volume": row["Volume"]
            }

            data.append(temp)

        self.spot = pd.DataFrame(data)
        return self.spot

    def get_options_data(self):
        """
        Implement
        """
        ticker = yf.Ticker(self.ticker)
        expiration_dates = ticker.options
        expirationDate = expiration_dates[1]
        self.options = ticker.option_chain(expirationDate)
        if self.options is None:
            raise ValueError(f"No options data found for ticker {self.ticker}.")
