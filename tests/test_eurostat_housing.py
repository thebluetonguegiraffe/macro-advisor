import pytest
import requests
from src.tools.eurostat.eurostat_housing import get_eurostat_housing
from src.tools.eurostat.eurostat_constants import EUROSTAT_HPI_FILTERS, EUROSTAT_GEO


def test_germany_default_params():
    result = get_eurostat_housing.invoke({"country": "DE"})
    assert len(result) == 8
    assert result[0] == {
        "purchase": "Purchases of existing dwellings",
        "unit": "Annual rate of change",
        "geo": "Germany",
        "period": "2024-Q1",
        "valor": -5.7,
    }
    assert result[-1] == {
        "purchase": "Purchases of existing dwellings",
        "unit": "Annual rate of change",
        "geo": "Germany",
        "period": "2025-Q4",
        "valor": 3.0,
    }


def test_france_newly_built_annual():
    result = get_eurostat_housing.invoke(
        {
            "country": "FR",
            "purchase": "DW_NEW",
            "unit": "RCH_A",
            "last_n": 2,
        }
    )
    assert len(result) == 2
    assert result[0] == {
        "purchase": "Purchases of newly built dwellings",
        "unit": "Annual rate of change",
        "geo": "France",
        "period": "2025-Q3",
        "valor": 1.0,
    }
    assert result[1] == {
        "purchase": "Purchases of newly built dwellings",
        "unit": "Annual rate of change",
        "geo": "France",
        "period": "2025-Q4",
        "valor": 0.2,
    }


def test_spain_existing_quarterly():
    result = get_eurostat_housing.invoke(
        {
            "country": "ES",
            "purchase": "DW_EXST",
            "unit": "RCH_Q",
            "last_n": 2,
        }
    )
    assert len(result) == 2
    assert result[0] == {
        "purchase": "Purchases of existing dwellings",
        "unit": "Quarterly rate of change",
        "geo": "Spain",
        "period": "2025-Q3",
        "valor": 3.3,
    }
    assert result[1] == {
        "purchase": "Purchases of existing dwellings",
        "unit": "Quarterly rate of change",
        "geo": "Spain",
        "period": "2025-Q4",
        "valor": 1.8,
    }


def test_invalid_country_raises():
    with pytest.raises((requests.exceptions.HTTPError, ValueError)):
        get_eurostat_housing.invoke({"country": "XX"})


def test_catalogue_structure():
    assert "purchase" in EUROSTAT_HPI_FILTERS
    assert "unit" in EUROSTAT_HPI_FILTERS
    assert len(EUROSTAT_HPI_FILTERS["purchase"]) > 0
    assert len(EUROSTAT_HPI_FILTERS["unit"]) > 0


def test_geo_catalogue():
    assert "DE" in EUROSTAT_GEO
    assert "FR" in EUROSTAT_GEO
    assert "ES" in EUROSTAT_GEO
    assert "UK" in EUROSTAT_GEO
    assert len(EUROSTAT_GEO) > 0
