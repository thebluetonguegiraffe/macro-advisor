from langchain.tools import tool
import requests

from src.tools.ecb.ecb_constants import ECB_BASE_URL, ECB_GDP_FILTERS, _parse_ecb_response


def _build_ecb_gdp_description() -> str:
    prices_str = ", ".join(f"{k}={v}" for k, v in ECB_GDP_FILTERS["prices"].items())
    adj_str = ", ".join(f"{k}={v}" for k, v in ECB_GDP_FILTERS["adjustment"].items())
    return (
        "Fetches GDP data from the ECB/Eurostat. "
        "Use to evaluate economic growth and macroeconomic health.\n\n"
        "Parameters:\n"
        "- country: 2-letter ISO code (e.g. 'ES', 'DE', 'FR'). Default: 'ES'.\n"
        f"- prices: price basis. Options: {prices_str}. Default: V.\n"
        f"- adjustment: seasonal adjustment. Options: {adj_str}. Default: N.\n"
        "- last_n: number of recent quarters to fetch (default 8)."
    )


@tool(description=_build_ecb_gdp_description())
def get_ecb_gdp(
    country: str = "ES",
    prices: str = "V",
    adjustment: str = "N",
    last_n: int = 8,
) -> list[dict]:
    url = f"{ECB_BASE_URL}/MNA/Q.{adjustment}.{country}.W2.S1.S1.B.B1GQ._Z._Z._Z.EUR.{prices}.N"
    params = {"lastNObservations": last_n, "format": "jsondata"}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return _parse_ecb_response(response.json())
