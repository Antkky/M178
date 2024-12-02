from Account import Account
import yfinance as yf
import pandas as pd
import numpy as np
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

        self.spot = None
        self.options = None

    def backtest(self, strategy):
        """
        Implement
        """
        self.reset()

        self.get_pricing_data()
        self.get_options_data()

        rows = []

        while not self.done: # main loop
            action = strategy(self.spot, self.options)
            data = self.forward(action)
            rows.append(data)

        BTdata = pd.DataFrame(rows)
        return BTdata

    def forward(self, action):
        """
        Advance the simulation by one step and update the environment state.
        """
        # Increment step
        self.step += 1

        # Check if the simulation is done
        if self.step >= len(self.spot):
            self.done = True
            return None

        # Execute the action
        self.account.execute(action)

        # Calculate market returns
        if self.step > 0:
            mkreturns = (self.spot[self.step].close - self.spot[self.step - 1].close) / self.spot[self.step - 1].close
        else:
            mkreturns = 0

        # Calculate strategy returns (replace with appropriate calculation)
        streturns = self.account.get_strategy_returns()

        # Return current state data
        return {
            "step": self.step,
            "open": self.spot[self.step].open,
            "high": self.spot[self.step].high,
            "low": self.spot[self.step].low,
            "close": self.spot[self.step].close,
            "volume": self.spot[self.step].volume,
            "mkreturns": mkreturns,
            "streturns": streturns,
        }

    def montecarlo(self, data):
        MCdata = None

        ############################
        # implement code here
        ############################

        return MCdata

    def plot(self, data):
        # Extract plot data
        plotdata = data.plotdata

        # Create subplots
        self.fig_price, self.ax_returns = plt.subplots(figsize=(10, 6))

        # Plot returns over time
        self.ax_returns.plot(plotdata['Time'], plotdata['Returns'], label='Returns', color='blue', linewidth=1.5)

        # Set titles and labels
        self.ax_returns.set_title(f'Returns for {self.ticker}')
        self.ax_returns.set_xlabel('Time')
        self.ax_returns.set_ylabel('Returns')

        # Add grid and legend
        self.ax_returns.grid(True, linestyle='--', alpha=0.7)
        self.ax_returns.legend()

        # Show the plot
        plt.show()

    def reset(self):
        self.step = 0
        self.first_rendering = True
        self.done = False

        self.spot = None
        self.options = None

    def get_pricing_data(self):
        """
        Implement
        """
        self.spot = yf.download(self.ticker, start=self.start, end=self.end)
        if self.spot.empty:
            raise ValueError(f"No spot data found for ticker {self.ticker}.")
        self.spot["Returns"] = self.spot['Adj Close'].pct_change()

    def get_options_data(self):
        """
        Implement
        """
        ticker = yf.Ticker(self.ticker)
        expiration_dates = ticker.options
        expirationDate = expiration_dates[1]
        self.options = ticker.option_chain(expirationDate)
        if self.options.empty:
            raise ValueError(f"No options data found for ticker {self.ticker}.")
