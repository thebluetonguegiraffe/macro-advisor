ECB_BASE_URL = "https://data-api.ecb.europa.eu/service/data"
ECB_CPI_FILTERS = {
    "icp_item": {
        "000000": "HICP Total",
        "FOOD00": "Food",
        "NRGY00": "Energy",
        "GOODS0": "Goods",
        "SERV00": "Services",
        "XEF000": "Core inflation (excl. food and energy)",
    },
    "icp_suffix": {
        "ANR": "Annual rate of change",
        "MAR": "Monthly rate of change (not available for all countries)",
        "INX": "Index",
        "CTR": "Contribution to annual rate",
    },
}

ECB_GDP_FILTERS = {
    "prices": {
        "V": "Current prices (nominal)",
        "Q": "Chain-linked volumes",
        "L": "Chain-linked volumes, % change on previous period",
    },
    "adjustment": {
        "N": "Not seasonally adjusted",
        "Y": "Seasonally and calendar adjusted",
    },
}


def _parse_ecb_response(data: dict) -> list[dict]:
    dimensions = data["structure"]["dimensions"]
    series_dims = dimensions["series"]
    time_values = [t["id"] for t in dimensions["observation"][0]["values"]]

    # build label lookup per dimension: position_index -> label
    dim_labels = {dim["id"]: [v["name"] for v in dim["values"]] for dim in series_dims}

    result = []
    for series_key, series_data in data["dataSets"][0]["series"].items():
        positions = [int(i) for i in series_key.split(":")]
        series_meta = {
            dim["id"]: dim_labels[dim["id"]][positions[idx]]
            for idx, dim in enumerate(series_dims)
            if dim_labels[dim["id"]]
        }
        for obs_idx, obs_values in series_data["observations"].items():
            value = obs_values[0]
            if value is not None:
                result.append(
                    {
                        **series_meta,
                        "period": time_values[int(obs_idx)],
                        "valor": value,
                    }
                )
    return result
