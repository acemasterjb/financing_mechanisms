from httpx import Client

BASE_URL = "https://api.gateio.ws/api/v4"
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


def get_raw_historical_token_spot_prices(
    _pair: str, _start_date: int, _end_date: int
) -> list[list[int | float]]:
    path = "/spot/candlesticks"
    params = {"currency_pair": _pair, "from": _start_date, "to": _end_date, "interval": "1d"}

    with Client(headers=HEADERS) as client:
        resp = client.get(BASE_URL + path, params=params)
        return resp.json()


def format_raw_gate_io_resp_entry(
    raw_gate_io_resp_entry: list[int | float],
) -> dict[str, int | float]:
    return {
        "timestamp": raw_gate_io_resp_entry[0],
        "volume": float(raw_gate_io_resp_entry[1]),
        "close": float(raw_gate_io_resp_entry[2]),
        "high": float(raw_gate_io_resp_entry[3]),
        "low": float(raw_gate_io_resp_entry[4]),
        "open": float(raw_gate_io_resp_entry[5]),
    }


def get_historical_token_spot_prices(
    pair: str, start_date: int, end_date: int
) -> list[dict[str, int | float]]:
    raw_gate_io_resp = get_raw_historical_token_spot_prices(pair, start_date, end_date)

    return list(map(format_raw_gate_io_resp_entry, raw_gate_io_resp))
