import requests
from langchain.tools import tool

from src.tools.ine.ine_constants import INE_BASE_URL, INE_IPV_FILTERS, _parse_ine_response


def _build_housing_description() -> str:
    ccaa_str = ", ".join(
        f"{v}={k.replace('_', ' ')}"
        for k, v in INE_IPV_FILTERS["comunidad_autonoma"]["values"].items()
    )
    tipo_str = ", ".join(
        f"{v}={k.replace('_', ' ')}" for k, v in INE_IPV_FILTERS["tipo_vivienda"]["values"].items()
    )
    indicador_str = ", ".join(
        f"{v}={k.replace('_', ' ')}" for k, v in INE_IPV_FILTERS["indicador"]["values"].items()
    )

    return (
        "Fetches the housing price index for Spain from INE (IPV). "
        "Table ID: 25171. Quarterly data.\n\n"
        "Parameters:\n"
        "- nult: last N quarters (1-20). Use 4 for 1 year, 12 for 3 years.\n"
        "- filters: list of 'fk_variable:value_id' strings. "
        "Always specify all three dimensions to avoid getting 239 rows.\n"
        "- date_from / date_to: date range as 'yyyymmdd'. Use date range OR nult, not both.\n\n"
        "Available filters (use fk_variable:value_id format):\n"
        "  COMUNIDAD AUTÓNOMA:\n"
        f"    Nacional → {INE_IPV_FILTERS['comunidad_autonoma']['nacional']['fk_variable']}:{INE_IPV_FILTERS['comunidad_autonoma']['nacional']['id']}. For all Spain, use this.\n"  # noqa
        f"    CCAA (fk_variable {INE_IPV_FILTERS['comunidad_autonoma']['fk_variable']}): {ccaa_str}\n"  # noqa
        f"  TIPO VIVIENDA (fk_variable {INE_IPV_FILTERS['tipo_vivienda']['fk_variable']}): {tipo_str}\n"  # noqa
        f"  INDICADOR (fk_variable {INE_IPV_FILTERS['indicador']['fk_variable']}): {indicador_str}\n\n"  # noqa
        "Time range (use ONE):\n"
        "  - nult: last N quarters (1=latest, 4=~1 year, max 20).\n"
        "  - date_from + date_to: exact range as 'yyyymmdd'.\n\n"
        "Example: filters=['349:16473', '345:16463', '3:74'] → Nacional, general, variación anual.\n"  # noqa
        "NEVER invent IDs — only use the values listed above."
    )


@tool(description=_build_housing_description())
def get_ine_housing(
    nult: int = 4,
    filters: list[str] | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    url = f"{INE_BASE_URL}/DATOS_TABLA/25171"
    params = [("nult", nult), ("tip", "A")]
    if filters:
        for f in filters:
            params.append(("tv", f))
    if date_from and date_to:
        params = [(k, v) for k, v in params if k != "nult"]
        params.append(("date", f"{date_from}:{date_to}"))
    response = requests.get(url, params=params)
    response.raise_for_status()
    return _parse_ine_response(response.json())


if __name__ == "__main__":
    result = get_ine_housing.invoke({"nult": 1, "filters": ["349:16473", "345:16463", "3:74"]})
    print(result[:2])
