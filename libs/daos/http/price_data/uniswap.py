from os import getenv
from typing import Callable

from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

load_dotenv()
QUERY_URL = "https://gateway.thegraph.com/api/{api}/subgraphs/id/2szAn45skWZFLPUbxFEtjiEzT1FMW8Ff5ReUPbZbQxtt"


def replace_placeholder(input_str: str, placeholder: str, value: str):
    return input_str.replace(placeholder, value)


def reduce_string(
    func: Callable, input_str: str, placeholders: list[str], values: list[str]
):
    output_str = input_str
    for placeholder, value in zip(placeholders, values):
        output_str = func(output_str, placeholder, value)
    return output_str


def get_raw_historical_token_spot_prices(
    token_contract_address: str, start_date: int, end_date: int
) -> list[dict[str, str | int]]:
    transport = RequestsHTTPTransport(
        QUERY_URL.format(api=getenv("GRAPH_API")), verify=True, retries=2
    )

    with Client(transport=transport, fetch_schema_from_transport=True) as session:
        query_str = """
            {
                tokenDayDatas(
                where:{
                    token: "$token_contract_address",
                    date_gte: $start,
                    date_lte: $end
                }
                ){
                    id
                    priceUSD
                    date
                }
            }
            """
        placeholders = ["$token_contract_address", "$start", "$end"]
        values = [token_contract_address, str(start_date), str(end_date)]
        final_query_string = reduce_string(
            replace_placeholder, query_str, placeholders, values
        )
        query = gql(final_query_string)

        resp = session.execute(query)
        try:
            return resp["tokenDayDatas"]
        except KeyError:
            print("The graph node(s) indexing this data is most likely out of sync")
            raise


def format_raw_uni_resp_entry(
    raw_uni_resp_entry: dict[str, str | int]
) -> dict[str, int | float]:
    return {
        "timestamp": raw_uni_resp_entry["date"],
        "close": float(raw_uni_resp_entry["priceUSD"]),
    }


def get_historical_token_spot_prices(
    token_contract_address: str, start_date: int, end_date: int
) -> list[dict[str, int | float]]:
    raw_uni_resp = get_raw_historical_token_spot_prices(
        token_contract_address, start_date, end_date
    )

    return list(map(format_raw_uni_resp_entry, raw_uni_resp))
