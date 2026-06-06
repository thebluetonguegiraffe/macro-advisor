from langchain.tools import tool
import requests

from src.tools.ecb.ecb_constants import ECB_BASE_URL, ECB_CPI_FILTERS, _parse_ecb_response


def _build_ecb_cpi_description() -> str:
    items_str = ", ".join(f"{k}={v}" for k, v in ECB_CPI_FILTERS["icp_item"].items())
    suffix_str = ", ".join(f"{k}={v}" for k, v in ECB_CPI_FILTERS["icp_suffix"].items())
    return (
        "Fetches HICP inflation data from the ECB. "
        "Use to track inflation trends and cost of living changes across EU countries.\n\n"
        "Parameters:\n"
        "- country: 2-letter ISO code (e.g. 'ES', 'DE', 'FR', 'IT'). Default: 'ES'.\n"
        f"- icp_item: category of goods/services. Options: {items_str}. Default: 000000.\n"
        f"- icp_suffix: type of measure. Options: {suffix_str}. Default: ANR.\n"
        "- last_n: number of recent months to fetch (default 12)."
    )


@tool(description=_build_ecb_cpi_description())
def get_ecb_cpi(
    country: str = "ES",
    icp_item: str = "000000",
    icp_suffix: str = "ANR",
    last_n: int = 12,
) -> list[dict]:
    url = f"{ECB_BASE_URL}/HICP/M.{country}.N.{icp_item}.4D0.{icp_suffix}"
    params = {"lastNObservations": last_n, "format": "jsondata"}
    response = requests.get(url, params=params)
    if response.status_code == 404:
        raise ValueError(
            f"No data found for country='{country}', icp_suffix='{icp_suffix}'. "
            f"Try icp_suffix='ANR' instead."
        )
    response.raise_for_status()
    return _parse_ecb_response(response.json())
