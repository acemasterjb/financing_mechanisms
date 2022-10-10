from datetime import datetime
from os import getenv
from typing import Any

from dotenv import load_dotenv
from httpx import Client, Timeout

load_dotenv()
COVALENT_URI = "https://api.covalenthq.com/v1"


def get_raw_historical_token_spot_prices(
    contract_address: str,
    start_date: datetime,
    end_date: datetime,
    chain_id: int = 1,
) -> list[dict[str, Any]]:
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")
    timeout = Timeout(10.0, read=15.0, connect=30.0)
    with Client(
        headers={
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            + "AppleWebKit/537.36 (KHTML, like Gecko) "
            + "Chrome/100.0.4896.127 Safari/537.36 Edg/100.0.1185.50"
        },
    ) as client:
        if contract_address == "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee":
            contract_address = "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"

        req_url = (
            COVALENT_URI
            + f"/pricing/historical_by_addresses_v2/{chain_id}"
            + f"/USD/{contract_address}/?quote-currency=USD&format=JSON"
            + f"&from={start_date}&to={end_date}&key=ckey_{getenv('COVALENT_KEY')}"
        )

        resp = client.get(req_url, timeout=timeout)
        resp.raise_for_status()
        print(resp.url)
        return resp.json()["data"][0]["prices"]


def format_raw_covalent_resp_entry(
    raw_covalent_resp_entry: dict[str, Any]
) -> dict[str, int | float]:
    return {
        "timestamp": raw_covalent_resp_entry["date"],
        "close": raw_covalent_resp_entry["price"],
    }


def get_historical_token_spot_prices(
    contract_address: str,
    start_date: int,
    end_date: int,
    chain_id: int = 1,
) -> list[dict[str, int | float]]:
    start_date = datetime.fromtimestamp(start_date)
    end_date = datetime.fromtimestamp(end_date)
    raw_covalent_resp = get_raw_historical_token_spot_prices(
        contract_address, start_date, end_date, chain_id
    )

    return list(map(format_raw_covalent_resp_entry, raw_covalent_resp))
