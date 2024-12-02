class BTdata:
    def __init__(self, raw_data=None):
        """
        Initialize BTdata with optional raw data.
        """
        self.raw_data = raw_data if raw_data is not None else {}

    class plotdata:
        def __init__(self, x_data=None, y_data=None, title="Plot", xlabel="X-axis", ylabel="Y-axis"):
            """
            Initialize plotdata with data and labels.
            """
            self.x_data = x_data if x_data is not None else []
            self.y_data = y_data if y_data is not None else []
            self.title = title
            self.xlabel = xlabel
            self.ylabel = ylabel

        def __str__(self):
            """
            String representation of the plot data.
            """
            return f"Plot Title: {self.title}, X-axis: {self.xlabel}, Y-axis: {self.ylabel}"

# Example Usage
bt_data = BTdata({"strategy_name": "Mean Reversion"})
plot_data = BTdata.plotdata(
    x_data=[1, 2, 3, 4],
    y_data=[10, 15, 20, 25],
    title="Strategy Performance",
    xlabel="Time",
    ylabel="Profit"
)

print(str(plot_data))  # Output: Plot Title: Strategy Performance, X-axis: Time, Y-axis: Profit
