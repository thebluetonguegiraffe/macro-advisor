import pytest
import requests
from src.tools.ecb.ecb_cpi import get_ecb_cpi


def test_cpi_spain_defaults():
    result = get_ecb_cpi.invoke({"country": "ES"})
    assert len(result) == 12
    assert result[0] == {
        "FREQ": "Monthly",
        "REF_AREA": "Spain",
        "ADJUSTMENT": "Neither seasonally nor working day adjusted",
        "ICP_ITEM": "HICP - Total",
        "DATA_PROVIDER": "Statistical Office of the European Commission (Eurostat)",
        "ICP_SUFFIX": "Annual rate of change",
        "period": "2025-06",
        "valor": 2.3,
    }
    assert result[-1]["period"] == "2026-05"
    assert result[-1]["valor"] == 3.6


def test_cpi_germany_annual():
    result = get_ecb_cpi.invoke({"country": "DE", "last_n": 1})
    assert len(result) == 1
    assert result[0]["REF_AREA"] == "Germany"
    assert result[0]["ICP_SUFFIX"] == "Annual rate of change"
    assert isinstance(result[0]["valor"], float)


def test_cpi_spain_energy():
    result = get_ecb_cpi.invoke({"country": "ES", "icp_item": "NRGY00", "last_n": 1})
    assert len(result) == 1
    assert "Energy" in result[0]["ICP_ITEM"]


def test_cpi_spain_monthly_rate_not_available():
    with pytest.raises(ValueError, match="No data found"):
        get_ecb_cpi.invoke({"country": "ES", "icp_suffix": "MAR", "last_n": 1})


def test_cpi_germany_monthly_rate():
    result = get_ecb_cpi.invoke({"country": "DE", "icp_suffix": "MAR", "last_n": 1})
    assert len(result) == 1
    assert isinstance(result[0]["valor"], float)


def test_cpi_invalid_country_raises():
    with pytest.raises((ValueError, requests.exceptions.HTTPError)):
        get_ecb_cpi.invoke({"country": "XX"})
