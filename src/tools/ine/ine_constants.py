INE_BASE_URL = "https://servicios.ine.es/wstempus/js/ES"

INE_CCAA = {
    "andalucia": "8997",
    "aragon": "8998",
    "asturias": "8999",
    "baleares": "9000",
    "canarias": "9001",
    "cantabria": "9002",
    "castilla_y_leon": "9003",
    "castilla_la_mancha": "9004",
    "cataluna": "9005",
    "comunitat_valenciana": "9006",
    "extremadura": "9007",
    "galicia": "9008",
    "madrid": "9009",
    "murcia": "9010",
    "navarra": "9011",
    "pais_vasco": "9012",
    "la_rioja": "9013",
    "ceuta": "9015",
    "melilla": "8995",
}
INE_IPV_FILTERS = {
    "comunidad_autonoma": {
        "fk_variable": "70",
        "nacional": {"fk_variable": "349", "id": "16473"},
        "values": INE_CCAA,
    },
    "tipo_vivienda": {
        "fk_variable": "345",
        "values": {
            "general": "16463",
            "vivienda_nueva": "16464",
            "vivienda_segunda_mano": "16465",
        },
    },
    "indicador": {
        "fk_variable": "3",
        "values": {
            "indice": "83",
            "variacion_trimestral": "73",
            "variacion_anual": "74",
            "variacion_ytd": "87",
        },
    },
}


INE_EPA_FILTERS = {
    "sexo": {
        "fk_variable": "18",
        "values": {
            "ambos_sexos": "454",
            "hombres": "452",
            "mujeres": "453",
        },
    },
    "comunidad_autonoma": {
        "fk_variable": "70",
        "nacional": {"fk_variable": "349", "id": "16473"},
        "values": INE_CCAA,
    },
    "edad": {
        "values": {
            "total": {"fk_variable": "356", "id": "15668"},
            "menores_25": {"fk_variable": "357", "id": "10568"},
            "25_y_mas": {"fk_variable": "357", "id": "10569"},
            "16_a_19": {"fk_variable": "360", "id": "10553"},
            "20_a_24": {"fk_variable": "360", "id": "15661"},
            "25_a_54": {"fk_variable": "360", "id": "10561"},
            "55_y_mas": {"fk_variable": "357", "id": "10560"},
        },
    },
}


def _parse_ine_response(data: list[dict]) -> list[dict]:
    result = []
    for serie in data:
        for point in serie.get("Data", []):
            result.append(
                {
                    "nombre": serie.get("Nombre", "").strip(),
                    "anyo": point.get("Anyo"),
                    "periodo": point.get("T3_Periodo"),
                    "valor": point.get("Valor"),
                    "unidad": serie.get("T3_Unidad", "").strip(),
                }
            )
    return result
