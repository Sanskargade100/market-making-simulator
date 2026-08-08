import os

import matplotlib
matplotlib.use("Agg")

import pandas as pd
import matplotlib.pyplot as plt

from simulation import run_market_making_simulation


def _ensure_output_directory(output_path: str) -> None:
    """Creates the parent folder for output_path if it does not exist."""

    output_directory = os.path.dirname(output_path)
    if output_directory:
        os.makedirs(output_directory, exist_ok=True)


def plot_pnl_chart(
    results_dataframe: pd.DataFrame,
    output_path: str = "results/pnl_chart.png"
) -> None:
    """
    Plots PnL over time.
    """

    if results_dataframe.empty:
        raise ValueError("results_dataframe cannot be empty.")

    _ensure_output_directory(output_path)

    plt.figure(figsize=(10, 6))
    plt.plot(results_dataframe["time_step"], results_dataframe["pnl"])
    plt.xlabel("Time Step")
    plt.ylabel("PnL")
    plt.title("Market Maker PnL Over Time")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_inventory_chart(
    results_dataframe: pd.DataFrame,
    output_path: str = "results/inventory_chart.png"
) -> None:
    """
    Plots inventory over time.
    """

    if results_dataframe.empty:
        raise ValueError("results_dataframe cannot be empty.")

    _ensure_output_directory(output_path)

    plt.figure(figsize=(10, 6))
    plt.plot(results_dataframe["time_step"], results_dataframe["inventory"])
    plt.xlabel("Time Step")
    plt.ylabel("Inventory")
    plt.title("Market Maker Inventory Over Time")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_spread_analysis(
    output_path: str = "results/spread_analysis.png"
) -> None:
    """
    Runs simulations with different spreads and plots final PnL.
    """

    _ensure_output_directory(output_path)

    spread_values = [0.5, 1.0, 2.0, 3.0, 5.0]
    final_pnls = []
    number_of_trades = []

    for spread in spread_values:
        results_dataframe, metrics = run_market_making_simulation(
            num_steps=1000,
            initial_fair_value=100.0,
            volatility=1.0,
            order_probability=0.7,
            buy_probability=0.5,
            sell_probability=0.5,
            trade_size=1,
            base_spread=spread,
            max_inventory=20,
            inventory_penalty=0.1,
            random_seed=42
        )

        final_pnls.append(metrics["final_pnl"])
        number_of_trades.append(metrics["number_of_trades"])

    spread_dataframe = pd.DataFrame({
        "base_spread": spread_values,
        "final_pnl": final_pnls,
        "number_of_trades": number_of_trades
    })

    plt.figure(figsize=(10, 6))
    plt.plot(spread_dataframe["base_spread"], spread_dataframe["final_pnl"], marker="o")
    plt.xlabel("Base Spread")
    plt.ylabel("Final PnL")
    plt.title("Effect of Spread Width on Final PnL")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


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

    plot_pnl_chart(results)
    plot_inventory_chart(results)
    plot_spread_analysis()

    print("Charts saved to results/")
