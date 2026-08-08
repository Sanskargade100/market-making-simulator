import pandas as pd


def calculate_max_drawdown(pnl_series: pd.Series) -> float:
    """
    Calculates maximum drawdown from a PnL series.

    Args:
        pnl_series: Series of PnL values.

    Returns:
        Maximum drawdown.
    """

    if pnl_series.empty:
        raise ValueError("pnl_series cannot be empty.")

    running_max = pnl_series.cummax()
    drawdown = running_max - pnl_series
    max_drawdown = drawdown.max()

    return float(max_drawdown)


def calculate_pnl_volatility(pnl_series: pd.Series) -> float:
    """
    Calculates standard deviation of PnL changes.

    Args:
        pnl_series: Series of PnL values.

    Returns:
        PnL volatility.
    """

    if pnl_series.empty:
        raise ValueError("pnl_series cannot be empty.")

    pnl_changes = pnl_series.diff().dropna()

    if pnl_changes.empty:
        return 0.0

    pnl_volatility = pnl_changes.std()

    return float(pnl_volatility)


def calculate_sharpe_ratio(pnl_series: pd.Series) -> float:
    """
    Calculates a per-step Sharpe ratio: the average PnL change divided by the
    volatility of PnL changes. This is a simple risk-adjusted measure of how
    much profit the strategy earns per unit of risk taken.

    Args:
        pnl_series: Series of PnL values.

    Returns:
        Sharpe ratio (0.0 if there is no volatility to divide by).
    """

    if pnl_series.empty:
        raise ValueError("pnl_series cannot be empty.")

    pnl_changes = pnl_series.diff().dropna()

    if pnl_changes.empty:
        return 0.0

    volatility = pnl_changes.std()

    if volatility == 0:
        return 0.0

    sharpe_ratio = pnl_changes.mean() / volatility

    return float(sharpe_ratio)


def calculate_final_metrics(results_dataframe: pd.DataFrame) -> dict:
    """
    Calculates final summary metrics from simulation results.

    Args:
        results_dataframe: DataFrame containing simulation output.

    Returns:
        Dictionary of risk and performance metrics.
    """

    if results_dataframe.empty:
        raise ValueError("results_dataframe cannot be empty.")

    required_columns = ["pnl", "inventory", "trade_executed"]

    for column in required_columns:
        if column not in results_dataframe.columns:
            raise ValueError(f"Missing required column: {column}")

    pnl_series = results_dataframe["pnl"]

    final_pnl = float(pnl_series.iloc[-1])
    max_drawdown = calculate_max_drawdown(pnl_series)
    pnl_volatility = calculate_pnl_volatility(pnl_series)
    sharpe_ratio = calculate_sharpe_ratio(pnl_series)
    max_inventory = int(results_dataframe["inventory"].abs().max())
    number_of_trades = int(results_dataframe["trade_executed"].sum())

    metrics = {
        "final_pnl": final_pnl,
        "max_drawdown": max_drawdown,
        "pnl_volatility": pnl_volatility,
        "sharpe_ratio": sharpe_ratio,
        "max_absolute_inventory": max_inventory,
        "number_of_trades": number_of_trades,
    }

    return metrics
