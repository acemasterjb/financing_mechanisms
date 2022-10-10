import pandas as pd


def get_historical_token_spot_prices(path: str, start_date: int, end_date: int):
    column_names = ["timestamp", "close", "volume"]
    data_types = {"timestamp": "int64", "close": "float64", "volume": "float64"}
    raw_data = pd.read_csv(
        path, names=column_names, index_col=0, dtype=data_types
    )
    raw_data: pd.DataFrame = raw_data.loc[start_date:end_date]

    return raw_data
