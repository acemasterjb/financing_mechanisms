import pandas as pd


def calculate_twap(dataseries: pd.Series, timeframe_in_days: int) -> float:
    return dataseries.sum() / timeframe_in_days

def calculate_twap_ohlc(dataset: list[dict[str, int | float]], timeframe_in_days: int) -> float:
    dataset_df = pd.DataFrame(dataset)
    daily_ohlc = pd.DataFrame(dataset_df[["open", "high", "low", "close"]], dtype="float64")
    daily_ohlc_avg = daily_ohlc.mean(axis=1)

    return calculate_twap(daily_ohlc_avg, timeframe_in_days)

def calculate_twap_interday(dataset: list[dict[str, int | float]], timeframe_in_days: int) -> float:
    dataset_df = pd.Series([entry["close"] for entry in dataset], dtype="float64")
    
    return calculate_twap(dataset_df, timeframe_in_days)
