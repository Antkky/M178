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



    def backtest(self, strategy): # run entire operation
        """
        Implement
        """
        self.reset()

        self.get_pricing_data()
        self.get_options_data()

        if not self.runCheck():
            return

        BTdata = None

        while not self.done: # main loop
            action = strategy(self.spot, self.options)
            self.forward(action)

        return BTdata


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


    def forward(self, action): # go forward 1 step (1 row)
        """
        Implement
        """
        self.step += 1

        if self.step >= 100:
            self.done = True
        # code goes here

        self.account.execute(action)


        return


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
