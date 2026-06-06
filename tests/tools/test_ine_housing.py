from src.tools.ine.ine_housing import get_ine_housing


def test_nacional_general_variacion_anual():
    result = get_ine_housing.invoke({"nult": 1, "filters": ["349:16473", "345:16463", "3:74"]})
    assert result[0] == {
        "nombre": "Nacional. General. Variación anual.",
        "anyo": 2025,
        "periodo": "T4",
        "valor": 12.9,
        "unidad": "Tasas",
    }


def test_madrid_vivienda_nueva_variacion_anual():
    result = get_ine_housing.invoke({"nult": 1, "filters": ["70:9009", "345:16464", "3:74"]})
    assert result[0] == {
        "nombre": "Madrid, Comunidad de. Vivienda nueva. Variación anual.",
        "anyo": 2025,
        "periodo": "T4",
        "valor": 12.3,
        "unidad": "Tasas",
    }


def test_nacional_segunda_mano_variacion_trimestral():
    result = get_ine_housing.invoke({"nult": 1, "filters": ["349:16473", "345:16465", "3:73"]})
    assert result[0] == {
        "nombre": "Nacional. Vivienda segunda mano. Variación trimestral.",
        "anyo": 2025,
        "periodo": "T4",
        "valor": 1.8,
        "unidad": "Tasas",
    }
