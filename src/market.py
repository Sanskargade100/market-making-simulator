import random


class Market:
    """
    Simulates a simple market where the fair value of an asset changes over time.
    """

    def __init__(
        self,
        initial_fair_value: float = 100.0,
        volatility: float = 1.0,
        order_probability: float = 0.7,
        buy_probability: float = 0.5,
        sell_probability: float = 0.5,
        trade_size: int = 1,
        random_seed: int | None = 42,
    ):
        """
        Args:
            initial_fair_value: Starting fair value of the asset.
            volatility: Maximum random movement of fair value per step.
            order_probability: Probability that a customer order arrives.
            buy_probability: Probability customer buys from market maker.
            sell_probability: Probability customer sells to market maker.
            trade_size: Number of units traded per order.
            random_seed: Random seed for reproducibility.
        """

        if initial_fair_value <= 0:
            raise ValueError("initial_fair_value must be greater than 0.")

        if volatility < 0:
            raise ValueError("volatility cannot be negative.")

        if not 0 <= order_probability <= 1:
            raise ValueError("order_probability must be between 0 and 1.")

        if not 0 <= buy_probability <= 1:
            raise ValueError("buy_probability must be between 0 and 1.")

        if not 0 <= sell_probability <= 1:
            raise ValueError("sell_probability must be between 0 and 1.")

        if buy_probability + sell_probability == 0:
            raise ValueError("At least one of buy_probability or sell_probability must be positive.")

        if trade_size <= 0:
            raise ValueError("trade_size must be greater than 0.")

        self.initial_fair_value = initial_fair_value
        self.fair_value = initial_fair_value
        self.volatility = volatility
        self.order_probability = order_probability
        self.buy_probability = buy_probability
        self.sell_probability = sell_probability
        self.trade_size = trade_size
        self.random_seed = random_seed

        if random_seed is not None:
            random.seed(random_seed)

    def reset(self) -> None:
        """
        Resets the market back to its starting state so a fresh simulation
        can be run with the same parameters and seed.
        """

        self.fair_value = self.initial_fair_value

        if self.random_seed is not None:
            random.seed(self.random_seed)

    def update_fair_value(self) -> float:
        """
        Randomly updates the fair value.

        Returns:
            Updated fair value.
        """

        price_change = random.uniform(-self.volatility, self.volatility)
        self.fair_value = max(0.01, self.fair_value + price_change)

        return self.fair_value

    def generate_customer_order(self) -> str:
        """
        Generates a random customer order.

        Returns:
            'buy', 'sell', or 'none'.

            buy  = customer buys from the market maker.
            sell = customer sells to the market maker.
            none = no trade.
        """

        order_arrival_random_value = random.random()

        if order_arrival_random_value > self.order_probability:
            return "none"

        total_trade_probability = self.buy_probability + self.sell_probability
        normalised_buy_probability = self.buy_probability / total_trade_probability

        trade_direction_random_value = random.random()

        if trade_direction_random_value < normalised_buy_probability:
            return "buy"

        return "sell"
