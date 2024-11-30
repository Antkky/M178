from Account import Account
import yfinance as yf
import pandas as pd
import numpy as np

# options pricing model does NOT take in implied volatility

class M178:
    def __init__(self, ticker, strategy, start, end, initial_deposit=10000):
        self.account = Account(initial_deposit)

        self.start = start
        self.end = end

        self.done = False

        self.ticker = ticker
        self.strategy = strategy

        self.spot = None
        self.options = None

        self.step = 0

    def run(self): # run entire operation
        while not self.done:
            action = self.strategy(self.data)
            self.forward(action)

    def forward(self, action): # go forward 1 step (1 row)
        self.step += 1

        if self.step >= 100:
            self.done = True

        print(self.step)

        return


    def get_pricing_data(self):
        self.spot = yf.download(self.ticker, start=self.start, end=self.end)
        if self.data.empty:
            raise ValueError(f"No data found for ticker {self.ticker}.")
        self.data["Returns"] = self.data['Adj Close'].pct_change()

    def get_options_data(self):
        ticker = yf.ticker(self.ticker)
        expiration_dates = ticker.options
        expirationDate = expiration_dates[1]
        self.options = ticker.options_chain(expirationDate)
