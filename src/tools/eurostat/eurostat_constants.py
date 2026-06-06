EUROSTAT_STATS_URL = "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data"

EUROSTAT_HPI_FILTERS = {
    "purchase": {
        "TOTAL": "Total",
        "DW_NEW": "Newly built dwellings",
        "DW_EXST": "Existing dwellings",
    },
    "unit": {
        "I10_Q": "Quarterly index 2010=100",
        "I15_Q": "Quarterly index 2015=100",
        "RCH_Q": "Quarterly rate of change",
        "RCH_A": "Annual rate of change",
    },
}

EUROSTAT_UNE_FILTERS = {
    "s_adj": {
        "NSA": "Unadjusted",
        "SA": "Seasonally adjusted",
        "TC": "Trend cycle",
    },
    "age": {
        "TOTAL": "Total",
        "Y_LT25": "Less than 25 years",
        "Y25-74": "From 25 to 74 years",
    },
    "unit": {
        "THS_PER": "Thousand persons",
        "PC_ACT": "Percentage of labour force",
    },
    "sex": {
        "T": "Total",
        "M": "Males",
        "F": "Females",
    },
}


EUROSTAT_GEO = {
    "EU": "European Union",
    "EU27_2020": "European Union 27 (from 2020)",
    "EA": "Eurozone",
    "EA20": "Eurozone 20 countries",
    "BE": "Belgium",
    "BG": "Bulgaria",
    "CZ": "Czech Republic",
    "DK": "Denmark",
    "DE": "Germany",
    "EE": "Estonia",
    "IE": "Ireland",
    "ES": "Spain",
    "FR": "France",
    "HR": "Croatia",
    "IT": "Italy",
    "CY": "Cyprus",
    "LV": "Latvia",
    "LT": "Lithuania",
    "LU": "Luxembourg",
    "HU": "Hungary",
    "MT": "Malta",
    "NL": "Netherlands",
    "AT": "Austria",
    "PL": "Poland",
    "PT": "Portugal",
    "RO": "Romania",
    "SI": "Slovenia",
    "SK": "Slovakia",
    "FI": "Finland",
    "SE": "Sweden",
    "IS": "Iceland",
    "NO": "Norway",
    "CH": "Switzerland",
    "UK": "United Kingdom",
    "TR": "Turkey",
}


def _parse_eurostat_response(data: dict) -> list[dict]:
    if not data.get("value"):
        raise ValueError("No data returned. Check that all parameters are valid.")

    times = list(data["dimension"]["time"]["category"]["index"].keys())
    values = data["value"]

    dimensions = {}
    for dim in data["id"]:
        if dim in ("freq", "time"):
            continue
        labels = list(data["dimension"][dim]["category"]["label"].values())
        dimensions[dim] = labels[0] if labels else None

    return [
        {
            **dimensions,
            "period": times[int(i)],
            "valor": v,
        }
        for i, v in values.items()
    ]
