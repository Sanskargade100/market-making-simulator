import os

import pandas as pd

from market import Market
from trader import MarketMaker
from risk import calculate_final_metrics


def run_market_making_simulation(
    num_steps: int = 1000,
    initial_fair_value: float = 100.0,
    volatility: float = 1.0,
    order_probability: float = 0.7,
    buy_probability: float = 0.5,
    sell_probability: float = 0.5,
    trade_size: int = 1,
    base_spread: float = 2.0,
    max_inventory: int = 20,
    inventory_penalty: float = 0.1,
    random_seed: int | None = 42
) -> tuple[pd.DataFrame, dict]:
    """
    Runs a complete market-making simulation.

    Args:
        num_steps: Number of simulation steps.
        initial_fair_value: Starting fair value of the asset.
        volatility: Random movement size of fair value.
        order_probability: Probability that a customer order arrives.
        buy_probability: Probability customer buys from market maker.
        sell_probability: Probability customer sells to market maker.
        trade_size: Number of units per trade.
        base_spread: Total bid-ask spread.
        max_inventory: Maximum inventory allowed.
        inventory_penalty: Inventory quote adjustment strength.
        random_seed: Random seed for reproducibility.

    Returns:
        results_dataframe, final_metrics
    """

    if num_steps <= 0:
        raise ValueError("num_steps must be greater than 0.")

    market = Market(
        initial_fair_value=initial_fair_value,
        volatility=volatility,
        order_probability=order_probability,
        buy_probability=buy_probability,
        sell_probability=sell_probability,
        trade_size=trade_size,
        random_seed=random_seed
    )

    trader = MarketMaker(
        base_spread=base_spread,
        max_inventory=max_inventory,
        inventory_penalty=inventory_penalty,
        initial_cash=0.0
    )

    simulation_records = []

    for time_step in range(1, num_steps + 1):
        fair_value = market.update_fair_value()

        bid_price, ask_price = trader.calculate_quotes(fair_value=fair_value)

        order_type = market.generate_customer_order()

        starting_inventory = trader.inventory
        starting_cash = trader.cash

        trade_executed = trader.execute_order(
            order_type=order_type,
            bid_price=bid_price,
            ask_price=ask_price,
            trade_size=trade_size
        )

        ending_inventory = trader.inventory
        ending_cash = trader.cash

        pnl = trader.calculate_pnl(fair_value=fair_value)

        simulation_records.append({
            "time_step": time_step,
            "fair_value": fair_value,
            "bid_price": bid_price,
            "ask_price": ask_price,
            "spread": ask_price - bid_price,
            "order_type": order_type,
            "trade_executed": trade_executed,
            "trade_size": trade_size if trade_executed else 0,
            "starting_inventory": starting_inventory,
            "ending_inventory": ending_inventory,
            "inventory": ending_inventory,
            "starting_cash": starting_cash,
            "ending_cash": ending_cash,
            "cash": ending_cash,
            "pnl": pnl
        })

    results_dataframe = pd.DataFrame(simulation_records)

    final_metrics = calculate_final_metrics(results_dataframe)

    return results_dataframe, final_metrics


def save_simulation_results(
    results_dataframe: pd.DataFrame,
    output_path: str = "results/simulation_results.csv"
) -> None:
    """
    Saves simulation results as CSV.

    Args:
        results_dataframe: DataFrame containing simulation results.
        output_path: CSV output path.
    """

    if results_dataframe.empty:
        raise ValueError("results_dataframe cannot be empty.")

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)

    results_dataframe.to_csv(output_path, index=False)


if __name__ == "__main__":
    results, metrics = run_market_making_simulation(
        num_steps=1000,
        initial_fair_value=100.0,
        volatility=1.0,
        order_probability=0.7,
        buy_probability=0.5,
        sell_probability=0.5,
        trade_size=1,
        base_spread=2.0,
        max_inventory=20,
        inventory_penalty=0.1,
        random_seed=42
    )

    save_simulation_results(results)

    print(results.head())
    print("\nFinal Metrics:")
    for metric_name, metric_value in metrics.items():
        print(f"{metric_name}: {metric_value}")

    print("\nResults saved to results/simulation_results.csv")
