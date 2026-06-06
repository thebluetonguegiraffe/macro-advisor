import requests
from langchain.tools import tool

from src.tools.ecb.ecb_constants import ECB_BASE_URL, _parse_ecb_response


def _build_ecb_rates_description() -> str:
    return (
        "Fetches the official ECB key interest rates: Deposit Facility (DFR), "
        "Marginal Lending Facility (MLFR), and Main Refinancing Operations (MRR_FR). "
        "Use to analyze ECB monetary policy stance and borrowing costs.\n\n"
        "Parameters:\n"
        "- last_n: number of recent observations to fetch (default 12)."
    )


@tool(description=_build_ecb_rates_description())
def get_ecb_rates(last_n: int = 12) -> list[dict]:
    url = f"{ECB_BASE_URL}/FM/D.U2.EUR.4F.KR.MRR_FR+DFR+MLFR.LEV"
    params = {"lastNObservations": last_n, "format": "jsondata"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return _parse_ecb_response(response.json())
