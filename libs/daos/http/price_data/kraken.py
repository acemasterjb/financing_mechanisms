from typing import Any

from httpx import Client

BASE_URL = "https://api.kraken.com/0/public/"
HEADERS = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1b) Gecko/20020722",
}


def get_raw_historical_ohlc_token_spot_prices(
    pair: str, start_date: int
) -> list[list[int | str]]:
    """ get a kraken response for historical OHLC data

        note: this will only get the last 720 days of data (from "utc now")
        for datapoints that are older, use the 
    """
    path = "OHLC"
    params = {"pair": pair, "interval": 1440, "since": start}

    with Client(headers=HEADERS) as client:
        resp = client.get(BASE_URL + path, params=params)
        print(resp.url)
        return resp.json()["result"][pair]


def format_raw_uni_resp_entry(
    raw_kraken_resp_entry: list[str | int],
) -> dict[str, int | float]:
    return {
        "timestamp": raw_kraken_resp_entry[0],
        "open": float(raw_kraken_resp_entry[1]),
        "high": float(raw_kraken_resp_entry[2]),
        "low": float(raw_kraken_resp_entry[3]),
        "close": float(raw_kraken_resp_entry[4]),
        "volume": float(raw_kraken_resp_entry[6]),
    }


def get_historical_ohlc_token_spot_prices(
    pair: str, start_date: int
) -> list[dict[str, int | float]]:
    raw_kraken_resp = get_raw_historical_ohlc_token_spot_prices(pair, start)

    return list(map(format_raw_uni_resp_entry, raw_kraken_resp))


# def get_next
# def format_historical_close_prices
# def get_historical
