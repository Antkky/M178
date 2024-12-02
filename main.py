from M178 import M178
from Strategy import strategy

# RUNNING PROCESS
#
# Get Strategy
# Backtest Strategy
# Run Monte Carlo Simulation
# analyse

if __name__ == "__main__":
    engine = M178(ticker="QQQ", start="01-01-2014", price_only=True)    # Create Engine Instance

    BTdata = engine.backtest(strategy)      # Run Backtest
    engine.plot(BTdata)                     # Plot Backtest

    MCdata = engine.montecarlo(BTdata)      # Run Monte Carlo
    engine.plot(MCdata)                     # Plot Monte Carlo
