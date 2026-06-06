import requests
from langchain.tools import tool

from src.tools.ine.ine_constants import INE_BASE_URL, INE_EPA_FILTERS, _parse_ine_response


def _build_employment_description() -> str:
    ccaa_str = ", ".join(
        f"{v}={k.replace('_', ' ')}"
        for k, v in INE_EPA_FILTERS["comunidad_autonoma"]["values"].items()
    )
    sexo_str = ", ".join(
        f"{v}={k.replace('_', ' ')}" for k, v in INE_EPA_FILTERS["sexo"]["values"].items()
    )
    edad_items = INE_EPA_FILTERS["edad"]["values"]
    edad_str = ", ".join(
        f"{v['fk_variable']}:{v['id']}={k.replace('_', ' ')}" for k, v in edad_items.items()
    )

    return (
        "Fetches employment/unemployment data from INE (España, EPA survey). "
        "Table ID: 4247.\n\n"
        "Parameters:\n"
        "- nult: last N quarters (1-20). Use 1 for latest, 4 for ~1 year.\n"
        "- filters: list of 'fk_variable:value_id' strings. Use ONLY the IDs listed below.\n"
        "- date_from / date_to: date range as 'yyyymmdd'. Use date range OR nult, not both.\n\n"
        "Available filters (use fk_variable:value_id format):\n"
        f"  SEXO (fk_variable {INE_EPA_FILTERS['sexo']['fk_variable']}): {sexo_str}\n"
        f"  COMUNIDAD AUTÓNOMA (fk_variable {INE_EPA_FILTERS['comunidad_autonoma']['fk_variable']}):\n"  # noqa
        "    For all Spain, omit this filter entirely.\n"
        f"    {ccaa_str}\n"
        "  EDAD (fk_variable varía por tramo):\n"
        f"    {edad_str}\n\n"
        "Time range (use ONE):\n"
        "  - nult: last N quarters (1=latest, 4=~1 year, max 20).\n"
        "  - date_from + date_to: exact range as 'yyyymmdd'.\n\n"
        "Example: filters=['70:9009', '18:452'] → Madrid, hombres.\n"
        "NEVER invent IDs — only use the values listed above."
    )


@tool(description=_build_employment_description())
def get_ine_employment(
    nult: int = 1,
    filters: list[str] | None = None,
    date_from: str | None = None,
    date_to: str | None = None,
) -> list[dict]:
    url = f"{INE_BASE_URL}/DATOS_TABLA/4247"
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
    result = get_ine_employment.invoke({"nult": 1})
    print(result[:2])

    result = get_ine_employment.invoke({"nult": 1, "filters": ["18:453"]})
    print(result[:2])
