import pytest
import requests
from src.tools.ecb.ecb_gdp import get_ecb_gdp
from src.tools.ecb.ecb_constants import ECB_GDP_FILTERS


def test_gdp_spain_defaults():
    result = get_ecb_gdp.invoke({"country": "ES"})
    assert len(result) == 8
    assert result[0] == {
        "FREQ": "Quarterly",
        "ADJUSTMENT": "Neither seasonally adjusted nor calendar adjusted data",
        "REF_AREA": "Spain",
        "COUNTERPART_AREA": "Domestic (home or reference area)",
        "REF_SECTOR": "Total economy",
        "COUNTERPART_SECTOR": "Total economy",
        "ACCOUNTING_ENTRY": "Balance (Credits minus Debits)",
        "STO": "Gross domestic product at market prices",
        "INSTR_ASSET": "Not applicable",
        "ACTIVITY": "Not applicable",
        "EXPENDITURE": "Not applicable",
        "UNIT_MEASURE": "Euro",
        "PRICES": "Current prices",
        "TRANSFORMATION": "Non transformed data",
        "period": "2024-Q2",
        "valor": 401519,
    }
    assert result[-1]["period"] == "2026-Q1"
    assert result[-1]["valor"] == 421392


def test_gdp_france_current_prices():
    result = get_ecb_gdp.invoke({"country": "FR", "last_n": 1})
    assert len(result) == 1
    assert result[0]["REF_AREA"] == "France"
    assert result[0]["PRICES"] == "Current prices"
    assert isinstance(result[0]["valor"], (int, float))


def test_gdp_invalid_country_raises():
    with pytest.raises(requests.exceptions.HTTPError):
        get_ecb_gdp.invoke({"country": "XX"})


def test_get_ecb_gdp_filters_structure():
    assert "prices" in ECB_GDP_FILTERS
    assert "adjustment" in ECB_GDP_FILTERS
    assert "V" in ECB_GDP_FILTERS["prices"]
    assert "N" in ECB_GDP_FILTERS["adjustment"]
