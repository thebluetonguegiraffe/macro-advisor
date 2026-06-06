import requests
from langchain.tools import tool

from src.tools.eurostat.eurostat_constants import (
    EUROSTAT_GEO,
    EUROSTAT_UNE_FILTERS,
    EUROSTAT_STATS_URL,
    _parse_eurostat_response,
)


def _build_eurostat_employment_description() -> str:
    s_adj_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_UNE_FILTERS["s_adj"].items())
    age_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_UNE_FILTERS["age"].items())
    unit_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_UNE_FILTERS["unit"].items())
    sex_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_UNE_FILTERS["sex"].items())
    geo_str = ", ".join(f"{k}={v}" for k, v in EUROSTAT_GEO.items())

    return (
        "Fetches the monthly unemployment rate from Eurostat. "
        "Use to track labour market health across European countries.\n\n"
        "Parameters:\n"
        f"- country: 2-letter ISO code. Valid values: {geo_str}.\n"
        "Aggregates: 'EU', 'EA' (Eurozone).\n"
        "- sex: sex filter. "
        f"Options: {sex_str}. Default: T.\n"
        "- age: age group. "
        f"Options: {age_str}. Default: TOTAL.\n"
        "- unit: unit of measure. "
        f"Options: {unit_str}. Default: PC_ACT.\n"
        "- s_adj: seasonal adjustment. "
        f"Options: {s_adj_str}. Default: SA.\n"
        "- last_n: number of recent months to fetch (default 12).\n\n"
        "Example: country='ES', sex='F', age='Y_LT25', unit='PC_ACT' → "
        "unemployment rate for women under 25 in Spain."
    )


@tool(description=_build_eurostat_employment_description())
def get_eurostat_employment(
    country: str,
    sex: str = "T",
    age: str = "TOTAL",
    unit: str = "PC_ACT",
    s_adj: str = "SA",
    last_n: int = 12,
) -> dict:
    url = f"{EUROSTAT_STATS_URL}/une_rt_m"
    params = {
        "format": "JSON",
        "lang": "EN",
        "geo": country,
        "sex": sex,
        "age": age,
        "unit": unit,
        "s_adj": s_adj,
        "lastTimePeriod": last_n,
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return _parse_eurostat_response(response.json())
