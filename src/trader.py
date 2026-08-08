class MarketMaker:
    """
    Represents a simple market maker who quotes bid and ask prices,
    manages inventory, and tracks cash/PnL.
    """

    def __init__(
        self,
        base_spread: float = 2.0,
        max_inventory: int = 20,
        inventory_penalty: float = 0.1,
        initial_cash: float = 0.0,
    ):
        """
        Args:
            base_spread: Total bid-ask spread.
            max_inventory: Maximum inventory allowed before refusing some trades.
            inventory_penalty: How strongly quotes are adjusted based on inventory.
            initial_cash: Starting cash.
        """

        if base_spread <= 0:
            raise ValueError("base_spread must be greater than 0.")

        if max_inventory <= 0:
            raise ValueError("max_inventory must be greater than 0.")

        if inventory_penalty < 0:
            raise ValueError("inventory_penalty cannot be negative.")

        self.base_spread = base_spread
        self.max_inventory = max_inventory
        self.inventory_penalty = inventory_penalty
        self.initial_cash = initial_cash
        self.cash = initial_cash
        self.inventory = 0

    def reset(self) -> None:
        """
        Resets the market maker back to its starting cash and zero inventory
        so a fresh simulation can be run with the same parameters.
        """

        self.cash = self.initial_cash
        self.inventory = 0

    def calculate_quotes(self, fair_value: float) -> tuple[float, float]:
        """
        Calculates bid and ask prices.

        Inventory adjustment logic:
        - If inventory is positive, trader wants to sell more, so quotes shift lower.
        - If inventory is negative, trader wants to buy more, so quotes shift higher.

        Args:
            fair_value: Current fair value of the asset.

        Returns:
            bid_price, ask_price
        """

        if fair_value <= 0:
            raise ValueError("fair_value must be greater than 0.")

        half_spread = self.base_spread / 2

        inventory_adjustment = self.inventory_penalty * self.inventory

        adjusted_fair_value = fair_value - inventory_adjustment

        bid_price = adjusted_fair_value - half_spread
        ask_price = adjusted_fair_value + half_spread

        bid_price = max(0.01, bid_price)
        ask_price = max(bid_price + 0.01, ask_price)

        return bid_price, ask_price

    def can_execute_order(self, order_type: str, trade_size: int) -> bool:
        """
        Checks whether trader can execute order without breaching inventory limits.

        Args:
            order_type: 'buy', 'sell', or 'none'.
            trade_size: Number of units traded.

        Returns:
            True if order can be executed, False otherwise.
        """

        if trade_size <= 0:
            raise ValueError("trade_size must be greater than 0.")

        if order_type == "buy":
            projected_inventory = self.inventory - trade_size

        elif order_type == "sell":
            projected_inventory = self.inventory + trade_size

        elif order_type == "none":
            return False

        else:
            raise ValueError("order_type must be 'buy', 'sell', or 'none'.")

        return abs(projected_inventory) <= self.max_inventory

    def execute_order(
        self,
        order_type: str,
        bid_price: float,
        ask_price: float,
        trade_size: int
    ) -> bool:
        """
        Executes customer order.

        If customer buys:
            Market maker sells at ask price.
            Inventory decreases.
            Cash increases.

        If customer sells:
            Market maker buys at bid price.
            Inventory increases.
            Cash decreases.

        Args:
            order_type: 'buy', 'sell', or 'none'.
            bid_price: Market maker's bid price.
            ask_price: Market maker's ask price.
            trade_size: Number of units traded.

        Returns:
            True if trade executed, False otherwise.
        """

        if bid_price <= 0:
            raise ValueError("bid_price must be greater than 0.")

        if ask_price <= 0:
            raise ValueError("ask_price must be greater than 0.")

        if ask_price <= bid_price:
            raise ValueError("ask_price must be greater than bid_price.")

        if trade_size <= 0:
            raise ValueError("trade_size must be greater than 0.")

        if order_type == "none":
            return False

        if not self.can_execute_order(order_type, trade_size):
            return False

        if order_type == "buy":
            self.inventory -= trade_size
            self.cash += ask_price * trade_size
            return True

        if order_type == "sell":
            self.inventory += trade_size
            self.cash -= bid_price * trade_size
            return True

        raise ValueError("order_type must be 'buy', 'sell', or 'none'.")

    def calculate_pnl(self, fair_value: float) -> float:
        """
        Calculates mark-to-market PnL.

        PnL = cash + inventory × current fair value

        Args:
            fair_value: Current fair value of the asset.

        Returns:
            Current PnL.
        """

        if fair_value <= 0:
            raise ValueError("fair_value must be greater than 0.")

        pnl = self.cash + self.inventory * fair_value
        return pnl
