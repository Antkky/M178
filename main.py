from M178 import M178
import pandas as pd
from Strategy import strategy

# RUNNING PROCESS
#
# Get Strategy
# Backtest Strategy
# Run Monte Carlo Simulation
# analyse

if __name__ == "__main__":
    engine = M178(ticker="AAPl", start="2014-1-1", initial_deposit=10000.0)    # Create Engine Instance
    engine.reset()
    engine.get_pricing_data()
    btData = engine.backtest(strategy)
    mcData = engine.montecarlo(btData)
    engine.plotMC(mcData)
