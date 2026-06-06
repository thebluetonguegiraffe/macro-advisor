from src.tools.ine.ine_employment import get_ine_employment


def test_no_filters_returns_national_data():
    result = get_ine_employment.invoke({"nult": 1})
    assert result[0] == {
        "nombre": "Tasa de paro de la población. Ambos sexos. Total Nacional. Total.",
        "anyo": 2023,
        "periodo": "T4",
        "valor": 11.76,
        "unidad": "Tasas",
    }


def test_filter_sexo_mujeres():
    result = get_ine_employment.invoke({"nult": 1, "filters": ["18:453"]})
    assert result[0] == {
        "nombre": "Tasa de paro de la población. Mujeres. Total Nacional. Total.",
        "anyo": 2023,
        "periodo": "T4",
        "valor": 13.36,
        "unidad": "Tasas",
    }


def test_filter_comunidad_and_sexo():
    result = get_ine_employment.invoke({"nult": 1, "filters": ["70:9013", "18:453"]})
    assert result[0] == {
        "nombre": "Tasa de paro de la población. Mujeres. Rioja, La. Total.",
        "anyo": 2023,
        "periodo": "T4",
        "valor": 10.09,
        "unidad": "Tasas",
    }


def test_filter_edad_menores_25():
    result = get_ine_employment.invoke({"nult": 1, "filters": ["357:10568"]})
    assert result[0] == {
        "nombre": "Tasa de paro de la población. Ambos sexos. Total Nacional. Menores de 25 años.",
        "anyo": 2023,
        "periodo": "T4",
        "valor": 28.36,
        "unidad": "Tasas",
    }
