import requests
from langchain.tools import tool

from src.tools.eurostat.eurostat_constants import (
    EUROSTAT_GEO,
    EUROSTAT_HPI_FILTERS,
    EUROSTAT_STATS_URL,
    _parse_eurostat_response,
)


def _build_eurostat_housing_description() -> str:
    purchase_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_HPI_FILTERS["purchase"].items())
    unit_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_HPI_FILTERS["unit"].items())
    geo_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_GEO.items())
    return (
        "Fetches the quarterly House Price Index (HPI) from Eurostat. "
        "Use to analyze real estate costs and housing inflation across European countries.\n\n"
        "Parameters:\n"
        f"- country: 2-letter ISO code. Valid values: {geo_str}.\n"
        "Aggregates: 'EU' (full EU), 'EA' (Eurozone).\n"
        "- purchase: type of dwelling purchase. "
        f"Options: {purchase_str}. Default: DW_EXST.\n"
        "- unit: unit of measure. "
        f"Options: {unit_str}. Default: RCH_A.\n"
        "- last_n: number of recent periods to fetch (default 8).\n\n"
        "Example: country='DE', purchase='DW_NEW', unit='RCH_A' → "
        "annual rate of change for newly built dwellings in Germany."
    )


@tool(description=_build_eurostat_housing_description())
def get_eurostat_housing(
    country: str,
    purchase: str = "DW_EXST",
    unit: str = "RCH_A",
    last_n: int = 8,
) -> dict:
    url = f"{EUROSTAT_STATS_URL}/prc_hpi_q"
    params = {
        "format": "JSON",
        "lang": "EN",
        "purchase": purchase,
        "unit": unit,
        "geo": country,
        "lastTimePeriod": last_n,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return _parse_eurostat_response(response.json())
