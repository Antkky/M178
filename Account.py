class Account:
    ########################################################################################################
    class SpotPosition:
        def __init__(self, price, take, stop, size, direction):  # Entry
            self.entry_price = price
            self.take_profit = take
            self.stop_loss = stop
            self.position_size = size
            self.direction = direction

        def get_pnl(self, price):
            """"
            """
            pnl_per_unit = 0
            if self.direction == "long":
                pnl_per_unit = price - self.entry_price
            elif self.direction == "short":
                pnl_per_unit = self.entry_price - price
            return pnl_per_unit * self.position_size

        def check(self, price):
            """"
            """
            if self.direction == "long":
                if price <= self.stop_loss:
                    return "stoploss"
                elif price >= self.take_profit:
                    return "takeprofit"
            elif self.direction == "short":
                if price >= self.stop_loss:
                    return "stoploss"
                elif price <= self.take_profit:
                    return "takeprofit"
            return None

        def close(self, price):
            """"
            """
            pnl = self.get_pnl(price)
            self.position_size = 0
            return pnl

    ########################################################################################################
    class OptionPosition:
        def __init__(self, premium, strike, size, option_type, direction):  # entry
            self.premium = premium
            self.strike = strike
            self.size = size
            self.option_type = option_type  # "call" or "put"
            self.direction = direction  # "long" or "short"

        def get_pnl(self, price):
            """"
            """
            intrinsic_value = 0
            if self.option_type == "call":
                intrinsic_value = max(0, price - self.strike)
            elif self.option_type == "put":
                intrinsic_value = max(0, self.strike - price)

            if self.direction == "long":
                return (intrinsic_value - self.premium) * self.size
            elif self.direction == "short":
                return (self.premium - intrinsic_value) * self.size

    ########################################################################################################

    def __init__(self, deposit):
        self.equity = deposit
        self.cash = deposit
        self.unrealized_pnl = 0
        self.realized_pnl = 0
        self.options = []
        self.positions = []

        self.historical_realized_pnl = []

    def get_unrealized_pnl(self, price):
        """"
        """
        self.unrealized_pnl = 0

        # Check Spot Positions
        for position in self.positions:
            self.unrealized_pnl += position.get_pnl(price)

        # Check Options
        for option in self.options:
            self.unrealized_pnl += option.get_pnl(price)

        return self.unrealized_pnl

    def execute(self, action, size, price, direction, take=None, stop=None, option=None):
        """
        Handles execution of spot and options trades.
        """
        # spot execution
        if action == "buy_spot" or action == "sell_spot":
            direction = "long" if action == "buy_spot" else "short"
            cost = size * price

            if self.cash >= cost: # balance check
                self.cash -= cost
                new_position = self.SpotPosition(price, take, stop, size, direction) # open new position
                self.positions.append(new_position)
            else:
                raise ValueError("Insufficient cash to execute trade.")

        # options execution
        elif action == "buy_option" or action == "sell_option":
            if option is None:
                raise ValueError("Option details required for options trade.")
            premium = option.get("premium", 0)
            strike = option.get("strike", 0)
            option_type = option.get("type", "call")  # default to "call"
            direction = "long" if action == "buy_option" else "short"

            cost = premium * size
            if self.cash >= cost:
                self.cash -= cost
                new_option = self.OptionPosition(premium, strike, size, option_type, direction)
                self.options.append(new_option)
            else:
                raise ValueError("Insufficient cash to execute trade.")

    def close_position(self, position, price):
        """
        Close a specific position at the given price.
        """
        pnl = position.close(price)
        self.realized_pnl += pnl
        self.cash += position.position_size * price  # Add cash from closing
        self.positions.remove(position)

    def close_all_positions(self, price):
        """
        Close all open positions and calculate realized PnL.
        """
        for position in self.positions[:]:
            self.close_position(position, price)

        for option in self.options[:]:
            pnl = option.get_pnl(price)
            self.realized_pnl += pnl
            self.cash += pnl  # Add or subtract cash from option close
            self.options.remove(option)

    def update_equity(self, price):
        """
        Update total equity based on cash and unrealized PnL.
        """
        self.equity = self.cash + self.get_unrealized_pnl(price)
        return self.equity

    def return_data(self):
        pass
