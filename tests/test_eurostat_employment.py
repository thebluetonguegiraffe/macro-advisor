import pytest
import requests
from src.tools.eurostat.eurostat_employment import get_eurostat_employment
from src.tools.eurostat.eurostat_constants import EUROSTAT_UNE_FILTERS, EUROSTAT_GEO


def test_spain_default_params():
    result = get_eurostat_employment.invoke({"country": "ES"})
    assert len(result) == 12
    assert result[0] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Total",
        "unit": "Percentage of population in the labour force",
        "sex": "Total",
        "geo": "Spain",
        "period": "2025-05",
        "valor": 10.6,
    }
    assert result[-1] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Total",
        "unit": "Percentage of population in the labour force",
        "sex": "Total",
        "geo": "Spain",
        "period": "2026-04",
        "valor": 10.3,
    }


def test_germany_females_under25():
    result = get_eurostat_employment.invoke(
        {
            "country": "DE",
            "sex": "F",
            "age": "Y_LT25",
            "last_n": 2,
        }
    )
    assert len(result) == 2
    assert result[0] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Less than 25 years",
        "unit": "Percentage of population in the labour force",
        "sex": "Females",
        "geo": "Germany",
        "period": "2026-03",
        "valor": 6.4,
    }
    assert result[1] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Less than 25 years",
        "unit": "Percentage of population in the labour force",
        "sex": "Females",
        "geo": "Germany",
        "period": "2026-04",
        "valor": 6.2,
    }


def test_france_thousands_persons():
    result = get_eurostat_employment.invoke(
        {
            "country": "FR",
            "unit": "THS_PER",
            "last_n": 2,
        }
    )
    assert len(result) == 2
    assert result[0] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Total",
        "unit": "Thousand persons",
        "sex": "Total",
        "geo": "France",
        "period": "2026-03",
        "valor": 2615,
    }
    assert result[1] == {
        "s_adj": "Seasonally adjusted data, not calendar adjusted data",
        "age": "Total",
        "unit": "Thousand persons",
        "sex": "Total",
        "geo": "France",
        "period": "2026-04",
        "valor": 2632,
    }


def test_invalid_country_raises():
    with pytest.raises((requests.exceptions.HTTPError, ValueError)):
        get_eurostat_employment.invoke({"country": "XX"})


def test_catalogue_structure():
    assert "s_adj" in EUROSTAT_UNE_FILTERS
    assert "age" in EUROSTAT_UNE_FILTERS
    assert "unit" in EUROSTAT_UNE_FILTERS
    assert "sex" in EUROSTAT_UNE_FILTERS
    for group, values in EUROSTAT_UNE_FILTERS.items():
        assert len(values) > 0, f"Empty values in group '{group}'"


def test_geo_catalogue():
    assert "DE" in EUROSTAT_GEO
    assert "ES" in EUROSTAT_GEO
    assert "FR" in EUROSTAT_GEO
    assert len(EUROSTAT_GEO) > 0
